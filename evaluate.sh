#!/usr/bin/env sh

# check if data directory was provided
if [ -z "$1" ]
then
  echo "Usage: ./evaluate.sh <data-dir>"
  exit 1
fi

set -eu

DATA_DIR=$1

# install dependencies
uv sync

# capture pinned spacy version (--no-sync: don't let uv restore the lockfile version later)
PINNED=$(uv run --no-sync python -c "import spacy; print(spacy.__version__)" 2>/dev/null)

# run evaluation for the pinned and the latest spacy version
eval_models() {
  for MODEL_SIZE in sm md lg
  do
    MODEL_NAME="de_core_news_$MODEL_SIZE"

    # download spacy model
    uv run --no-sync python -m spacy download "$MODEL_NAME" --quiet >/dev/null

    # run evaluation

    # 1. line-based (default settings)
    HIT_RATE=$(uv run --no-sync python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME")
    printf '%s\tline-based\t%s\t%s\t\n' "$1" "$MODEL_SIZE" "$HIT_RATE"

    # 2. text-based
    HIT_RATE=$(uv run --no-sync python -m tests.evaluate_sentence_splitter "$DATA_DIR" --spacy-model "$MODEL_NAME" --no-split-on-line-breaks --max-len 0)
    printf '%s\ttext-based\t%s\t%s\t\n' "$1" "$MODEL_SIZE" "$HIT_RATE"
  done
}

eval_models "$PINNED"

# install latest spacy into the venv only (no lock change, models stay)
uv pip install -U spacy >/dev/null
LATEST=$(uv run --no-sync python -c "import spacy; print(spacy.__version__)" 2>/dev/null)
eval_models "$LATEST"

# revert to the pinned spacy version (uv pip keeps the models, no --sync)
uv pip install "spacy==$PINNED" >/dev/null
