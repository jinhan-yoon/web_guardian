# web_guardian
# 1. 현재 폴더를 Git 저장소로 초기화
git init

# 2. GitHub 원격 저장소 연결 (이름: origin)
git remote add origin https://github.com/jinhan-yoon/web_guardian.git

# 3. 기본 브랜치 이름을 main으로 변경 (GitHub 기본 권장 사항)
git branch -M main
2단계: 파일 추가 및 커밋(Commit) 생성
업로드할 파일들을 고르고, 어떤 변경사항인지 기록을 남기는 과정입니다.

Bash
# 1. 폴더 내의 모든 변경된 파일을 업로드 대상으로 지정
git add .

# 2. 버전 생성 및 설명 작성 (메시지는 자유롭게 변경 가능)
git commit -m "First commit - web_guardian setup"

# 3. Git 인증 정보 전달
git remote set-url origin https://<토큰ID>@github.com/jinhan-yoon/web_guardian.git

4단계: GitHub에 최종 업로드 (Push)
로컬에서 만든 커밋을 GitHub 저장소로 전송합니다.

Bash
git push -u origin main
💡 -u 옵션의 의미: > 처음 한 번만 -u origin main을 해주면, 다음부터는 긴 명령어 대신 **git push**나 **git pull**만

#커밋하기
git add .
git commit -m "코멘트"
git push -u origin main