import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

def _getenv(key):
    """ 환경변수를 찾는 함수입니다. .env """
    load_dotenv(find_dotenv())
    return os.getenv(key)

def get_completion(
        prompt: str,
        model="gpt-3.5-turbo",
        api_key: str = None,
        response_format = None,
) -> str:
    """ ChatGPT API를 통한 챗봇 기능입니다.
    자세한 내용은 https://github.com/openai/openai-python을 참고하세요.

    Args:
        prompt: ChatGPT에 전송하려는 프롬프트
        model: ChatGPT 모델명

    Returns: ChatGPT response중 답변 텍스트 데이터

    """

    if not api_key:
        api_key = _getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI api key is not setted.")

    client = OpenAI(api_key=api_key)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5
    )
    client.close()

    return response.choices[0].message.content