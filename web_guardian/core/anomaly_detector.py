import logging
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Anomaly:
    type: str  # 'NETWORK' or 'CONSOLE'
    level: str # 'ERROR' or 'WARNING'
    url: Optional[str]
    message: str
    timestamp: str

class AnomalyDetector:
    """
    Playwright 브라우저의 네트워크 응답과 콘솔 로그를 모니터링하여 
    이상 징후(4xx, 5xx 에러, JS Runtime Error 등)를 포착하는 클래스.
    """
    def __init__(self):
        self.anomalies: List[Anomaly] = []
        self.logger = logging.getLogger("AnomalyDetector")

    def handle_console(self, msg):
        """브라우저 콘솔 메시지 핸들러"""
        # 'error' 타입의 메시지만 필터링하여 저장
        if msg.type == "error":
            anomaly = Anomaly(
                type="CONSOLE",
                level="ERROR",
                url=None, # 콘솔 메시지는 특정 URL 매핑이 어려울 수 있음
                message=msg.text,
                timestamp="N/A" 
            )
            self.anomalies.append(anomaly)
            self.logger.error(f"[CONSOLE ERROR] {msg.text}")

    def handle_response(self, response):
        """네트워크 응답 핸들러"""
        status = response.status
        # 400 이상의 상태 코드를 이상 징후로 판단
        if status >= 400:
            anomaly = Anomaly(
                type="NETWORK",
                level="ERROR" if status >= 500 else "WARNING",
                url=response.url,
                message=f"HTTP Status {status}",
                timestamp="N/A"
            )
            self.anomalies.append(anomaly)
            self.logger.warning(f"[NETWORK ERROR] {status} - {response.url}")

    def get_all_anomalies(self) -> List[Anomaly]:
        """포착된 모든 이상 징후 리스트 반환"""
        return self.anomalies

    def has_critical_issue(self) -> bool:
        """치명적인 이슈(5xx 에러 등)가 있는지 확인"""
        return any(a.level == "ERROR" and a.type == "NETWORK" for a in self.anomalies)
