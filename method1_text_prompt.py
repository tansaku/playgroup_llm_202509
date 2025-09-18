# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

import logging
from collections import Counter
from datetime import datetime

from dotenv import load_dotenv

# from litellm import completion
import utils
from config import BREAK_IF_NOT_CHECKED_IN, providers
from litellm_helper import call_llm, check_litellm_key, disable_litellm_logging
from prompt import get_func_dict, make_prompt
from run_code import execute_transform
from utils import extract_from_code_block

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
disable_litellm_logging()

load_dotenv()


def run_experiment(model, provider, problems, messages, rr_trains, llm_responses):
    response, content = call_llm(model, messages, provider)
    llm_responses.append(response)
    # print(response)
    # print(response.choices[0].message.content)
    print(content)

    code_as_string = extract_from_code_block(content)

    train_problems = problems["train"]
    rr_train = execute_transform(code_as_string, train_problems)
    # rr_train is a tuple of RunResult, ExecutionOutcome, exception_message
    # rr_train[0].code_ran_on_all_inputs will be True if all train examples ran regardless of output quality
    # rr_train[0].transform_ran_and_matched_for_all_inputs will be True if all train inputs were transformed correctly
    if rr_train[0].transform_ran_and_matched_for_all_inputs:
        breakpoint()
    print(rr_train)
    rr_trains.append(rr_train)


def run_experiment_for_iterations(model, provider, iterations, problems, template_name):
    """method1_text_prompt's run experiment"""
    llm_responses = []
    rr_trains = []

    # make a prompt before calling LLM
    func_dict = get_func_dict()
    prompt = make_prompt(template_name, problems, target="train", func_dict=func_dict)

    print("PROMPT (printed once, as we iterate on the same prompt):")
    print(prompt)
    content = [{"type": "text", "text": prompt}]
    messages = [{"content": content, "role": "user"}]
    # we could print the whole json block
    # print(f"{messages=}")

    for n in range(iterations):
        print(
            f"---------------------------------------------------------------------------------------\nPrompt iteration {n}"
        )
        print(
            "\n\n---------------------------------------------------------------------------------------\n"
        )
        run_experiment(model, provider, problems, messages, rr_trains, llm_responses)
    return llm_responses, rr_trains


if __name__ == "__main__":
    if BREAK_IF_NOT_CHECKED_IN:
        utils.break_if_not_git_committed()

    parser = utils.add_argument_parser(
        problem_name=True, template_name=True, iterations=True, model_name=True
    )
    args = parser.parse_args()
    print(args)
    check_litellm_key(args)
    utils.initial_log(logger, args)
    start_dt = datetime.now()
    logger.info("Started experiment")

    # load a single problem
    problems = utils.get_examples(args.problem_name)

    model = args.model_name

    llm_responses, rr_trains = run_experiment_for_iterations(
        model=model,
        provider=providers[args.model_name],
        iterations=args.iterations,
        problems=problems,
        template_name=args.template_name,
    )

    # show responses
    print(
        "\n--\n".join(
            [response.choices[0].message.content for response in llm_responses]
        )
    )

    # rr_trains[0][0].transform_ran_and_matched_for_all_inputs
    # rr_trains is the list of RunResult pairs for the training problems
    # each pair contains the RunResult and the grids initial/final/generated
    # rr is each instance of the pair so rr[0] is the RunResult
    # and we want to know how often transform_ran_and_matched_for_all_inputs
    # was True, i.e. how many runs were correct
    print(
        f"Got {sum([rr[0].transform_ran_and_matched_for_all_inputs for rr in rr_trains])} of {len(rr_trains)} runs correct"
    )

    cnt_provider = Counter([response.provider for response in llm_responses])
    print(f"Provider counts: {cnt_provider}")

    all_token_usages = [
        llm_response.usage.total_tokens for llm_response in llm_responses
    ]

    print(
        f"Max token usage on a call was {max(all_token_usages):,}, "
        f"Median token usage on a call was {sorted(all_token_usages)[int(len(all_token_usages) / 2)]:,}"
    )
    # print(f"Max token usage on a call was {max(all_token_usages)}")
    # print(
    #    f"Median token usage on a call was {sorted(all_token_usages)[int(len(all_token_usages)/2)]}"
    # )
    end_dt = datetime.now()
    dt_delta = end_dt - start_dt
    print(f"Experiment took {dt_delta}")
