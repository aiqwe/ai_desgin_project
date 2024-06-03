FROM python:3.11-slim
ARG app_path=/root/ai_desgin_project

RUN apt-get update && apt-get install cmake git -y
RUN git clone https://github.com/aiqwe/ai_desgin_project.git $app_path
WORKDIR $app_path

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
