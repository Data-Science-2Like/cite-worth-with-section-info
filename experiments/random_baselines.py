import argparse
import os
import random

import numpy as np
import torch

import wandb
from datareader import TransformerSingleSentenceDataset
from model import RandomBaseline


def enforce_reproducibility(seed=1000):
    # Sets seed manually for both CPU and CUDA
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # For atomic operations there is currently
    # no simple way to enforce determinism, as
    # the order of parallel operations is not known.
    # CUDNN
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # System based
    random.seed(seed)
    np.random.seed(seed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_data", help="Location of the training data", required=True, type=str)
    parser.add_argument("--test_data", help="Location of the test data", required=True, type=str, nargs='+')
    parser.add_argument("--run_name", help="A name for this run", required=True, type=str)
    parser.add_argument("--output_dir", help="Top level directory to save the evaluation metrics", required=True, type=str)
    parser.add_argument("--tag", help="A tag to give this run (for wandb)", required=True, type=str)
    parser.add_argument("--seed", type=int, help="Random seed", default=1000)
    parser.add_argument("--balance_class_weight", action="store_true", default=False,
                        help="Whether or not to use balanced class weights")
    parser.add_argument("--use_section_info",
                        help="Whether use the section information as an input for the prediction",
                        action="store_true", default=False)

    args = parser.parse_args()

    seed = args.seed
    num_labels = 2

    config = {
        "seed": seed,
        "balance_class_weight": args.balance_class_weight,
        "use_section_info": args.use_section_info
    }

    # Always first
    enforce_reproducibility(seed)

    train_data_loc = args.train_data
    test_data_locs = args.test_data

    DatareaderClass = TransformerSingleSentenceDataset
    model = RandomBaseline(args.balance_class_weight, args.use_section_info)

    train_dset = DatareaderClass(train_data_loc, None, use_section_info=args.use_section_info)

    # wandb initialization
    run = wandb.init(
        project="scientific-citation-detection",
        name=args.run_name,
        config=config,
        reinit=True,
        tags=args.tag
    )

    # Train it
    model.train(train_dset)

    for test_data_loc in test_data_locs:
        test_dset = DatareaderClass(test_data_loc, None, use_section_info=args.use_section_info)
        acc, P, R, F1 = model.evaluate(test_dset)
        wandb.run.summary[f'test-acc'] = acc
        wandb.run.summary[f'test-P'] = P
        wandb.run.summary[f'test-R'] = R
        wandb.run.summary[f'test-F1'] = F1
        wandb.run.summary[f'model one_threshold'] = model.one_threshold
        wandb.run.summary[f'model one_section_thresholds'] = model.one_section_thresholds
        os.makedirs(args.output_dir, exist_ok=True)
        with open(args.output_dir + '/' + (test_data_loc.split('/')[-1]).split('.')[0] + "_seed" + str(seed) + ".txt", 'w') as out:
            out.write("test_acc = {}\n".format(str(acc)))
            out.write("test_P = {}\n".format(str(P)))
            out.write("test_R = {}\n".format(str(R)))
            out.write("test_F1 = {}\n".format(str(F1)))
            out.write("model_one_threshold = {}\n".format(str(model.one_threshold)))
            out.write("model_one_section_threshold = {}\n".format(str(model.one_section_thresholds)))
