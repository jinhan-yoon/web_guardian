# Playwright 공식 이미지 사용 (브라우저 및 OS 의존성 모두 포함됨)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 전체 복사
COPY . .

# 실행 권한 부여
RUN chmod +x run.sh

# 컨테이너 실행 시 run.sh 실행
CMD ["./run.sh"]
