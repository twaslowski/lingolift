import logging
import os

import json5 as json
from openai import OpenAI

from llm.message import Message

api_key = os.getenv("OPENAI_API_KEY", None)
logger = logging.getLogger("root")


# todo: This breaks the literal_translations endpoint, because that relies on parsing the response to a JSON.


def openai_exchange(
    messages: list[Message],
    model_name: str = "gpt-3.5-turbo-1106",
    json_mode: bool = False,
) -> dict | str:
    """
    Abstraction layer for the OpenAI API.
    :param model_name: OpenAI model name.
    :param messages: List of message objects to emulate session state.
    Usually just contains System prompt and User request.
    :param json_mode: Whether to use LLM JSON mode. Defaults to False as OpenAI forcibly generates JSONs with an
    object root, not lists, even when instructed otherwise.
    :return: JSON response of LLM
    Note: If this was used in an interactive chat context, this should return a Message() object to track session state.
    However, in this context, we're simply consuming the responses without need for state, so this is fine.
    """
    client = OpenAI(api_key=api_key)
    logger.info(f"Sending messages to OpenAI API: {messages}")
    response_format = "json_object" if json_mode else "text"
    # mypy complains about the usage of the create() function, but clearly it works
    completion = client.chat.completions.create(  # type: ignore
        model=model_name,
        response_format={"type": response_format},
        messages=[message.asdict() for message in messages],
    )
    response = completion.choices[0].message.content
    logger.info(f"Received response: {response}")
    return response


def parse_response(gpt_response: str) -> dict:
    # Sometimes, llm will hallucinate '```json' at the start of the JSON it returns. This solves that.
    cleaned_response = gpt_response.replace("`", "").replace("json", "")
    return json.loads(cleaned_response)
