import logging
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional

class BrowserManager:
    """
    Playwright 브라우저의 생명주기를 관리하고, 
    설정(Headless 여부, Viewport 등) 및 세션(Context)을 생성하는 클래스.
    """
    def __init__(self, headless: bool = True, viewport: Optional[dict] = None):
        self.headless = headless
        self.viewport = viewport or {"width": 1280, "height": 720}
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.logger = logging.getLogger("BrowserManager")

    def start(self):
        """브라우저 실행 및 컨텍스트 설정"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        # 세션 관리를 위해 BrowserContext 생성
        self.context = self.browser.new_context(viewport=self.viewport)
        self.logger.info(f"Browser started (headless={self.headless})")

    def get_page(self) -> Page:
        """새 탭(Page) 생성 및 반환"""
        if not self.context:
            raise RuntimeError("BrowserManager.start() must be called before get_page()")
        return self.context.new_page()

    def close(self):
        """모든 리소스 정리"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.logger.info("Browser closed.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
