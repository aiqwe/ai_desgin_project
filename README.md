### 인공지능 종합 설계 프로젝트 레포 🚀

### 팀
6조

### 제목
나의 건강 검진 소견 받고 건강 나이 찾기

### 실행하기 (git)
1. 먼저 레포를 클론합니다.
```shell
git clone https://github.com/aiqwe/ai_desgin_project.git
```
2. 필요한 라이브러리를 설치해주세요.
```shell
cd ai_desgin_project
pip install --upgrade pip
pip install -r requirements.txt
```
3. streamlit을 실행해주세요. (가급적 port를 지정해주세요)
```shell
streamlit run app.py --server.port=7860
```
4. 루프백 8501포트로 접속가능합니다.
```shell
Local URL: http://localhost:7860 # 여기로 접속 가능!
```

### 실행하기(docker)
docker / docker-compose가 설치되어있으면 아래와 같이 실행가능합니다.
```shell
docker-compose up -d
```
http://localhost:7860 으로 접속하면 사용 가능합니다!


### 데이터 입력하기
직접 입력 말고도 csv 또는 xlsx로 업로드할 수 있어요.  
Openai API key와 모델을 입력해주세요.
(가급적 모델은 gpt-4o를 써야 에러가 안납니다!)

### Contributors
| 이름  | 학번     |
|-----|--------|
| 박건우 | A64011 |
| 유황선 | A67028 |
| 이두진 | A68066 |
| 정현정 | A65033 |
| 이재상 | A64058 |

### Code Tree
+ [src/data](src/data) : 공공데이터에서 수집한 건강검진 데이터(10만건)
+ [src/api.py](src/api.py) : ChatGPT API 코드
+ [src/process.py](src/process.py) : 건강검진 데이터를 전처리하기 위한 코드
+ [src/prompts.py](src/prompts.py) : ChatGPT에 건내줄 프롬프트 파일
