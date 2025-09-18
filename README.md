# playgroup_llm_202509


# Walkthrough

* `python method1_text_prompt.py -p 0d3d703e -i 5` # run method1 with the default prompt on an easy problem for 5 iterations
  * equivalent to the fully formed `python method1_text_prompt.py -p 0d3d703e -t baseline.j2 -m openrouter/deepseek/deepseek-chat-v3-0324 -i 5`


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
