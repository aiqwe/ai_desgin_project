import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from typing import List, Dict

def _getenv(key: str):
    """ 환경변수를 찾는 함수입니다. .env """
    load_dotenv(find_dotenv())
    return os.getenv(key)

def get_completion(
        messages: List[Dict],
        model: str = "gpt-4o",
        api_key: str = None,
) -> str:
    """ ChatGPT API를 통한 챗봇 기능입니다.
    자세한 내용은 https://github.com/openai/openai-python을 참고하세요.

    Args:
        messages: ChatGPT에 전송하려는 멀티턴 대화 내용
          예시)
          prompt = "{clothes} 입고가도되?".format(clothes=clothes)
          messages = [
              {"role": "system", "content": "당신은 날씨를 잘 알고 있는 코디네이터에요."},
              {"role": "user", "content": "오늘 날씨 알려줘"},
              {"role": "assistant", "content": "오늘 날씨는 30도로 예상되며..."},
              {"role": "assistant", "content": prompt}
          ]
        model: ChatGPT 모델명

    Returns: ChatGPT response중 답변 텍스트 데이터

    """

    if not api_key:
        api_key = _getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI api key is not setted.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
    )

    return response.choices[0].message.content