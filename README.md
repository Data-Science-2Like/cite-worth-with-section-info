# CiteWorth including Section Information
This implementation is based on
```
@inproceedings{wright2021citeworth,
    title={{CiteWorth: Cite-Worthiness Detection for Improved Scientific Document Understanding}},
    author={Dustin Wright and Isabelle Augenstein},
    booktitle = {Findings of ACL-IJCNLP},
    publisher = {Association for Computational Linguistics},
    year = 2021
}
```
by forking the original repository by Dustin Wright and Isabelle Augenstein: https://github.com/copenlu/cite-worth

We experiment with additionally including the section information as an input to the cite-worthiness classification.

The following README is written by Dustin Wright and Isabelle Augenstein with slight modifications to make clear that these parts are their and not our contribution.  
Please, see the README written by us in the `experiments` directory for details on our contribution.

## Getting the data
The CiteWorth data is available in the HuggingFace dataset hub at [copenlu/citeworth](https://huggingface.co/datasets/copenlu/citeworth). As such, load the dataset as follows:

```
from datasets import load_dataset

dataset = load_dataset('copenlu/citeworth')
```

Alternatively, the CiteWorth data is available for download via this link: [https://drive.google.com/drive/folders/1j4B1rQFjjqnRzKsf15ur2\_rCaBh5TJKD?usp=sharing](https://drive.google.com/drive/folders/1j4B1rQFjjqnRzKsf15ur2\_rCaBh5TJKD?usp=sharing)

The data is derived from the [S2ORC dataset](https://github.com/allenai/s2orc), specifically the 20200705v1 release of the data. It is licensed under the [CC By-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) license.   

The data is licensed under the [CC By-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) license.  
The code is licensed under the MIT license.

### Dataset Structure

The data is structured as a json lines file, where each line contains a full paragraph of data. The fields in the json are as follows
 - `paper_id`: The S2ORC paper ID where the paragraph comes from
 - `section_idx`: An index into the section array in the original S2ORC data
 - `file_index`: The volume in the S2ORC dataset that the paper belongs to
 - `file_offset`: Byte offset to the start of the paper json in the S2ORC paper PDF file
 - `mag_field_of_study`: The field of study to which a paper belongs (an array, but each paper belongs to a single field)
 - `original_text`: The original text of the paragraph
 - `section_title`: Title of the section to which the paragraph belongs
 - `samples`: An array containing dicts of the cleaned sentences for the paragraph, in order. The fields for each dict are as follows
   - `text`: The cleaned text for the sentence
   - `label`: Label for the sentence, either `check-worthy` for cite-worthy sentences or `non-check-worthy` non-cite-worthy sentences
   - `original_text`: The original sentence text
   - `ref_ids`: List of the reference IDs in the S2ORC dataset for papers cited in this sentence
   - `citation_text`: List of all citation text in this sentence

## Pretrained models
Dustin Wright and Isabelle Augenstein released two pretrained models from their paper ["CiteWorth: Cite-Worthiness Detection for Improved Scientific Document Understanding"](https://arxiv.org/abs/2105.10912), available in the [HuggingFace model hub](https://huggingface.co/copenlu). The two models are:
 - `copenlu/citebert`: SciBERT trained on citation detection and masked language modeling from CiteWorth data
 - `copenlu/citebert-cite-only`: SciBERT trained on citation detection only from CiteWorth data

## Environment setup
It is recommended to use Anaconda to create your environment. After installing conda, run the following to create the environment.
```[bash]
$ conda env create -f environment.yml python=3.8
$ conda activate citeworth
$ python -m spacy download en_core_web_sm
$ pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz   
``` 

## Building a dataset from scratch
Dustin Wright and Isabelle Augenstein have released the code to build a dataset using the same filtering and cleaning as CiteWorth in the `dataset_creation` directory. To do so, do the following:

First, download the [S2ORC dataset](https://github.com/allenai/s2orc) and place it in `dataset_creation/data/s2orc_full`. Then, run the following commands:
```[bash]
$ cd dataset_creation
$ python filter_papers_full.py
$ python get_filtered_pdf_line_offsets.py
$ python build_dataset.py
```

Filtering the data may take a while depending on your computing infrastructure. You should then have a file `dataset_creation/data/citation_needed_data_contextualized_with_removal_v1.jsonl`. 


## Running experiments
The code for the experiments can be found under `experiments`. To run them, first create a directory `experiments/data` and place all of the CiteWorth data in this directory. Then, go to `experiments/experiment_scripts` and run any of the experiments given there.

[Weights and Biases](https://wandb.ai/site) is used to log the experiments. If you do not have/do not wish to use wandb, run the following in the `experiments` directory before executing any of the scripts:
```
$ wandb off
```


## Citing
Please use the following citation when referencing the work by Dustin Wright and Isabelle Augenstein or when using the CiteWorth data:

```
@inproceedings{wright2021citeworth,
    title={{CiteWorth: Cite-Worthiness Detection for Improved Scientific Document Understanding}},
    author={Dustin Wright and Isabelle Augenstein},
    booktitle = {Findings of ACL-IJCNLP},
    publisher = {Association for Computational Linguistics},
    year = 2021
}
```
