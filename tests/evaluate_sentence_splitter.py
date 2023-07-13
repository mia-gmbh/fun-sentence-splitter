import re
from collections.abc import Generator
from pathlib import Path

import spacy
import typer
from tqdm import tqdm

from fun_sentence_splitter.sentence_splitter import Span, init

WHITE_SPACE = re.compile(r"\s+")


def main(data_dir: Path, max_len: int = 100, spacy_model: str = "de_core_news_sm") -> None:
    sentence_splitter = init(
        max_len_before_split=max_len,
        spacy_model=spacy_model,
    )

    split_files = list(data_dir.glob("*.split"))
    overall_gold_spans_count = 0
    overall_overlap = 0
    for split_file in tqdm(split_files):
        text_file = split_file.with_suffix(".txt")

        gold_spans = frozenset(_find_spans(text_file=text_file, split_file=split_file))
        gold_spans_count = len(gold_spans)
        test_spans = frozenset(sentence.span for sentence in sentence_splitter(text_file.read_text()))

        overlap = len(gold_spans & test_spans)  # TODO TD: allow for partial overlap

        print(
            f"{split_file.name}:"
            f" gold standard: {gold_spans_count},"
            f" overlap={overlap},"
            f" hit rate={_hit_rate(overlap, gold_spans_count):.5}",
        )

        overall_overlap += overlap
        overall_gold_spans_count += gold_spans_count

    hit_rate = _hit_rate(overall_overlap, overall_gold_spans_count)

    print(f"\n{80 * '-'}")
    print(f"span hit rate using spacy {spacy_model}@{spacy.__version__}: {hit_rate:.5}"
          f" ({overall_gold_spans_count} spans from {len(split_files)} files)")
    print(f"{80 * '-'}\n")


def _find_spans(text_file: Path, split_file: Path) -> Generator[Span, None, None]:
    if not text_file.exists():
        print(f"ERROR - File {text_file} not found")
        return

    if not split_file.exists():
        print(f"ERROR - File {split_file} not found")
        return

    full_text = text_file.read_text()
    stop_idx = 0
    with split_file.open() as f:
        for sentence in f.read().splitlines():
            # replace all spaces with regex pattern
            tmp = WHITE_SPACE.sub(r" ", sentence).strip()
            tmp = re.escape(tmp)
            tmp = tmp.replace(r"\ ", r"\s+")
            re_sentence = re.compile(tmp)
            match = re_sentence.search(full_text, stop_idx)
            if not match:
                print(f'ERROR - Could not "{re_sentence.pattern}" after {stop_idx} in {text_file}')
                continue
            start_idx, stop_idx = match.start(), match.end()
            yield start_idx, stop_idx


def _hit_rate(overlap: int, spans_count: int) -> float:
    return overlap / spans_count if spans_count else 0


if __name__ == "__main__":
    typer.run(main)
