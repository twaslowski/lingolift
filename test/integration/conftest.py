import json
from test.mock_llm_adapter import MockLLMAdapter
from unittest.mock import patch

import pytest

from lingolift import lambda_handlers
from lingolift.generative.morphology_generator import MorphologyGenerator
from lingolift.lambda_context_container import ContextContainer
from lingolift.nlp.morphologizer import Morphologizer


@pytest.fixture
def mock_llm_adapter():
    return MockLLMAdapter()


@pytest.fixture
def context_container(mock_llm_adapter):
    context_container = ContextContainer(mock_llm_adapter)
    with patch.object(lambda_handlers, "context_container", context_container):
        yield context_container


@pytest.fixture
def morphology_generator(context_container) -> MorphologyGenerator:
    return context_container.morphology_generator


@pytest.fixture
def morphologizer(context_container) -> Morphologizer:
    return context_container.morphologizer


@pytest.fixture
def real_event():
    return {
        # one event for both lambdas; additional fields don't cause issues
        "body": json.dumps({"sentence": "This is a test.", "word": "test"})
    }


@pytest.fixture
def pre_warm_event():
    return {"body": json.dumps({"pre_warm": "true"})}


# @pytest.fixture
# def inflections():
#     return Inflections(
#         pos=PartOfSpeech(value="VERB", explanation=""), gender=None, inflections=[]
#     )
