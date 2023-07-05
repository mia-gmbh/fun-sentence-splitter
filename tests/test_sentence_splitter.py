import pytest

from sentencesplitter.sentence_splitter import Sentence, SentenceSplitter, init


@pytest.fixture(scope="module")
def cut() -> SentenceSplitter:
    return init(spacy_model="de_core_news_sm")


def test_should_split_text_into_2_sentences(cut: SentenceSplitter) -> None:
    text = "Das ist ein Test. Das ist ein weiterer Test."
    actual_sentences = list(cut(text))
    expected_sentences = [
        Sentence(
            text="Das ist ein Test.",
            span=(0, 17),
        ),
        Sentence(
            text="Das ist ein weiterer Test.",
            span=(18, 44),
        ),
    ]

    assert actual_sentences == expected_sentences


def test_should_split_text_into_3_sentences(cut: SentenceSplitter) -> None:
    text = "Wir diagnostizierten bei der Patientin A00. Auch A01 wurde später gefunden. Ansonsten ging es ihr gut"
    actual_sentences = list(cut(text))
    expected_sentences = [
        Sentence(
            text="Wir diagnostizierten bei der Patientin A00.",
            span=(0, 43),
        ),
        Sentence(
            text="Auch A01 wurde später gefunden.",
            span=(44, 75),
        ),
        Sentence(
            text="Ansonsten ging es ihr gut",
            span=(76, 101),
        ),
    ]

    assert actual_sentences == expected_sentences


def test_should_trim_left_whitespace(cut: SentenceSplitter) -> None:
    texts = [
        "Dies ist ein Satz ohne führende Leerzeichen.",  # len: 44)
        " Dies ist ein Satz mit einem führenden Leerzeichen.",  # len: 51)
        "  Dies ist ein Satz mit zwei führenden Leerzeichen.",  # len: 51)
        "   Dies ist ein Satz mit drei führenden Leerzeichen.",  # len: 52)
        "    Dies ist ein Satz mit vier führenden Leerzeichen.",  # len: 53)
    ]
    actual_sentences = [cut(text) for text in texts]
    expected_sentences = [
        [Sentence(text="Dies ist ein Satz ohne führende Leerzeichen.", span=(0, 44))],
        [Sentence(text="Dies ist ein Satz mit einem führenden Leerzeichen.", span=(1, 51))],
        [Sentence(text="Dies ist ein Satz mit zwei führenden Leerzeichen.", span=(2, 51))],
        [Sentence(text="Dies ist ein Satz mit drei führenden Leerzeichen.", span=(3, 52))],
        [Sentence(text="Dies ist ein Satz mit vier führenden Leerzeichen.", span=(4, 53))],
    ]
    assert actual_sentences == expected_sentences


def test_should_trim_right_whitespace(cut: SentenceSplitter) -> None:
    texts = [
        "Dies ist ein Satz ohne nachfolgendes Leerzeichen.",  # len: 49
        "Dies ist ein Satz mit einem nachfolgenden Leerzeichen. ",  # len: 54
        "Dies ist ein Satz mit zwei nachfolgenden Leerzeichen.  ",  # len: 53
        "Dies ist ein Satz mit drei nachfolgenden Leerzeichen.   ",  # len: 53
        "Dies ist ein Satz mit vier nachfolgenden Leerzeichen.    ",  # len: 53
    ]
    actual_sentences = [cut(text) for text in texts]
    expected_sentences = [
        [Sentence(text="Dies ist ein Satz ohne nachfolgendes Leerzeichen.", span=(0, 49))],
        [Sentence(text="Dies ist ein Satz mit einem nachfolgenden Leerzeichen.", span=(0, 54))],
        [Sentence(text="Dies ist ein Satz mit zwei nachfolgenden Leerzeichen.", span=(0, 53))],
        [Sentence(text="Dies ist ein Satz mit drei nachfolgenden Leerzeichen.", span=(0, 53))],
        [Sentence(text="Dies ist ein Satz mit vier nachfolgenden Leerzeichen.", span=(0, 53))],
    ]
    assert actual_sentences == expected_sentences


def test_should_trim_surrounding_whitespace(cut: SentenceSplitter) -> None:
    text = (
        "Dies ist ein Satz ohne Leerzeichen zu Beginn und Ende."  # (0, 54)
        " Dies ist ein Satz mit einem Leerzeichen zu Beginn und Ende. "  # (54, 115)
        "  Dies ist ein Satz mit zwei Leerzeichen zu Beginn und Ende.  "  # (115, 177)
        "   Dies ist ein Satz mit drei Leerzeichen zu Beginn und Ende.   "  # (177, 241)
        "    Dies ist ein Satz mit vier Leerzeichen zu Beginn und Ende.    "  # (241, 307)
    )
    actual_sentences = cut(text)
    expected_sentences = [
        Sentence(text="Dies ist ein Satz ohne Leerzeichen zu Beginn und Ende.", span=(0, 54)),
        Sentence(text="Dies ist ein Satz mit einem Leerzeichen zu Beginn und Ende.", span=(55, 114)),
        Sentence(text="Dies ist ein Satz mit zwei Leerzeichen zu Beginn und Ende.", span=(117, 175)),
        Sentence(text="Dies ist ein Satz mit drei Leerzeichen zu Beginn und Ende.", span=(180, 238)),
        Sentence(text="Dies ist ein Satz mit vier Leerzeichen zu Beginn und Ende.", span=(245, 303)),
    ]
    assert actual_sentences == expected_sentences
