#!/usr/bin/env bash
# MinerU 双模式 OCR：pipeline（校对底稿，无幻觉）+ vlm（复杂版式交叉比对）
# 用法：make ocr 或 bash scripts/ocr.sh [PDF路径]
# 断点续跑：已存在且非空的分片自动跳过
set -euo pipefail
cd "$(dirname "$0")/.."

PDF="${1:-source/中国近现代史.pdf}"
CHUNK=100
TOTAL=$(mdls -name kMDItemNumberOfPages -raw "$PDF")

for model in pipeline vlm; do
  out="ocr/$model"
  mkdir -p "$out"
  start=1
  while [ "$start" -le "$TOTAL" ]; do
    end=$((start + CHUNK - 1))
    [ "$end" -gt "$TOTAL" ] && end=$TOTAL
    f="$out/pages-$(printf '%03d' "$start")-$(printf '%03d' "$end").md"
    if [ -s "$f" ]; then
      echo "跳过 $model $start-$end（已存在）"
    else
      echo "== $model 第 $start-$end 页 =="
      mineru-open-api extract "$PDF" --model "$model" --ocr \
        --pages "$start-$end" -f md -o "$f" --timeout 1800
    fi
    start=$((end + 1))
  done
done

echo "OCR 完成：ocr/pipeline/（底稿）、ocr/vlm/（交叉比对）"
