#!/bin/sh

# fastapi 실행 명령어
poetry run uvicorn main:app --host 0.0.0.0 --port 80 --reload