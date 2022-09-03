# CiteWorth including Section Information

## File Contents
In the following we only name the files that were modified or created by us.
Thereby, we retained the structure and architecture of the original repository.

`experiment_scripts/longformer-*`: shell scripts to run the Longformer model in the ctx variant, the solo variant, and for the domain evaluation experiments  
(longformer-ctx.sh and longformer-solo.sh by the original authors served as a basis for these scripts)

`experiment_scripts/randombaseline-*`: shell scripts to run the baselines for cite-worthiness detection  
(chance baseline &rarr; randombaseline-withoutweighting.sh, class-weighted baseline &rarr; randombaseline-withweighting.sh, class-weighted baseline with the section as a prior &rarr; randombaseline-section.sh)

`datareader.py`: entails the mapping from section headings to section types as defined by our structure analysis and adds the section type to the input of the model in one of the following variants: either first, always, or extra  
(for more detail on the input variants, we refer to Section 3.2 in our scientific report)

`domain_adaption_baselines.py`: provides a commandline interface to execute the domain evaluation experiments and was modified by us in order to allow for multiple training domains

`metrics.py`: this file was only modified in order to make the original implementation runnable

`model.py`: implements the randombaseline as an instantiable class and we modified the AutoTransformerForSentenceSequenceModeling model (i.e., the model instantiated when utilizing a Longformer model for the cite-worthiness detection) in order to be able to treat the section-extra variant properly since in this case not all [SEP] tokens are forwarded to the classification model  

`neural_baselines.py`: provides a commandline interface to execute (among others) the longformer-ctx and longformer-solo experiments and was modified by us such that section information can be added in any of the three variants, evaluation metrics are stored in a file, and evaluation over multiple test datasets is possible

`random_baselines.py`: implemented by us and provides a commandline interface to execute the baseline experiments

## Running the Experiments
Place the S2ORC_CiteWorth dataset into the `experiments/data` directory and set up the environment as described in the README of the parent directory.
If you do not want to use wandb logging, run `wandb off` in this `experiments` directory.

You can then execute any of the experiment scripts via `./<script-name>.sh`.
Perform the execution in the `experiments/experiment_scripts` directory.  
Alternatively, you can also perform experiments by running the respective python file with `python <neural/random/domain_adaption>_baselines.py` and adding the commandline arguments.
Perform the execution in this `experiments` directory.

The trained models and the calculated evaluation metrics are saved in the `experiments/<output_dir>/` or `experiments/<output_dir>/files` directory per chosen random seed.
In case of the experiment scripts, the `output_dir` is `models/<exp_name>`.
