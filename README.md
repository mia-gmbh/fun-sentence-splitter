# Fun Sentence Splitter

A fundamental sentence splitter based on [spacy](https://spacy.io/).

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
