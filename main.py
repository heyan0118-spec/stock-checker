import requests
import os

# 실제 주소 대신 '암호명'을 사용합니다.
# 깃허브 설정(Secrets)에 등록한 값을 자동으로 가져오게 됩니다.
TARGET_URL = os.environ.get('TARGET_URL')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SOLD_OUT_TEXT = "상담원 연결" 

def check_stock():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # 설정값이 잘 들어왔는지 확인
        if not TARGET_URL or not SLACK_WEBHOOK_URL:
            print("설정값(Secrets)이 비어있습니다.")
            return

        response = requests.get(TARGET_URL, headers=headers)
        if SOLD_OUT_TEXT not in response.text:
            requests.post(SLACK_WEBHOOK_URL, json={"text": "🚨 재고 발생!! 지금 바로 접속하세요!"})
            print("재고 발견! 알림 전송 완료.")
        else:
            print("아직 품절 상태입니다.")
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    check_stock()