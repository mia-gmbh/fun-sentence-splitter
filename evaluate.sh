#!/usr/bin/env sh

# check if data directory was provided
if [ -z "$1" ]
then
  echo "Usage: ./evaluate.sh <data-dir>"
  exit 1
fi

DATA_DIR=$1

# guard against local changes
# git diff-index --quiet HEAD -- || { echo "Please commit your changes before running the evaluation." && exit 1; }

# install dependencies
poetry install --quiet

# run evaluation for current and latest spacy version
for INSTALL_LATEST_SPACY in yes no
do
  SPACY_VERSION=$(poetry run spacy info 2>/dev/null | grep 'spaCy version' | awk '{print $3}')

  for MODEL_SIZE in sm md lg
  do
    MODEL_NAME="de_core_news_$MODEL_SIZE"

    # download spacy model
    poetry run spacy download $MODEL_NAME --quiet >/dev/null

    # run evaluation

    # 1. line-based (default settings)
    HIT_RATE=$(python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME")
    printf '%s\tline-based\t%s\t%s\t\n' "$SPACY_VERSION" "$MODEL_SIZE" "$HIT_RATE"

    # 2. text-based
    HIT_RATE=$(python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME" --no-split-on-line-breaks --max-len 0)
    printf '%s\ttext-based\t%s\t%s\t\n' "$SPACY_VERSION" "$MODEL_SIZE" "$HIT_RATE"
  done

  if [ $INSTALL_LATEST_SPACY = "yes" ]
  then
    # install latest spacy version & evaluate in next iteration
    poetry add spacy@latest --quiet
  fi
done

# restore old version + delete downloaded models of latest version
git restore pyproject.toml poetry.lock
poetry install --sync --quiet
