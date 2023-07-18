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

```shell
./evaluate.sh path/to/splits_dir
```

`path/to/splits_dir`: directory containing pairs of *.split and *.txt files. .split files contain the expected
sentences, each on a separate line. .txt files contain the original text to split.

The evaluation script will automatically update the spacy dependency and download the required language models.
