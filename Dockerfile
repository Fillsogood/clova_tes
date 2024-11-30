# Python 3.11 이미지를 베이스 이미지로 사용
FROM python:3.11

# pip를 최신 버전으로 업그레이드하고, poetry 패키지를 설치
RUN pip install --upgrade pip \
    && pip install poetry

# 컨테이너 내 작업 디렉터리를 /solideng로 설정
WORKDIR /solideng

# 프로젝트의 pyproject.toml 파일과 poetry.lock 파일을 컨테이너로 복사
COPY ./pyproject.toml ./poetry.lock* ./

# poetry 설정 및 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || echo "No logs available."

COPY . .

RUN chmod +x ./start.sh

# 컨테이너 시작 시 start.sh 스크립트를 실행하도록 설정
ENTRYPOINT ["./start.sh"]