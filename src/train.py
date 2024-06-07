""" VectorDB 인코드 학습 코드 """

from typing import Optional, Literal
from dataclasses import dataclass, field
from copy import deepcopy
from pathlib import Path
import logging
import json
import os
import sys

import wandb
import datasets
from datasets import Dataset
import torch
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer
)
from sentence_transformers.losses import TripletLoss
from sentence_transformers.evaluation import TripletEvaluator
from transformers import HfArgumentParser

MODEL_ID = "intfloat/multilingual-e5-small"
# logger = logging.getLogger(__name__)
dir_path = Path(__file__).parent

def _getenv(key):
    """ 환경변수를 찾는 함수입니다. .env """
    load_dotenv(find_dotenv())
    return os.getenv(key)

class ModelArguments:
    """
    Model 호출 / Tokenizer 코드 
    """
    model_path: Optional[str] = field(default = MODEL_ID, metadata = {"help": "모델 Checkpoint, Default: intfloat/multilingual-e5-small"})
    torch_dtype: Optional[str] = field(default = torch.bfloat16, metadata = {"help": "모델 dtype 설정, Default: bf16"})
    device: Optional[str] = field(default = "cuda", metadata = {"help": "모델 device 설정, Default: cuda"})

class DataTrainingArguments:
    """
    데이터셋 생성, 학습 코드
    """
    dataset: Optional[str] = field(default = "./data/health.json", metadata = {"help": "학습에 사용할 데이터셋 위치, Default: ./data/health.json"})
    training_args: Optional[str] = field(default = "./training_args.json", metadata = {"help": "학습에 사용할 Configuration, Default: ./trainig_args.json"})


def check_dataset(data_type: Literal["train", "test"]):
    return (Path(dir_path) / f"data/{data_type}_dataset.json").exists()

def negative_sampling(example):
    bucket = [pos for pos in positive if pos != example['text']]
    neg = random.choice(bucket)
    return {"positive": example["text"], "negative": neg, "anchor": example["title"]}

def main():
    parser = HfArgumentParser((ModelArguments, DataArguments, TrainingArguments))
    
    if sys.argv[1] == "train_args.json":
        model_args, data_args, training_args = parser.parse_json_file(json_file = str(dir_path / sys.argv[1]))
    else:
        model_args, data_args, training_args = parser.parse_args_into_dataclasses()
        
    # log_level = training_args.get_process_log_lovel()
    # logger.setLevel(log_level)
    # datasets.utils.logging.set_verbosity(log_level)
    # transformers.utils.logging.set_verbosity(log_level)
    # transformers.utils.logging.enable_default_handler()
    # transformers.utils.logging.enable_explicit_format()

    
    # Dataset
    if (not check_dataset("train")) and (not check_dataset("test")):
        train_dataset_path = str(dir_path / "data/train_dataset.json")
        test_dataset_path = str(dir_path / "data/test_dataset.json")

        if not check_dataset("train"):
            train_dataset = load_dataset("json", data_file = train_dataset_path, split = "train")

        if not check_dataset("test"):
            test_dataset = load_dataset("json", data_file = test_dataset_path, split = "test")

    else:
        dataset = json.loads(Path(data_args.dataset).read_text())
        positive = [ele['text'] for ele in dataset]
        negative = deepcopy(positive)
        
        dataset = dataset.map(negative_sampling, remove_columns = ['title', 'text', 'url'])
        dataset = dataset.train_test_split(test_size = 0.1)
        train_dataset = dataset['train']
        test_dataset = dataset['test']

        train_dataset.to_json(train_dataset_path, force_ascii=False)
        test_dataset.to_json(test_dataset_path, force_ascii=False)

    # Model
    model = SentenceTransformer(model_args.model_path, torch_dtype = model_args.torch_dtype, device = model_args.device)

    # Train
    wandb.login(_getenv("WANDB_API_KEY"))
    loss = TripletLoss(model)
    args.hub_token =(_getenv("HF_WRITE_TOKEN"))
    train_parameters = dict(
        model=model,
        args=args,
        train_dataset=train_dataset,
        loss=loss
    )

    if traitraining_args.do_eval:
        evaluator = TripletEvaluator(
            anchor = test_dataset["anchor"],
            positive = test_dataset["positive"],
            negative = test_dataset["negative"],
            name = "health_encoder_test"
        )
        evaluator(model)
    
        train_parameters.update({"evaluator": evaluator})
    trainer = SentenceTransformerTrainer(**train_parameters)
    trainer.train()

main()
# python train.py training_args.json

        
    
