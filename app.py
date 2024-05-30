from datetime import datetime
import streamlit as st
import pandas as pd
from typing import Literal
from src import process
from src import api
from src import prompts
import json

st.set_page_config(layout="wide")

############################################################ Declaration ############################################################
def get_data(user_id: int = None, age: int = None, gender: str = None, dic: dict = None):
    if not user_id or not age or not gender:
        raise ValueError("가입자일련번호, 나이, 성별은 필수값입니다.")
    user_id = int(user_id)
    group = process.get_group_info(age=age, gender=gender)
    my = process.get_personal_info(user_id = user_id)
    my.update({"기준년도": datetime.now().year})
    if dic is None:
        raise ValueError("새로 입력한 값이 없습니다.")
    df = pd.DataFrame(data=[group, my, dic], columns=group.keys())
    df['가입자일련번호'] = df['가입자일련번호'].astype(str)
    df = df.T
    df.columns = [f'{age}/{gender} 그룹 평균', '최근 검진 결과', '올해 검진 결과']
    return df

def get_health_completion(
        age = None,
        gender = None,
        dic = None,
        prompt_type: Literal["report", "age"] = None,
        model = None,
        api_key = None
):

    prompt_mapper = {
        "report": prompts.HEALTH_REPORT_PROMPT,
        "age": prompts.HEALTH_AGE_PROMPT
    }

    if dic is None or age is None or gender is None:
        raise ValueError(
            "건강검진결과를 입력해주세요. 나이와 성별은 필수값입니다."
        )
    if model is None:
        model = "gpt-3.5-turbo"

    group_string = process.get_group_info(age=age, gender=gender, to_string=True)
    prompt = prompt_mapper[prompt_type].format(current=process._to_string(dic), group=group_string)
    response = api.get_completion(prompt=prompt, model=model, api_key=api_key)
    return response

# 건강나이
@st.experimental_dialog("건강 검진 결과를 입력해보세요.")
def make_newdata():
    dic = {
        "openai_key": st.text_input(label="OPENAI_API_KEY를 입력하세요.", placeholder="sk-...."),
        "openai_model": st.selectbox(label="OPENAI_API에서 사용할 모델을 골라주세요.", options=("gpt-4o", "gpt-3.5-turbo")),
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
    if st.button("제출하기"):
        st.session_state.openai = {'openai_key': dic['openai_key'], 'openai_model': dic['openai_model']}
        st.session_state.make_newdata = {"dic": dic}
        st.rerun()

############################################################ Body ############################################################

col1, col2 = st.columns([1, 20])
with col1:
    st.image("./assets/health_icon.png")
with col2:
    st.markdown("### 당신의 건강을 측정해보세요.")
st.markdown("---")

if "make_newdata" not in st.session_state or "openai" not in st.session_state:
    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("./assets/health_check_image.jpeg", width=250)
    with col2:
        st.markdown("""##### 얼마나 건강한지 궁금하신가요?""")
        st.text("""건강 검진 데이터를 입력하고, 소견을 받아보세요.\n검사 결과 뿐만아니라 건강 나이까지 측정해드립니다.
        """)
        if st.button("직접 입력하러가기"):
            make_newdata()
        uploaded_file = st.file_uploader("또는 파일을 업로드하세요.")
        st.write("아래 OPENAI API 정보는 PoC 용으로 임시로 설정합니다.")
        openai_key = st.text_input(label="발급받은 OPENAI_API_KEY를 입력하세요.", placeholder="sk-....")
        openai_model = st.selectbox(label="OPENAI_API에 사용할 모델을 골라주세요.", options=("gpt-4o", "gpt-3.5-turbo"))
        if openai_key is not None and openai_model is not None:
            st.session_state.openai = {'openai_key': openai_key, 'openai_model': openai_model}

        if uploaded_file is not None:
            st.write(uploaded_file.name)
            if uploaded_file.name.endswith("csv"):
                dic = pd.read_csv(uploaded_file).to_dict("records")[0]
            if uploaded_file.name.endswith("xlsx"):
                dic = pd.read_excel(uploaded_file).to_dict("records")[0]
            st.session_state.make_newdata = {"dic": dic}
        if st.button("파일로 제출하기"):
            st.rerun()


else:
    dic = st.session_state.make_newdata['dic']
    openai_key = st.session_state.openai['openai_key']
    openai_key = api._getenv("OPENAI_API_KEY") if openai_key is None else openai_key
    openai_model = st.session_state.openai['openai_model']
    openai_model = openai_model if openai_model is not None else "gpt-4o"

    col1, col2, col3 = st.columns([1, 3.5, 2.5])

    with col1:
        st.markdown("#### 당신의 건강 검진 결과에요.")
        st.image("./assets/health.png")

    with col2:
        # get completion
        with st.status("AI가 소견을 작성중이에요...", expanded=True) as status:
            st.write("건강검진 결과를 작성중이에요.")
            health_report = get_health_completion(age=int(dic['나이']),
                                                  gender=dic['성별'],
                                                  dic=dic,
                                                  prompt_type="report",
                                                  model=openai_model,
                                                  api_key=openai_key)
            st.write("건강 나이를 측정중이에요.")
            health_age_report = get_health_completion(age=int(dic['나이']),
                                                      gender=dic['성별'],
                                                      dic=dic,
                                                      prompt_type="age",
                                                      model=openai_model,
                                                      api_key=openai_key)

        # 건강검진 결과
        with st.chat_message("assistant"):
            st.write(health_report)


    with col3:
        df = get_data(user_id=dic['가입자일련번호'], age=int(dic['나이']), gender=dic['성별'], dic=dic)
        st.dataframe(df, height=900)

    # 건강나이
    st.markdown("---")
    st.markdown("#### 당신의 건강 나이에요.")
    health_age_report = health_age_report.replace("`", "")
    health_age_report = health_age_report.replace("json", "")

    result = json.loads(health_age_report)
    health_age = result['health_age']
    health_age_reason = result['reason']
    col1, col2 = st.columns([1, 5])
    with col1:
        st.metric(
            label = "당신의 건강 나이",
            value = f"{health_age}세",
            delta = f"{health_age - int(dic['나이'])}(실제나이 대비)",
        )
        if health_age - int(dic['나이']) > 0:
            st.markdown("🥲 :red[안되요. 실제 나이보다 더 건강하지 못해요!]")
        if health_age - int(dic['나이']) < 0:
            st.markdown("😆 :green[좋아요! 실제 나이보다 더 젊어요!]")

    with col2:
        with st.chat_message("assistant"):
            st.write(health_age_reason)

    del st.session_state.make_newdata
    del st.session_state.openai

    if st.button("다시 입력하기"):
        st.rerun()


