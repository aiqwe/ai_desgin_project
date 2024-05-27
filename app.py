import streamlit as st
import pandas as pd
import numpy as np
from src import process

# parameters
health_age = 65
group_health_age = 70

def get_data(user_id = None, dic = None):
    if user_id is None:
        raise ValueError("가입자일련번호는 필수값입니다!")
    user_id = int(user_id)
    group = process.get_group_info(user_id = user_id)
    my = process.get_personal_info(user_id = user_id)
    if dic is None:
        raise ValueError("새로 입력한 값이 없습니다.")
    df = pd.DataFrame(data=[group, my, dic], columns=group.keys())
    df['기준년도'] = df['기준년도'].astype(str)
    df['가입자일련번호'] = df['가입자일련번호'].astype(str)
    df = df.T
    df.columns = ['평균', '2022년', '현재']
    return df

def get_completion(user_id = None):
    if user_id is None:
        raise ValueError("가입자일련번호는 필수값입니다!")
    pass

st.title("당신의 건강 나이를 측정해보세요.")
st.markdown("---")
st.subheader("당신의 건강검진 결과를 입력해주세요.")

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

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        st.image("./assets/health.png")
        st.write("건강검진 결과")

    with col2:
        df = get_data(user_id=dic['가입자일련번호'], dic=dic)
        st.dataframe(df)
    with col3:
        df = get_data(user_id=dic['가입자일련번호'], dic=dic)
        st.dataframe(df)
    st.write("검사 소견")
    st.text("노답임.") # 검사소견
    st.markdown("---")
    st.subheader("당신의 건강 나이")
    # 건강나이
    # 동년배 건강나이
    # 당신의 건강나이



