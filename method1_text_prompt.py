# GOAL
# Can you make a generic prompt that correctly describes the rules governgin how
# the initial grid turns into the final grid?
# BONUS can you make it write code that solves this?

from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

import analysis

# from litellm import completion
import utils
from config import providers  # BREAK_IF_NOT_CHECKED_IN
from litellm_helper import call_llm, check_litellm_key, disable_litellm_logging
from prompt import get_func_dict, make_prompt
from run_code import execute_transform
from utils import (
    extract_from_code_block,
    initial_log,
    make_experiment_folder,
    setup_logging,
)

disable_litellm_logging()

load_dotenv()


def run_experiment(model, provider, problems, messages, rr_trains, llm_responses):
    response, content = call_llm(model, messages, provider)
    llm_responses.append(response)
    # print(response)
    # print(response.choices[0].message.content)
    # print(content)
    logger.info(f"Content: {content}")

    code_as_string = extract_from_code_block(content)

    train_problems = problems["train"]
    rr_train = execute_transform(code_as_string, train_problems)
    # print(rr_train)
    logger.info(f"RR train: {rr_train}")
    rr_trains.append(rr_train)


def run_experiment_for_iterations(model, provider, iterations, problems, template_name):
    """method1_text_prompt's run experiment"""
    llm_responses = []
    rr_trains = []

    # make a prompt before calling LLM
    func_dict = get_func_dict()
    prompt = make_prompt(template_name, problems, target="train", func_dict=func_dict)

    # print("PROMPT (printed once, as we iterate on the same prompt):")
    # print(prompt)
    logger.info(f"Prompt: {prompt}")
    content = [{"type": "text", "text": prompt}]
    messages = [{"content": content, "role": "user"}]
    # we could print the whole json block
    # print(f"{messages=}")

    for n in tqdm(range(iterations)):
        run_experiment(model, provider, problems, messages, rr_trains, llm_responses)
    return llm_responses, rr_trains


if __name__ == "__main__":
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
    exp_folder = make_experiment_folder()
    logger = setup_logging(exp_folder)
    initial_log(logger, args)
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
    # print(
    #    "\n--\n".join(
    #        [response.choices[0].message.content for response in llm_responses]
    #    )
    # )

    analysis.summarise_results(rr_trains)
    analysis.summarise_llm_responses(llm_responses)
    end_dt = datetime.now()
    dt_delta = end_dt - start_dt
    print(f"Experiment took {dt_delta}")
    print(f"Full logs in:\n{experiment_folder}/experiment.log")
