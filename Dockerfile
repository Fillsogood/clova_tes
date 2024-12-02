# Python 3.11 이미지를 베이스로 사용
FROM python:3.11

# pip 최신 버전 설치 및 poetry 설치
RUN pip install --upgrade pip \
    && pip install poetry

# 작업 디렉터리 설정
WORKDIR /solideng

# 필요한 파일 복사
COPY ./pyproject.toml ./poetry.lock* ./
COPY ./start.sh /solideng/start.sh
COPY . .

# Poetry로 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# 실행 권한 부여
RUN chmod +x /solideng/start.sh

# 컨테이너 시작 시 start.sh 실행
ENTRYPOINT ["sh", "./start.sh"]
