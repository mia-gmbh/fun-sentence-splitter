# Fun Sentence Splitter

A fundamental sentence splitter based on spacy.

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
