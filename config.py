# TODO
# https://openrouter.ai/meta-llama/llama-4-scout?quantization=bf16

# When executing, check github state and if True will break if git not committed
# use this if I'm recording experiments
BREAK_IF_NOT_CHECKED_IN = False

# model_list = [
#    {'model_name': 'deepseek-chat-v3-0324',
##   'litellm_params': {'model': "openrouter/deepseek/deepseek-chat-v3-0324"}}
# ]


providers = {
    # DeepSeek V3 0324
    # https://openrouter.ai/deepseek/deepseek-chat-v3-0324
    "openrouter/deepseek/deepseek-chat-v3-0324": {
        "order": [
            "lambda/fp8",  # "Lambda",  # fp8, 164k, 164k
            # "beseten/fp8", # Beseten, fp8 164k context 131k length
            # "gmicloud/fp8", # GMiCloud, fp8 164k 164k
            # "chutes/fp8", # Chutes, fp8 164k 164k
            # "deepinfra/fp8",  # "DeepInfra",  # fp8, 164k, 164k
            # "nebius/fp8",  # "Nebius AI Studio",  # fp8 164k, 164k
        ],
        "allow_fallbacks": False,
    },
    # Opus 4 is multimodal (text and image)
    "openrouter/anthropic/claude-opus-4": {
        "order": [
            "anthropic",  # 200k, 32k
            "google-vertex",  # 200k, 32k
        ],
        "allow_fallbacks": False,
    },
    # GPT 4o, multimodal
    # https://openrouter.ai/openai/gpt-4o/api
    # GPT o3 - needs private (2nd) OpenAI key so I'm ignoring it
    # GPT o1-pro is crazy expensive! Multimodal
    # https://openrouter.ai/openai/o1-pro
    # GPT o1 is more like Opus 4 on pricing, multimodal
    # https://openrouter.ai/openai/o1
}
