# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

import re

from dotenv import load_dotenv
from tqdm import tqdm

from db import record_run
from litellm_helper import call_llm, check_litellm_key, disable_litellm_logging
from prompt import get_func_dict, make_prompt
from run_code import execute_transform

# from litellm import completion
from utils import (
    do_first_setup,
    do_last_report,
    extract_from_code_block,
    make_message_part,
)

disable_litellm_logging()

load_dotenv()


def extract_explanation(text):
    """Extract content between EXPLANATION tags."""
    pattern = r"<EXPLANATION>(.*?)</EXPLANATION>"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        return ""  # return empty string if no explanation found


def run_experiment(
    db_filename: str,
    iteration_n: int,
    model,
    problems,
    messages,
    rr_trains,
    llm_responses,
):
    response, content = call_llm(model, messages)
    llm_responses.append(response)
    logger.info(f"Content: {content}")
    messages_plus_response = messages + [make_message_part(content, "assistant")]

    code_as_string = extract_from_code_block(content)

    train_problems = problems["train"]
    rr_train = execute_transform(code_as_string, train_problems)
    explanation = extract_explanation(content)
    record_run(
        db_filename,
        iteration_n,
        explanation,
        code_as_string,
        messages_plus_response,
        rr_train[0].transform_ran_and_matched_for_all_inputs,
    )
    logger.info(f"RR train: {rr_train}")
    rr_trains.append(rr_train)


def run_experiment_for_iterations(
    db_filename: str, model, iterations, problems, template_name
):
    """method1_text_prompt's run experiment"""
    llm_responses = []
    rr_trains = []

    # make a prompt before calling LLM
    func_dict = get_func_dict()
    initial_prompt = make_prompt(
        template_name, problems, target="train", func_dict=func_dict
    )
    logger.info(f"Prompt: {initial_prompt}")

    messages = [make_message_part(initial_prompt, "user")]

    for n in tqdm(range(iterations)):
        run_experiment(
            db_filename,
            n,
            model,
            problems,
            messages,
            rr_trains,
            llm_responses,
        )
    return llm_responses, rr_trains


if __name__ == "__main__":
    # We can force the code to _only run_ if fully checked it
    # if BREAK_IF_NOT_CHECKED_IN:
    #    utils.break_if_not_git_committed()

    args, experiment_folder, logger, start_dt, db_filename, problems = do_first_setup()
    check_litellm_key(args)  # note this will check any provider
    model = args.model_name

    llm_responses, rr_trains = run_experiment_for_iterations(
        db_filename=db_filename,
        model=model,
        iterations=args.iterations,
        problems=problems,
        template_name=args.template_name,
    )

    do_last_report(rr_trains, llm_responses, experiment_folder, start_dt)
