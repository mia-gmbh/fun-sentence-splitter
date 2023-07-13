from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import spacy
from spacy.attrs import ORTH  # type: ignore[import]

Span = tuple[int, int]  # start and end index (exclusive)


@dataclass(frozen=True)
class Sentence:
    """A sentence from a document, with text, start and end index."""
    text: str
    span: Span


SentenceSplitter = Callable[[str], list[Sentence]]


def init(  # noqa: C901  # the price for hiding stuff inside a closure
        *,
        spacy_model: str | Path,
        abbreviations: Iterable[str] = frozenset(),
        always_split_on_line_breaks: bool = False,
        max_len_before_split: int = 0,
) -> SentenceSplitter:
    """Initialize a new sentence splitter function.

    :param spacy_model: The spacy model to use for sentence splitting, e.g. "en_core_web_sm". Can be a path to a model.
    :param abbreviations: Optional abbreviations to add to the spacy tokenizer
    :param always_split_on_line_breaks: Optionally split the text on newlines _before_ sentence splitting is applied
    :param max_len_before_split: Optional maximum length of a line before sentence splitting is applied.
        Only valid in combination with always_split_on_line_breaks=True.
    :return: A sentence splitter function
    """
    # input validation
    if not always_split_on_line_breaks and max_len_before_split > 0:
        raise ValueError("parameter max_len_before_split is only valid in combination with always_split_on_line_breaks=True")  # noqa: E501

    nlp = spacy.load(spacy_model)

    for abbrev in abbreviations:
        nlp.tokenizer.add_special_case(abbrev, [{ORTH: abbrev}])  # type: ignore[union-attr]

    @lru_cache(maxsize=100)
    def apply(text: str) -> list[Sentence]:
        """The actual sentence splitter. Splits a text into sentences."""
        sentences: list[Sentence] = []
        if always_split_on_line_breaks:
            add_line_based_splits(sentences, text)
        else:
            add_text_split(sentences, text)
        return sentences

    def add_line_based_splits(sentences: list[Sentence], text: str) -> None:
        cur_idx = 0
        for line in text.splitlines(keepends=True):  # 1. text is always split at line breaks
            if len(line) < max_len_before_split:  # 2. if a line is short enough, it is added as a sentence
                cur_idx += add_line_split(cur_idx, line, sentences)
            else:
                for sentence in nlp(line).sents:  # 3. else, it is split using spacy
                    cur_idx += add_line_split(cur_idx, sentence.text_with_ws, sentences)

    def add_text_split(sentences: list[Sentence], text: str) -> None:
        cur_idx = 0
        for sentence in nlp(text).sents:
            cur_idx += add_line_split(cur_idx, sentence.text_with_ws, sentences)

    def add_line_split(cur_idx: int, line: str, sentences: list[Sentence]) -> int:
        line_length = len(line)
        if stripped_text := line.strip():
            # sentence starts after leading whitespace
            start_idx = cur_idx + line_length - len(line.lstrip())
            # sentence ends before trailing whitespace
            end_idx = start_idx + len(stripped_text)
            sentences.append(Sentence(text=stripped_text, span=(start_idx, end_idx)))
        return line_length

    return apply
