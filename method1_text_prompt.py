# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

import re
from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

import analysis

# from litellm import completion
import utils
from db import make_db, record_run
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
        iterations=args.iterations,
        problems=problems,
        template_name=args.template_name,
    )

    analysis.summarise_results(rr_trains)
    analysis.summarise_llm_responses(llm_responses)
    end_dt = datetime.now()
    dt_delta = end_dt - start_dt
    print(f"Experiment took {dt_delta}")
    print(f"Full logs in:\n{experiment_folder}/experiment.log")
