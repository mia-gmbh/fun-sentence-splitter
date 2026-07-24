# Fun Sentence Splitter

A fundamental sentence splitter based on [spacy](https://spacy.io/).

## Usage

```python
from fun_sentence_splitter import init

splitter = init(spacy_model="de_core_news_sm")

for sentence in splitter("Das ist ein Satz. Und hier noch einer!"):
    print(sentence.text, sentence.span)
```

`init(...)` returns a splitter function. Each `Sentence` exposes `.text` and `.span` (a `(start, end)` index pair into the original text).

Split on line breaks first (e.g. for structured documents) and only run spaCy on longer lines:

```python
splitter = init(
    spacy_model="de_core_news_sm",
    always_split_on_line_breaks=True,
    max_len_before_split=100,
)
```

> Download the language model once: `uv run python -m spacy download de_core_news_sm`

## Requirements

[uv](https://docs.astral.sh/uv/).

## Local Dev Setup

Install dependencies and download the Spacy language model used in the tests:

```shell
uv sync
uv run python -m spacy download de_core_news_sm
```

Run static checks and tests:

```shell
uv run ruff check .
uv run mypy .
uv run pytest --cov=fun_sentence_splitter
```

## Run Evaluation

```shell
./evaluate.sh path/to/splits_dir
```

`path/to/splits_dir`: directory containing pairs of *.split and *.txt files. .split files contain the expected
sentences, each on a separate line. .txt files contain the original text to split.

The evaluation script will automatically update the spacy dependency and download the required language models.
