import logging
import sys
from typing import Dict, Any
from core.browser_manager import BrowserManager
from core.anomaly_detector import AnomalyDetector
from scenarios.login_check import LoginScenario

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('reports/logs/guardian.log')
    ]
)
logger = logging.getLogger("WebGuardian")

# 범용 프로토타입 설정 (실제 사용 시 이 부분을 yaml/json 파일로 분리)
DEFAULT_CONFIG = {
    "login_url": "https://example.com/login",
    "main_url": "https://example.com/dashboard",
    "auth": {
        "username": "test_user",
        "password": "test_password"
    },
    "selectors": {
        "username": "input[name='username']",
        "password": "input[name='password']",
        "submit": "button[type='submit']",
        "success_indicator": ".dashboard-welcome-msg"
    }
}

def main():
    logger.info("Starting Web Guardian Anomaly Detection System...")
    
    config = DEFAULT_CONFIG
    detector = AnomalyDetector()
    
    try:
        with BrowserManager(headless=True) as bm:
            page = bm.get_page()
            
            # [중요] Global Watcher 등록: 네트워크 응답 및 콘솔 메시지 리스너 연결
            page.on("console", detector.handle_console)
            page.on("response", detector.handle_response)
            
            logger.info("Running Login Scenario...")
            scenario = LoginScenario(config)
            success = scenario.run(page)
            
            # 결과 취합
            anomalies = detector.get_all_anomalies()
            critical_issue = detector.has_critical_issue()
            
            print("\n" + "="*50)
            print("🚀 WEB GUARDIAN FINAL REPORT")
            print("="*50)
            print(f"✅ Scenario Status : {'SUCCESS' if success else 'FAILED'}")
            print(f"⚠️  Anomalies Found : {len(anomalies)} items")
            print(f"🚨 Critical Issue : {'YES' if critical_issue else 'NO'}")
            print("-"*50)
            
            if anomalies:
                print("Detailed Anomalies:")
                for i, a in enumerate(anomalies, 1):
                    print(f"{i}. [{a.type}] {a.level} - {a.message} ({a.url or 'N/A'})")
            else:
                print("No anomalies detected. System is healthy.")
            print("="*50 + "\n")
            
            if not success or critical_issue:
                sys.exit(1) # 에러 발생 시 Exit Code 1 반환

    except Exception as e:
        logger.exception(f"System crash: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
