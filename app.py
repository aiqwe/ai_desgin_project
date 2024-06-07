from datetime import datetime
import streamlit as st
import pandas as pd
from typing import Literal, Dict, List
import time
import json
import webbrowser as wb
from urllib import parse
from src import (
    process,
    api,
    prompts,
    chromadb,
    inference
)

st.set_page_config(layout="wide")

# Function Declaration
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

@st.cache_data
def get_health_completion(
        messages: List[Dict] = None,
        model: str = None,
        api_key: str = None
) -> str:
    """
    GPT API로 건강검진 결과, 건강 나이 Response를 Request합니다.
    Args:
        model: 사용할 GPT 모델
        api_key: Open AI API Key
        prompt_config: 프롬프트 및 프롬프트에 전달할 포맷
          - prompt_config['messages'] : (필수값) 사용할 멀티턴 mesages
          작성 예시)

              prompt = "{clothes} 입고가도되?".format(clothes=clothes)

              messages = [
                  {"role": "system", "content": "당신은 날씨를 잘 알고 있는 코디네이터에요."},
                  {"role": "user", "content": "오늘 날씨 알려줘"},
                  {"role": "assistant", "content": "오늘 날씨는 30도로 예상되며..."},
                  {"role": "assistant", "content": prompt}
              ]

    Returns: ChatGPT Response 문자열

    """

    if not messages:
        raise ValueError("messages는 필수값입니다.")

    if not model:
        model = "gpt-4o"

    response = api.get_completion(messages=messages, model=model, api_key=api_key)
    return response

# 건강나이
@st.experimental_dialog("건강 검진 결과를 입력해보세요.")
def make_newdata():
    dic = {
        "openai_key": st.text_input(label="OPENAI_API_KEY를 입력하세요.", placeholder="sk-....", type="password"),
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

def text_generator(text):
    tokens = text.split(" ")
    for token in tokens:
        yield token + " "
        time.sleep(0.02)

def json_parse(text):
    text = text.replace("`", "")
    text = text.replace("json", "")
    text = text.replace("json", "")
    result = json.loads(text)
    return result

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
        openai_key = st.text_input(label="발급받은 OPENAI_API_KEY를 입력하세요.", placeholder="sk-....", type="password")
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

# 건강 검진 결과 / 건강 나이 메인 페이지
else:
    # Variable Declaration
    dic = st.session_state.make_newdata['dic']
    openai_key = st.session_state.openai['openai_key']
    openai_key = openai_key if openai_key else api._getenv("OPENAI_API_KEY")
    openai_model = st.session_state.openai['openai_model']
    openai_model = openai_model if openai_model is not None else "gpt-4o"
    chroma = chromadb.Chroma('test')

    age = int(dic['나이'])
    gender = dic['성별']

    group_string = process.get_group_info(age=age, gender=gender, to_string=True)
    current_string = process._to_string(dic)

    # get completion
    with st.status("AI가 검진 결과를 작성중이에요...", expanded=True) as status:
        st.write_stream(text_generator("건강검진 결과를 해석중이에요..."))
        messages = [
            {"role": "user", "content": prompts.HEALTH_REPORT_PROMPT_1.format(current=current_string, group=group_string)}
        ]
        disease = get_health_completion(messages=messages, model=openai_model, api_key=openai_key)
        disease = json_parse(disease)
        st.text(disease['disease'])

        if len(disease['disease']) > 1 or disease['disease'][0] != "NO":
            disease_exists = False

        urls_string = ""
        if not disease_exists:
            st.write_stream(text_generator("관련된 문서를 Vector DB에서 찾고 있어요..."))
            urls = [chroma.query(encoder.average_pool(d).tolist(), n_results=1)['metadatas'][0][0]['url'] for d in disease['disease']]
            urls_string = process._to_string(urls)
        st.write_stream(text_generator("찾은 문서로 GPT에게 물어보고 있어요..."))
        messages.append({"role": "user", "content": prompts.HEALTH_REPORT_PROMPT_2.format(current=current_string, group=group_string, url=urls_string)})
        health_report = get_health_completion(messages=messages, model=openai_model, api_key=openai_key)

    col1, col2, col3 = st.columns([1.5, 4, 2.5])
    with col1:
        st.markdown("#### 당신의 건강 검진 결과에요.")
        st.image("./assets/health.png")
        st.text(disease)
        st.text("YES" if disease else "NO")
        if not disease_exists:
            disease_string = "".join(disease['disease'])
            st.markdown("이 질병들을 조심하세요!")
            st.markdown("판교 근처에는 이런 병원들이 있어요")
            if st.button("병원 찾기"):
                area_encoded = parse.quote("판교")
                disease_encoded = parse.quote(disease['disease'][0])
                hospital_url = f"https://map.naver.com/p/search/{area_encoded}%20{disease_encoded}"
                wb.open_new(hospital_url)


    # 건강검진 결과
    with col2:
        st.chat_message("assistant").write_stream(text_generator(health_report))

    with col3:
        df = get_data(user_id=dic['가입자일련번호'], age=int(dic['나이']), gender=dic['성별'], dic=dic)
        st.dataframe(df, height=900)

    # 건강나이
    st.markdown("---")
    with st.status("AI가 건강 나이를 작성중이에요...", expanded=True) as status:
        st.write_stream(text_generator("건강 나이를 측정중이에요."))
        messages.append({'role': 'user', 'content': prompts.HEALTH_AGE_PROMPT})
        health_age_report = get_health_completion(messages=messages, model=openai_model, api_key=openai_key)

    st.markdown("#### 당신의 건강 나이에요.")

    result = json_parse(health_age_report)
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
            st.write_stream(text_generator(health_age_reason))


