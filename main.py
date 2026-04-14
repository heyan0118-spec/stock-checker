import requests
import os

TARGET_URL = os.environ.get('TARGET_URL')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SOLD_OUT_TEXT = "상담원 연결"  # 실제 사이트에 표시되는 정확한 글자여야 합니다.

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(TARGET_URL, headers=headers)
        # 웹사이트의 전체 텍스트에서 '상담원 연길'이 포함되어 있는지 확인
        page_content = response.text
        
        if SOLD_OUT_TEXT in page_content:
            # 상담원 연결 글자가 발견됨 -> 알림 안 보냄
            print(f"[{response.status_code}] 아직 품절 상태입니다.")
        else:
            # 품절 글자가 발견되지 않음 -> 재고 발생 가능성!
            # 단, 사이트가 정상적으로 열렸을 때(200)만 알림 전송
            if response.status_code == 200:
                requests.post(SLACK_WEBHOOK_URL, json={"text": "🚨 재고 발생 가능성!! 지금 바로 확인하세요!"})
                print("재고 발견 가능성! 슬랙 알림 전송 완료.")
            else:
                print(f"사이트 접속 불안정 (상태코드: {response.status_code})")
                
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    check_stock()
