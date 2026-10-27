#!/usr/bin/env bash
# rerun.sh: run the same saved prompt N times and keep every answer, for a fair "is it worse today?" check.
# Usage: ./rerun.sh prompt.txt [runs] [model]
#   ./rerun.sh my-task.txt 5 claude-opus-5-5
# Needs the Claude Code CLI (`claude`) logged in. Each answer is saved as JSON (the answer text is in .result; the
# model that actually answered is listed under .modelUsage). Nothing is sent anywhere else.
set -euo pipefail

PROMPT_FILE="${1:?usage: ./rerun.sh prompt.txt [runs] [model]}"
RUNS="${2:-5}"
MODEL="${3:-claude-opus-5-5}"
OUT="runs/$(date +%Y-%m-%d_%H%M)"
mkdir -p "$OUT"
cp "$PROMPT_FILE" "$OUT/prompt.txt"
echo "model=$MODEL runs=$RUNS started=$(date -Iseconds)" > "$OUT/meta.txt"

for i in $(seq 1 "$RUNS"); do
  t0=$(date +%s)
  # Same prompt, same model, no conversation history: only the model's answer can change between runs.
  claude -p --model "$MODEL" --output-format json < "$PROMPT_FILE" > "$OUT/run-$i.json"
  echo "run $i: $(( $(date +%s) - t0 ))s"
done

echo "saved $RUNS answers in $OUT"
echo "answer text only:  for f in $OUT/run-*.json; do jq -r .result \"\$f\" > \"\${f%.json}.txt\"; done"
