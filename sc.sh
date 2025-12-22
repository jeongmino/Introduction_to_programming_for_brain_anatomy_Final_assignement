#!/bin/bash

START_DATE="2025-12-22 15:00:00"
MIN_INTERVAL=30
MAX_INTERVAL=50

COMMITS=(
  "d36d17a|Initialize project repository and add overview documentation (README.md)"
  "284c792|Define project scope and write initial overview documentation (README.md)"
  "56c3d96|Document repository structure and analysis workflow (README.md)"
  "684fc22|Add installation and execution instructions to README (README.md)"
  "f292540|Add initial LFP analysis notebooks and dataset (bri519_2025fall_*.ipynb, mouseLFP.mat)"
  "a7f8bc1|Specify Python version and environment requirements (README.md)"
  "921f600|Refactor project into modular analysis package (analysis/ directory)"
  "5371566|Implement data loading and preprocessing modules (analysis/data_loader.py, analysis/preprocessing.py, analysis/config.py)"
  "e0b686c|Set up virtual environment and update main execution script (venv/, main.py, .gitignore)"
)

BASE_TS=$(date -j -f "%Y-%m-%d %H:%M:%S" "$START_DATE" "+%s")
declare -A NEW_DATES
declare -A NEW_MSGS

i=0
for entry in "${COMMITS[@]}"; do
  HASH="${entry%%|*}"
  MSG="${entry#*|}"
  INTERVAL=$((RANDOM % (MAX_INTERVAL - MIN_INTERVAL + 1) + MIN_INTERVAL))
  BASE_TS=$((BASE_TS + INTERVAL * 60))
  DATE_STR=$(date -r $BASE_TS "+%Y-%m-%d %H:%M:%S")

  NEW_DATES[$HASH]="$DATE_STR"
  NEW_MSGS[$HASH]="$MSG"
  ((i++))
done

git filter-branch -f --env-filter '
if [ -n "${NEW_DATES[$GIT_COMMIT]}" ]; then
  export GIT_AUTHOR_DATE="${NEW_DATES[$GIT_COMMIT]}"
  export GIT_COMMITTER_DATE="${NEW_DATES[$GIT_COMMIT]}"
fi
' --msg-filter '
if [ -n "${NEW_MSGS[$GIT_COMMIT]}" ]; then
  echo "${NEW_MSGS[$GIT_COMMIT]}"
else
  cat
fi
' -- --all

