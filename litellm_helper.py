import os
import sys
import time

import litellm


def disable_litellm_logging():
    # disable litllm debug logs
    # https://github.com/BerriAI/litellm/issues/6813
    litellm._logging._disable_debugging()


def check_litellm_key(args):
    api_key_valid = litellm.check_valid_key(
        api_key=os.environ["OPENROUTER_API_KEY"], model=args.model_name
    )
    assert api_key_valid is True, "API key is not valid"


def call_llm(model, messages, provider):
    """Call llm, get a response (hopefully)

    Returns:
        response: litellm.Response object, content"""
    NBR_PROVIDER_RETRIES = 10
    response = None
    # check we have a well-formed message to send
    for message in messages:
        assert "content" in message.keys()
        assert "role" in message.keys()
    for retry_n in range(NBR_PROVIDER_RETRIES):
        temperature = 1.0
        if temperature != 1.0:
            print(f"~~~~~~~~~~~~~# non default TEMPERATURE {temperature}")
        try:
            response = litellm.completion(
                model=model,
                messages=messages,
                transforms=[""],
                route="",
                provider=provider,
                timeout=20,
                temperature=temperature,
            )
        except litellm.RateLimitError as e:
            print(f"!Rate limit error: {e}")
            print("Sleeping for a bit...")
            time.sleep(2)
        except litellm.Timeout as e:
            print(f"!Timeout error: {e}")
            print("Sleeping for a bit...")
            time.sleep(2)
        except litellm.APIError as e:
            print(f"!APIError error: {e}")
            print("Sleeping for a bit...")
            time.sleep(2)
        if response is not None:
            break
    if response is None:
        print("Failed to get a response after retries")
        sys.exit(1)
    return response, response.choices[0].message.content
