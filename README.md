# Fun Sentence Splitter

A fundamental sentence splitter based on [spacy](https://spacy.io/).

## Requirements

Python 3.10 or higher and [poetry](https://python-poetry.org).

## Local Dev Setup

Download the Spacy language model used in the tests:

```shell
python -m spacy download de_core_news_sm
```

Run static checks and tests:

```shell
ruff .
mypy .
pytest --cov=fun_sentence_splitter
```

## Run Evaluation

1. Change the `spacy` dependency in the `pyproject.toml` to the version you want to evaluate and run:

    ```shell
    poetry lock --no-update
    poetry install
    ```

2. Download the Spacy language model you want to evaluate, e.g.:

    ```shell
    python -m spacy download de_core_news_lg
    ```

Evaluate:

```shell
python -m tests.evaluate_sentence_splitter path/to/splits_dir [--spacy-model de_core_news_lg] [--max-len 47]
```

`path/to/splits_dir`: directory containing pairs of *.split and *.txt files. .split files contain the expected
sentences, each on a separate line. .txt files contain the original text to split.

`--spacy-model`: name or location of the spacy language model. Optional, defaults to `de_core_news_sm`.

`--max-len`: maximum line length before before spacy is used. Optional, defaults to `100`.
