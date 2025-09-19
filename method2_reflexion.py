# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

import logging
from datetime import datetime
from pprint import pprint

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

Given the above examples and guidance, write several bullet points that explain the rules that convert the input patterns to the output patterns. Do note write any code, just explain the rules in a block that is marked like the following and ends with:
<EXPLANATION>
...
</EXPLANATION>
"""


prompt_for_reflexion = """
# Feedback on your mistake

Your explanation was wrong, the code you created from it did not work. You must now come up with a new explanation that is better that will work. It must explain how to get from the initial grid to the final grid correctly. Reflect on the previous explanation and come up with a new idea that is radically different.
"""


def call_then_ask_for_new_explanation(model, messages, provider, llm_responses):
    """Call the LLM with the description and any past explanations, ask for new explanation"""
    response, explanation_response_as_text = call_llm(model, messages, provider)

    llm_responses.append(response)
    return explanation_response_as_text


def call_then_ask_for_code_from_explanation(model, messages, provider, llm_responses):
    messages.append(make_message_part(prompt_for_python_code, "user"))
    response2, code_response2_as_text = call_llm(model, messages, provider)
    llm_responses.append(response2)
    # print("CODE (as text):")
    # print(code_response2_as_text)
    code_as_string = extract_from_code_block(code_response2_as_text)
    # print("CODE (as code):")
    # print(code_as_string)
    return code_as_string


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
    REFLEXION_ITERATIONS = 3
    if REFLEXION_ITERATIONS != 3:
        # useful debug message to ian
        print(f"---REFLEXION_ITERATIONS is {REFLEXION_ITERATIONS}, not 3")
    previous_explanations = []
    # we can force the previous explanation part for debugging
    # previous_explanations = ["""<EXPLANATION>This is a word substitution puzzle where numbers are switched around</EXPLANATION>"""]
    for n in range(REFLEXION_ITERATIONS):
        prompt_to_describe_problem = make_prompt(
            template_name, problems, target="train", func_dict=func_dict
        )
        messages_to_get_explanation = []
        messages_to_get_explanation.append(
            make_message_part(prompt_to_describe_problem, "user")
        )
        # if we've iterated and failed, list the previous (incorrect) explanations
        if previous_explanations:
            explanation_prompt_pre = """Previously you wrote the following explanations, each of these are WRONG. You must not repeat these explanations, you must come up with something radically different."""
            messages_to_get_explanation.append(
                make_message_part(explanation_prompt_pre, "user")
            )
            for previous_explanation in previous_explanations:
                messages_to_get_explanation.append(
                    make_message_part(
                        "Incorrect explanation:\n" + previous_explanation, "assistant"
                    )
                )
            explanation_prompt_post = """Never repeat the above explanations, you must come up with something radically different. Start by explaining why this might be wrong."""
            messages_to_get_explanation.append(
                make_message_part(explanation_prompt_post, "user")
            )
        # Next ask for a new explanation
        messages_to_get_explanation.append(
            make_message_part(prompt_for_explanation, "user")
        )

        print("PROMPT:")
        # print(initial_prompt, prompt_for_explanation)
        pprint(messages_to_get_explanation)

        explanation_response_as_text = call_then_ask_for_new_explanation(
            model, messages_to_get_explanation, provider, llm_responses
        )
        print("EXPLANATION:")
        print(explanation_response_as_text)
        previous_explanations.append(explanation_response_as_text)

        # Build a new prompt using the most recent explanation (and not any historic bad explanations)
        messages_to_get_code = []
        messages_to_get_code.append(
            make_message_part(prompt_to_describe_problem, "user")
        )
        messages_to_get_code.append(make_message_part(prompt_for_explanation, "user"))
        messages_to_get_code.append(
            make_message_part(explanation_response_as_text, "assistant")
        )
        code_as_string = call_then_ask_for_code_from_explanation(
            model, messages_to_get_code, provider, llm_responses
        )
        print(f"CODE: \n-----\n{code_as_string}\n-----")

        # run the code
        train_problems = problems["train"]
        rr_train = execute_transform(code_as_string, train_problems)
        print("----rr_train on execution1")
        print(rr_train)
        # input("Press Enter to continue...")

        if rr_train[0].transform_ran_and_matched_for_all_inputs:
            # we've succeeded
            print("--------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if n > 0:
                print("---------------*******************!!!!")
            print(f"--------------SUCCESS on iteration  {n}  !!!!!!!!!!!!!!!")
            print("--------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            rr_trains.append(rr_train)
            return rr_train
        # if we failed, we need to iterate, so just loop again

    print("--------------xxxxxxxxxxxxxxxxxxxx")
    print("--------------FAILURE on this run xxxxxx")
    print("--------------xxxxxxxxxxxxxxxxxxxx")
    # take the last execution result, move on
    rr_trains.append(rr_train)
    return rr_train


def run_experiment_for_iterations(
    db_filename: str, model, provider, iterations, problems, template_name
):
    """"""
    llm_responses = []
    rr_trains = []

    successes = 0
    for n in range(iterations):
        print(
            f"---------------------------------------------------------------------------------------\nPrompt iteration {n}"
        )
        print(
            "\n\n---------------------------------------------------------------------------------------\n"
        )
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
        print(f"rr_trains: {len(rr_trains)}")
        rr_train = rr_trains[-1]
        success = rr_train[0].transform_ran_and_matched_for_all_inputs
        successes += success
        if success:
            print(
                "-------------------------------- SUCCESS --------------------------------"
            )
            # input("Press Enter to continue...")
        print(f"Successes: {successes} on {n=} of {iterations=}")
    assert len(rr_trains) == iterations
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
