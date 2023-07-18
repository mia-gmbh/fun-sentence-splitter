#!/usr/bin/env sh

# check if data directory was provided
if [ -z "$1" ]
  then
    echo "Usage: ./evaluate.sh <data-dir>"
    exit 1
fi

DATA_DIR=$1

# guard against local changes
git diff-index --quiet HEAD -- || { echo "Please commit your changes before running the evaluation." && exit 1; }

# install dependencies
poetry install --quiet

for i in current latest
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
    HIT_RATE=$(python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME" --no-split-on-line-breaks)
    printf '%s\ttext-based\t%s\t%s\t\n' "$SPACY_VERSION" "$MODEL_SIZE" "$HIT_RATE"
  done

  # don't update spacy model again if we're already on the latest version
  [ $i = "latest" ] && break

  # update spacy model
  poetry add spacy@latest --quiet
done
