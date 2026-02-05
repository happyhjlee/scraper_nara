import requests
from urllib.parse import unquote
import datetime

# 1. 포털에서 복사한 '일반 인증키'를 여기에 정확히 붙여넣어!
MY_API_KEY = "f6d40f87e591061160a75d151bcd1c70ef587d9c7620574258622e939db0131a"

def get_order_plan():
    # 발주계획 API 주소 (물품)
    url = "http://apis.data.go.kr/1230000/OrderPlanService02/getOrderPlanSttusListThng"
    
    # 일반 인증키가 인코딩된 상태일 수 있으니 unquote로 한 번 풀어주는 게 국룰이야!
    params = {
        'serviceKey': unquote(MY_API_KEY), 
        'numOfRows': '10',
        'pageNo': '1',
        'type': 'json',
        'prchseTargetNm': '보안'
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        
        # 만약 여기서 'Unexpected errors'가 뜨면 100% 키 등록 대기 중인 거야.
        if "Unexpected errors" in response.text:
            print("--- 아직 API 키가 활성화되지 않았어! (1시간 뒤에 다시 해봐) ---")
            return []
            
        data = response.json()
        items = data.get('response', {}).get('body', {}).get('items', [])
        
        if isinstance(items, dict):
            items = [items]
        return items
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

# 이후 RSS 생성 로직은 동일...
