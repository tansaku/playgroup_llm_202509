# playgroup_llm_202509


# Walkthrough

```
python prompt.py --help # select a template and problem to render
python prompt.py -t baseline.j2 -p 0d3d703e # render this problem
```

```
python run_code.py --help
python run_code.py -p 0d3d703e -c example_solutions/ex_soln_0d3d703e.py # run good solution on the right problem
python run_code.py -p 0d3d703e -c example_solutions/ex_soln_08ed6ac7.py # run the wrong solution on a different problem
```

The `run_code` module builds a `utils.RunResult` result, this tracks if and how many of the example `initial` problems were transformed correctly to the desired `final` states.

### run method1 with the default prompt on an easy problem for 5 iterations

```
# run the basic method with the default prompt for 5 iterations
python method1_text_prompt.py --help # see the arg description
python method1_text_prompt.py -p 0d3d703e -i 5
# this is equivalent to the fully formed version which selects the prompt and model to run
# python method1_text_prompt.py -p 0d3d703e -t baseline.j2 -m openrouter/deepseek/deepseek-chat-v3-0324 -i 5
``` 


# Setup notes


## Setup notes by Ian for Ian

```
conda activate basepython312
cd /home/ian/workspace/personal/playgroup/playgroup_llm_202509
python -m venv .venv
. .venv/bin/activate # activate local env
pip install -r requirements.txt

# chatgpt recommendation for folder monitoring, cross platform
sudo apt install fswatch
```

### pre-commit

```
# pre-commit, on .pre-commit-config.yaml
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-commit
```

### track folder file changes

```
# simpler output
fswatch --event Created --event Updated --event Removed -x ./*.py | while read file event; do     echo "$(date '+%Y-%m-%d %H:%M:%S')  $file  $event"; done
# works, very verbose, multiple reports per single change
fswatch -x ./*.py | while read file event; do     echo "$(date '+%Y-%m-%d %H:%M:%S')  $file  $event"; done
```

### run pytest every time a file changes

```
#fswatch -r -x tests/ src/ | while read file event; do
# run tests after a file change
fswatch -r -x *.py | while read file event; do
    clear
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Change detected in $file ($event)"
    pytest
    sleep 1
done
```
