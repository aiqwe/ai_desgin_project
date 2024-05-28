import streamlit as st
import pandas as pd
from typing import Literal
from src import process
from src import api
from src import prompts
import json

def get_data(user_id: int = None, age: int = None, gender: str = None, dic: dict = None):
    if not user_id or not age or not gender:
        raise ValueError("가입자일련번호, 나이, 성별은 필수값입니다.")
    user_id = int(user_id)
    group = process.get_group_info(age=age, gender=gender)
    my = process.get_personal_info(user_id = user_id)
    if dic is None:
        raise ValueError("새로 입력한 값이 없습니다.")
    df = pd.DataFrame(data=[group, my, dic], columns=group.keys())
    df['기준년도'] = df['기준년도'].astype(str)
    df['가입자일련번호'] = df['가입자일련번호'].astype(str)
    df = df.T
    df.columns = ['평균', '2022년', '현재']
    return df

def get_health_completion(
        age = None,
        gender = None,
        dic = None,
        prompt_type: Literal["report", "age"] = None,
        model = "gpt-3.5-turbo"
):

    prompt_mapper = {
        "report": prompts.HEALTH_REPORT_PROMPT,
        "age": prompts.HEALTH_AGE_PROMPT
    }

    if dic is None or age is None or gender is None:
        raise ValueError(
            "건강검진결과를 입력해주세요. 나이와 성별은 필수값입니다."
        )
    group_string = process.get_group_info(age=age, gender=gender, to_string=True)
    prompt = prompt_mapper[prompt_type].format(current=process._to_string(dic), group=group_string)
    response = api.get_completion(prompt=prompt, model=model)
    return response

st.title("당신의 건강을 측정해보세요.")
st.markdown("---")
st.subheader("당신의 건강검진 결과를 입력해주세요.")
# 건강나이
st.write(f"당신의 건강검진 결과를 입력해주세요.")
dic = {
    "기준년도": st.text_input(label="기준년도", placeholder="yyyy로 입력하세요. 예) 2023"),
    "가입자일련번호": st.text_input(label="가입자일련번호", placeholder="1 ~ 100000 사이의 숫자를 입력하세요. 예) 1"),
    "나이": st.text_input(label="나이", placeholder="나이를 입력하세요. 예) 45"),
    "성별": st.text_input(label="성별", placeholder="성별을 입력하세요. 예) 남 또는 여"),
    "키": st.text_input(label="키", placeholder="키를 입력하세요. 예) 159.6"),
    "체중": st.text_input(label="체중", placeholder="체중을 입력허세요. 예) 52.6"),
    "허리둘레": st.text_input(label="허리둘레", placeholder="허리둘레를 입력하세요. 예) 75.2"),
    "시력_좌": st.text_input(label="시력 (좌)", placeholder="왼쪽 눈의 시력을 입력하세요. 예) 0.9"),
    "시력_우": st.text_input(label="시력 (우)", placeholder="오른쪽 눈의 시력을 입력하세요. 예) 0.9"),
    "청력_좌": st.text_input(label="청력 (좌)", placeholder="왼쪽 청력을 입력하세요. 예) 0.8"),
    "청력_우": st.text_input(label="청력 (우)", placeholder="오른쪽 청력을 입력하세요. 예) 0.8"),
    "수축기혈압": st.text_input(label="수축기 혈압", placeholder="수축했을 때의 혈압을 입력하세요. 예) 115.1"),
    "이완기혈압": st.text_input(label="이완기 혈압", placeholder="이완했을 때의 혈압을 입력하세요. 예) 80.1"),
    "식전혈당": st.text_input(label="식전혈당", placeholder="밥먹기 전 혈당을 입력하세요. 예) 95.5"),
    "총콜레스테롤": st.text_input(label="총 콜레스테롤", placeholder="콜레스테롤 수치를 입력하세요. 예) 195.5"),
    "트리글리세라이드": st.text_input(label="중성지방", placeholder="중성지방 수치를 입력하세요. 예) 98.5"),
    "HDL콜레스테롤": st.text_input(label="HDL콜레스테롤", placeholder="HDL콜레스테롤 수치를 입력하세요. 예) 62.5"),
    "LDL콜레스테롤": st.text_input(label="LDL콜레스테롤", placeholder="LDL콜레스테롤 수치를 입력하세요. 예) 114.5"),
    "혈색소": st.text_input(label="혈색소", placeholder="혈색소 수치를 입력하세요. 예) 12.97"),
    "요단백": st.text_input(label="요단백", placeholder="요단백 수치를 입력하세요. 예) 1.2"),
    "혈청크레아티닌": st.text_input(label="혈청크레아티닌", placeholder="혈청크레아티닌 수치를 입력하세요. 예) 0.65"),
    "혈청지오티": st.text_input(label="혈청지오티", placeholder="혈청지오티 수치를 입력하세요. 예) 22.2"),
    "혈청지피티": st.text_input(label="혈청지피티", placeholder="혈청지피티 수치를 입력하세요. 예) 18.5"),
    "감마지티피": st.text_input(label="감마지티피", placeholder="감마지티피 수치를 입력하세요. 예) 22.5"),
    "흡연상태": st.text_input(label="흡연상태", placeholder="흡연상태를 입력하세요. 예) 1=흡연중, 0=흡연 안함"),
    "음주여부": st.text_input(label="음주여부", placeholder="음주여부를 입력하세요. 예) 1=음주함, 0=음주 안함"),
}
if st.button(label = "제출하기"):
    st.subheader("당신의 건강 검진 결과")
    st.markdown("---")

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("./assets/health.png")
        st.write("건강검진 결과")

    with col2:
        df = get_data(user_id=dic['가입자일련번호'], age=int(dic['나이']), gender=dic['성별'], dic=dic)
        st.dataframe(df)
    # with col3:
    #     df = get_data(user_id=dic['가입자일련번호'], age=int(dic['나이']), gender=dic['성별'], dic=dic)
    #     st.dataframe(df)
    st.subheader("검진 결과 소견")

    # get completion
    with st.status("AI가 소견을 작성중이에요...", expanded=True) as status:
        st.write("건강검진 결과를 작성중이에요.")
        health_report = get_health_completion(age=int(dic['나이']), gender=dic['성별'], dic=dic, prompt_type="report", model="gpt-4o")
        st.write("건강 나이를 측정중이에요.")
        health_age_report = get_health_completion(age=int(dic['나이']), gender=dic['성별'], dic=dic, prompt_type="age", model="gpt-4o")

        # 건강검진 결과
    with st.chat_message("assistant"):
        st.write(health_report)

    # 건강나이
    st.markdown("---")
    st.subheader("당신의 건강 나이")

    # result = json.loads(health_age_report)
    # health_age = result['health_age']
    # health_age_reason = result['reason']
    # col1, col2 = st.columns([1, 3])
    # with col1:
    #     st.metric(
    #         label="당신의 건강나이",
    #         value = health_age,
    #         delta = f"-{int(dic['나이']) - health_age}(실제나이 대비)",
    #         delta_color="inverse"
    #     )
    with st.chat_message("assistant"):
        st.write(health_age_report)


