import logging
from playwright.sync_api import Page
from typing import Dict, Any, Optional

class LoginScenario:
    """
    로그인 후 메인 페이지 진입 및 핵심 요소의 가시성을 확인하는 시나리오.
    설정 파일(config)을 통해 대상 URL과 계정 정보를 유연하게 받아 처리합니다.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger("LoginScenario")

    def run(self, page: Page) -> bool:
        """
        시나리오 실행: 로그인 -> 메인 페이지 대기 -> 핵심 요소 검증
        returns: 성공 여부 (True/False)
        """
        try:
            # 1. 로그인 페이지 이동
            self.logger.info(f"Navigating to login page: {self.config['login_url']}")
            page.goto(self.config['login_url'])

            # 2. 로그인 정보 입력 및 제출
            # 셀렉터는 설정 파일에서 가져옴 (사이트마다 다르므로)
            page.fill(self.config['selectors']['username'], self.config['auth']['username'])
            page.fill(self.config['selectors']['password'], self.config['auth']['password'])
            page.click(self.config['selectors']['submit'])

            # 3. 로그인 후 메인 페이지 진입 대기
            self.logger.info("Waiting for main page load after login...")
            page.wait_for_url(self.config['main_url'], timeout=10000)

            # 4. 핵심 요소(Success Indicator) 가시성 확인
            # 예: '로그아웃' 버튼이나 '마이페이지' 텍스트가 보이는지 확인
            success_selector = self.config['selectors']['success_indicator']
            if page.is_visible(success_selector):
                self.logger.info(f"Success indicator found: {success_selector}")
                return True
            else:
                self.logger.error(f"Success indicator NOT found: {success_selector}")
                return False

        except Exception as e:
            self.logger.exception(f"Scenario failed due to error: {str(e)}")
            return False
