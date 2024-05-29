import pytest

from lingolift.nlp.syntactical_analysis import perform_analysis


@pytest.mark.skip("Mocking broken. Fix via dependency injection.")
def test_happy_path(mocker):
    mocker.patch(
        "lingolift.nlp.syntactical_analysis.llm_detect_language", return_value="DE"
    )
    # Perform one comprehensive test, because analyses are quite slow.
    sentence = "Satzzeichen werden nicht gezählt."
    result = list(perform_analysis(sentence))

    # ensure punctuation tokens are omitted from the analysis
    assert len(result) == 4

    assert result[0].pos.value == "NOUN"
    assert result[1].pos.value == "AUX"
    assert result[1].morphology.explanation == "3rd person Plural Present tense"
    assert result[3].pos.value == "VERB"
