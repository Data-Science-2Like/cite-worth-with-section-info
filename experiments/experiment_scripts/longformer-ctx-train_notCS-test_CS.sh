#!/bin/bash
. activate scientific-citation-detection

cd ..
run_name="longformer-ctx-train_all-test_CS"
tag="citeworth-with-section-info"
model_dir=models/longformer-ctx-train_all-test_CS
python domain_adaptation_baselines.py \
  --train_data data/train.jsonl \
  --validation_data data/dev.jsonl \
  --test_data data/test.jsonl \
  --run_name "${run_name}" \
  --tag "${tag}" \
  --model_name allenai/longformer-base-4096 \
  --model_dir ${model_dir} \
  --balance_class_weight \
  --n_gpu 1 \
  --batch_size 4 \
  --learning_rate 0.00001112 \
  --warmup_steps 300 \
  --weight_decay 0.0 \
  --n_epochs 3 \
  --seed 1000 \
  --sequence_model \
  --train_domain "Biology" "Medicine" "Engineering" "Chemistry" "Psychology" "Materials Science" "Economics" "Mathematics" "Physics" \
  --test_domain "Computer Science"
