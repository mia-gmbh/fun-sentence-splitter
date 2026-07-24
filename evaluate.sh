#!/usr/bin/env sh

# check if data directory was provided
if [ -z "$1" ]
then
  echo "Usage: ./evaluate.sh <data-dir>"
  exit 1
fi

DATA_DIR=$1

# install dependencies
uv sync

# capture pinned spacy version
PINNED=$(uv run python -c "import spacy; print(spacy.__version__)" 2>/dev/null)

# run evaluation for the pinned and the latest spacy version
for LABEL in pinned latest
do
  if [ "$LABEL" = "latest" ]
  then
    # install latest spacy into the venv only (no lock change, models stay)
    uv pip install -U spacy >/dev/null
    SPACY_VERSION=$(uv run python -c "import spacy; print(spacy.__version__)" 2>/dev/null)
  else
    SPACY_VERSION=$PINNED
  fi

  for MODEL_SIZE in sm md lg
  do
    MODEL_NAME="de_core_news_$MODEL_SIZE"

    # download spacy model
    uv run python -m spacy download $MODEL_NAME --quiet >/dev/null

    # run evaluation

    # 1. line-based (default settings)
    HIT_RATE=$(uv run python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME")
    printf '%s\tline-based\t%s\t%s\t\n' "$SPACY_VERSION" "$MODEL_SIZE" "$HIT_RATE"

    # 2. text-based
    HIT_RATE=$(uv run python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME" --no-split-on-line-breaks --max-len 0)
    printf '%s\ttext-based\t%s\t%s\t\n' "$SPACY_VERSION" "$MODEL_SIZE" "$HIT_RATE"
  done
done

# revert to the pinned spacy version (uv pip install keeps the models, no --sync)
uv pip install "spacy==$PINNED" >/dev/null
