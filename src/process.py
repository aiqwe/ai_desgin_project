import pandas as pd
from functools import cache
from src import Path

def get_value_type():
    """ 연속변수와 명목변수 구분 """
    type_mapper = {
        "con": ['키', '체중', '허리둘레', '시력_좌', '시력_우', '청력_좌', '청력_우', '수축기혈압', '이완기혈압',
                '식전혈당', '총콜레스테롤', '트리글리세라이드', 'HDL콜레스테롤', 'LDL콜레스테롤', '혈색소', '요단백',
                '혈청크레아티닌', '혈청지오티', '혈청지피티', '감마지티피'],
        "cate": ['흡연상태', '음주여부']
    }
    return type_mapper

def _infer_df(dataframe:pd.DataFrame = None):
    """ 데이터프레임을 명시하지 않으면 data.csv를 읽도록 하기"""
    if dataframe is None:
        dataframe = get_dataframe()
    return dataframe

def _to_string(data):
    return "\n".join(f"{key}: {value}" for key, value in data.items())

@cache
def get_dataframe(df: pd.DataFrame = None) -> pd.DataFrame:
    """ 데이터 프레임 읽어오기 """
    if not df:
        df = pd.read_parquet(str(Path.data_path / "data.parquet"))
    return df

def get_personal_info(user_id: int, df: pd.DataFrame = None, to_string: bool = False) -> dict:
    """ 특정 id의 정보 읽어오기 """
    df = _infer_df(dataframe=df)
    data = df[df['가입자일련번호'] == user_id].to_dict("records")[0]

    if to_string:
        data = _to_string(data)

    return data

def get_group_info(age: int, gender: str, df: pd.DataFrame = None, to_string: bool = False) -> dict:
    """ 특정 유저의 성/연령에 해당하는 정보를 집계하기"""
    df = _infer_df(dataframe=df)
    if not isinstance(gender, str):
        raise ValueError("gender should be string type.")
    if not isinstance(age, int):
        raise ValueError("age should be integer type.")

    df = df.query(f'성별 == "{gender}" and 나이 == {age}')
    data = {"기준년도": "TOTAL", "가입자일련번호": "GROUP", "나이": age, "성별": gender}
    data.update(_get_agg_data(df))

    if to_string:
        data = _to_string(data)

    return data

def _get_agg_data(df, how="mean"):
    """ get_group_info에서 사용하는 집계함수 구현"""
    mapper = get_value_type()
    columns = df.columns
    res = {}

    for col in columns:
        if col in mapper['con']:
            res[col] = round(df.agg({col: how}).item(), 2) # 연속변수면 how 파라미터에 따라 처리
        if col in mapper['cate']:
            res[col] = df[col].mode().item() # Categorical 데이터면 가장 빈도수가 많은 데이터로 선택

    return res




