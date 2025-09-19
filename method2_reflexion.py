# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

import logging
from datetime import datetime

# from litellm import completion
from dotenv import load_dotenv

import analysis
import utils
from config import providers
from db import make_db
from litellm_helper import call_llm, check_litellm_key, disable_litellm_logging
from prompt import get_func_dict, make_prompt
from run_code import execute_transform
from utils import (
    extract_from_code_block,
    initial_log,
    make_experiment_folder,
    make_message_part,
    setup_logging,
)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
disable_litellm_logging()

load_dotenv()

prompt_for_python_code = """
## Action to write a solution in Python

After this write a solution in Python code that follows the following format. You must accept an `initial` np.ndarray of numbers as input and return a `final` np.ndarray of numbers. Each number is in the range [0...9] and the grid is rectangular. The grid size of `final` may be different to the size of `initial`.

You can use only pure Python, numpy.

```python
import numpy as np
def transform(initial):
    assert isinstance(initial, np.ndarray)
    ... # you need to write code to generate `final`
    assert isinstance(final, np.ndarray)
    return final
```
"""

prompt_for_explanation = """
## Action to explain what you see

Given the above examples, write several bullet points that explain the rules that convert the input patterns to the output patterns. Do note write any code, just explain the rules in a block that is marked like the following and ends with </EXPLANATION>:
<EXPLANATION>
...
</EXPLANATION>
"""

prompt_for_reflexion = """"""


def run_experiment(
    db_filename: str,
    iteration_n: int,
    model,
    provider,
    problems,
    template_name,
    rr_trains,
    llm_responses,
):
    # make a prompt before calling LLM
    func_dict = get_func_dict()
    initial_prompt = make_prompt(
        template_name, problems, target="train", func_dict=func_dict
    )
    messages = [make_message_part(initial_prompt, "user")]
    messages.append(make_message_part(prompt_for_explanation, "user"))

    print("PROMPT:")
    print(initial_prompt, prompt_for_explanation)

    def ask_for_explanation_and_code(model, messages, provider):
        # first send in the opening prompt which asks for an explanation
        response = call_llm(model, messages, provider)
        assert response is not None, "No response from LLM after retries"
        llm_responses.append(response)
        print(response)
        # this should be the explanation
        explanation_response_as_text = response.choices[0].message.content
        print("EXPLANATION:")
        print(explanation_response_as_text)

        messages.append(
            utils.make_message_part(explanation_response_as_text, "assistant")
        )
        messages.append(utils.make_message_part(prompt_for_python_code, "user"))
        response2 = call_llm(model, messages, provider)
        assert response2 is not None, "No response from LLM after retries"
        llm_responses.append(response2)
        print("CODE (as text):")
        code_response2_as_text = response2.choices[0].message.content
        print(code_response2_as_text)
        code_as_string = extract_from_code_block(code_response2_as_text)
        print("CODE (as code):")
        print(code_as_string)
        return explanation_response_as_text, code_as_string

    explanation_response_as_text, code_as_string = ask_for_explanation_and_code(
        model, messages, provider
    )

    # run the code
    train_problems = problems["train"]
    rr_train = execute_transform(code_as_string, train_problems)
    print("----rr_train on execution1")
    print(rr_train)

    if rr_train[0].transform_ran_and_matched_for_all_inputs:
        # we've succeeded
        rr_trains.append(rr_train)
        return rr_train
    # instead - we didn't get success
    messages = [make_message_part(initial_prompt, "user")]
    messages.append(make_message_part(prompt_for_explanation, "user"))
    messages.append(make_message_part(explanation_response_as_text, "assistant"))
    prompt_for_reflexion = """
# Feedback on your mistake

Your explanation was wrong, the code you created from it did not work. You must now come up with a new explanation that is better that will work. It must explain how to get from the initial grid to the final grid correctly. Reflect on the previous explanation and come up with a new idea that is radically different.
"""
    messages.append(make_message_part(prompt_for_reflexion, "user"))
    messages.append(make_message_part(prompt_for_explanation, "user"))

    explanation_response_as_text, code_as_string = ask_for_explanation_and_code(
        model, messages, provider
    )
    train_problems = problems["train"]
    rr_train = execute_transform(code_as_string, train_problems)
    print("----rr_train on execution2")
    print(rr_train)
    rr_trains.append(rr_train)
    return rr_train


def run_experiment_for_iterations(
    db_filename: str, model, provider, iterations, problems, template_name
):
    """"""
    llm_responses = []
    rr_trains = []

    for n in range(iterations):
        run_experiment(
            db_filename,
            n,
            model,
            provider,
            problems,
            template_name,
            rr_trains,
            llm_responses,
        )
    return llm_responses, rr_trains


if __name__ == "__main__":
    # We can force the code to _only run_ if fully checked it
    # if BREAK_IF_NOT_CHECKED_IN:
    #    utils.break_if_not_git_committed()

    parser = utils.add_argument_parser(
        problem_name=True, template_name=True, iterations=True, model_name=True
    )
    args = parser.parse_args()
    print(args)
    check_litellm_key(args)
    experiment_folder = make_experiment_folder()
    print(f"tail -n +0 -f {experiment_folder}/experiment.log")
    print(f"sqlite3 {experiment_folder}/experiments.db")
    exp_folder = make_experiment_folder()
    logger = setup_logging(exp_folder)
    initial_log(logger, args)
    start_dt = datetime.now()
    logger.info("Started experiment")

    db_filename = make_db(exp_folder)
    logger.info(f"Database created at: {db_filename}")

    # load a single problem
    problems = utils.get_examples(args.problem_name)

    model = args.model_name

    llm_responses, rr_trains = run_experiment_for_iterations(
        db_filename=db_filename,
        model=model,
        provider=providers[args.model_name],
        iterations=args.iterations,
        problems=problems,
        template_name=args.template_name,
    )

    analysis.summarise_results(rr_trains)
    analysis.summarise_llm_responses(llm_responses)
    end_dt = datetime.now()
    dt_delta = end_dt - start_dt
    print(f"Experiment took {dt_delta}")
