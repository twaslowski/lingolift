import json

import iso639
from shared.exception import ApplicationException

from generative.response_suggestion import generate_response_suggestions
from generative.translation import generate_translation
from generative.literal_translation import generate_literal_translation
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


def translation_handler(event, _):
    body = json.loads(event.get('body'))
    sentence = body.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_translation(sentence)
        return ok(response.model_dump())
    except iso639.LanguageNotFoundError:
        return fail(ApplicationException(f"Language for sentence {sentence} could not be identified."), 400)


def response_suggestion_handler(event, _):
    body = json.loads(event.get('body'))
    sentence = body.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    response = generate_response_suggestions(sentence)
    return ok([r.model_dump() for r in response])


def literal_translation_handler(event, _):
    body = json.loads(event.get('body'))
    sentence = body.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    response = generate_literal_translation(sentence)
    return ok([r.model_dump() for r in response])


def ok(res: dict | list) -> dict:
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(res)
    }


def fail(e: ApplicationException, status: int) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(e.dict())
    }
