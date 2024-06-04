import torch
from torch.nn import functional as F
from typing import Union, List, Iterable
from transformers import AutoTokenizer, AutoModel
import transformers
from functools import partial

def _infer_device() -> str:
    """ device 자동설정 https://github.com/huggingface/peft/blob/6f41990da482dba96287da64a3c7d3c441e95e23/src/peft/utils/other.py#L75"""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    elif mlu_available:
        return "mlu"
    elif is_xpu_available():
        return "xpu"
    elif is_npu_available():
        return "npu"
    return "cpu"

def _call_default_model(device: str = None):
    """ default 모델 호출 코드를 별도로 작성"""
    if not device:
        device =_infer_device()
    model_id = "intfloat/multilingual-e5-small"
    model = AutoModel.from_pretrained(model_id, device_map=device)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    return model, tokenizer

def inference(
        input_text: Union[List[str], str],
        model: transformers.PreTrainedModel = None,
        tokenizer: transformers.PreTrainedTokenizer = None,
        device: str = None
) -> torch.Tensor:
    """인퍼런스"""
    
    if (not model) or (not tokenizer):
        model, tokenizer = _call_default_model(device=device)

    inputs = tokenizer(
        input_text,
        max_length=tokenizer.model_max_length,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(model.device)
    
    output = model(**inputs)
    last_hidden = output.last_hidden_state.masked_fill(~inputs['attention_mask'][..., None].bool(), 0.0).to("cpu")
    return last_hidden
    

def average_pool(
        input_text: Union[List[str], str],
        model: transformers.PreTrainedModel = None,
        tokenizer: transformers.PreTrainedTokenizer = None,
        device: str = None
) -> torch.Tensor:
    """Input으로 받는 문장 내 여러 토큰들을 Average Pool을 사용해서 하나의 임베딩 값으로 변환해줍니다..

    Args:
        input_text: 임베딩될 문장 또는 문장의 리스트
        model: 임베딩을 수행할 모델 (default: intfloat/multilingual-e5-base)
        tokenizer: 모델의 토크나이저 (default: intfloat/multilingual-e5-base)
        device: 모델의 device 설정

    Returns: Average Pool된 임베딩 텐서

    """
    if (not model) or (not tokenizer):
        model, tokenizer = _call_default_model(device=device)

    inputs = tokenizer(
        input_text,
        max_length=tokenizer.model_max_length,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(model.device)

    output = model(**inputs)
    last_hidden = output.last_hidden_state.masked_fill(~inputs['attention_mask'][..., None].bool(), 0.0)
    embeddings = (last_hidden.sum(dim=1) / inputs['attention_mask'].sum(dim=1)[..., None]).to("cpu")
    embeddings = F.normalize(embeddings, p=2, dim=1)
    return embeddings