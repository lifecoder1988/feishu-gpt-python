# Note: The openai-python library support for Azure OpenAI is in preview.
import logging
import os
import openai
#from openai import AsyncOpenAI
from util.app_config import app_config
from util.logger import gpt_logger, app_logger
if app_config.IS_AZURE:
    openai.api_type = "azure"
    openai.api_base = app_config.AZURE_API_HOST
    openai.api_version = "2023-03-15-preview"
    openai.api_key = app_config.AZURE_API_KEY
else:
    openai.base_url = app_config.API_URL
    openai.api_key = app_config.OPENAI_KEY


def get_single_response(user_id,message, prompt=app_config.DEFAULT_PROMPT):
    return get_chat_response(user_id,[{"role": "user", "content": message}])


def get_chat_response(user_id, chat_history, prompt=app_config.DEFAULT_PROMPT):
    messages = [{"role": "system", "content": prompt}, *chat_history]
    messages = [entry for entry in messages if entry['content']]
    gpt_logger.info("GPT request: %s", messages)
    response = get_gpt_response(user_id,messages)
    print(response.choices[0].message)
    return response.choices[0].message.content

    if "choices" not in response:
        gpt_logger.info("GPT raw response1: %s", response)
        return ""
    choice = response["choices"][0]  # type: ignore
    if "message" not in choice:
        gpt_logger.info("GPT raw response: %s", response)
        return ""
    message = choice["message"]
    print("22222")
    print(message)
    if "content" in message and "role" in message and message["role"] == "assistant":
        gpt_logger.info("GPT response: %s", message["content"])
        return message["content"]
    gpt_logger.info("GPT raw response2: %s", response)
    return ""


def get_gpt_response(user_id,messages):
    response = openai.chat.completions.create(
        model=app_config.GPT_MODEL,
        messages=messages,
        user=user_id,
        stop=None)
    return response


if __name__ == "__main__":
    app_logger.info(get_chat_response([{"role": "assistant", "content": "Hello, how can I help you?"}, {
                    "role": "user", "content": "Tell me a joke."}]))
    app_logger.info(get_single_response("什么是战争国债"))
