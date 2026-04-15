import requests
import os

# GitHub Secrets(금고)에서 정보를 가져옵니다
TARGET_URL = os.environ.get('TARGET_URL')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
# 사이트에 따라 "품절" 또는 "상담원 연결" 중 현재 표시되는 문구로 설정하세요
SOLD_OUT_TEXT = "상담원 연결" 

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(TARGET_URL, headers=headers)
        
        # 전체 페이지 내용에서 SOLD_OUT_TEXT가 없으면 재고가 있는 것으로 판단
        if SOLD_OUT_TEXT not in response.text:
            payload = {"text": f"🚨 재고 발생!! 지금 바로 접속하세요!\n주소: {TARGET_URL}"}
            res = requests.post(SLACK_WEBHOOK_URL, json=payload)
            print(f"재고 발견! 슬랙 전송 결과: {res.status_code}")
        else:
            print(f"[{response.status_code}] 아직 '{SOLD_OUT_TEXT}' 상태입니다.")
            
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    check_stock()
