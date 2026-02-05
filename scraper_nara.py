import os
import requests
import datetime
#import pandas as pd

# 1. 설정 (인증키와 검색어)
# 공공데이터포털에서 발급받은 Decoding 인증키를 입력하세요.
# 직접 입력하기보다 GitHub Secrets를 쓰는 게 좋지만, 일단 여기에 넣어 테스트해봐!
MY_API_KEY = "f6d40f87e591061160a75d151bcd1c70ef587d9c7620574258622e939db0131a" 

def get_g2b_data():
    url = "http://apis.data.go.kr/1230000/BidPublicInfoService05/getBidPblancListInfoServc01"
    
    # 오늘 날짜 기준으로 검색 (예: 20260204)
    today = datetime.datetime.now().strftime("%Y%m%d")
    
    params = {
        'serviceKey': MY_API_KEY,
        'numOfRows': '20',      # 가져올 공고 수
        'pageNo': '1',
        'inqryDiv': '1',        # 공고명 검색
        'bidNtceNm': '코스콤',     # 검색 키워드 (원하는 대로 수정!)
        'type': 'json'          # 결과 형식
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        items = data.get('response', {}).get('body', {}).get('items', [])
        if not items:
            print("수집된 공고가 없습니다.")
            return []
        
        return items
    except Exception as e:
        print(f"API 호출 중 오류 발생: {e}")
        return []

# 2. RSS XML 생성
items = get_g2b_data()

if items:
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title><![CDATA[나라장터 보안 공고 피드]]></title>
    <link>https://www.g2b.go.kr</link>
    <description><![CDATA[조달청 API를 통해 수집된 최신 보안 입찰 정보]]></description>
    <language>ko-kr</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="https://raw.githubusercontent.com/happyhjlee/scraper/main/g2b_feed.xml" rel="self" type="application/rss+xml" />"""

    for item in items:
        title = item.get('bidNtceNm', '제목 없음')
        link = item.get('bidNtceDtlUrl', 'https://www.g2b.go.kr')
        org = item.get('ntceInsttNm', '알 수 없음') # 공고기관
        end_date = item.get('bidClseDt', '마감일 정보 없음') # 입찰마감일시
        
        rss_xml += f"""
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{link}</link>
        <description><![CDATA[공고기관: {org}<br>마감일시: {end_date}]]></description>
        <guid isPermaLink="false">{item.get('bidNtceNo', title)}</guid>
        <pubDate>{now}</pubDate>
    </item>"""
    
    rss_xml += "\n</channel>\n</rss>"

    # 3. 파일 저장 (파일명은 g2b_feed.xml로 구분하자)
    with open("g2b_feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)
    print(f"성공: {len(items)}건의 공고를 g2b_feed.xml로 저장했습니다.")
else:
    print("수집된 데이터가 없어 파일을 생성하지 않았습니다.")
