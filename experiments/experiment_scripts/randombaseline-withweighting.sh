#!/bin/bash
. activate scientific-citation-detection

cd ..
run_name="randombaseline-withweighting"
tag="citeworth-baseline"
output_dir=models/randombaseline-withweighting
python random_baselines.py \
  --train_data data/train.jsonl \
  --test_data data/test_conform.jsonl data/test_non_conform.jsonl data/test.jsonl \
  --run_name "${run_name}" \
  --tag "${tag}" \
  --output_dir ${output_dir} \
  --seed 1000 \
  --balance_class_weight

