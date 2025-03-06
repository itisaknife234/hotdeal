import streamlit as st
import requests
import pandas as pd
from bs4 import beautifulSoup

def fetch_hotdeals(keyword):
    url = "https://arca.live/b/hotdeal"  # 아카라이브 핫딜 게시판
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
    except requests.exceptions.RequestException as e:
        st.error(f"🔴 데이터 요청 중 오류 발생: {e}")
        return []
    
    try:
        soup = BeautifulSoup(response.text, "html.parser")  # html.parser를 기본으로 사용
    except Exception as e:
        st.error(f"🔴 HTML 파싱 중 오류 발생: {e}")
        return []

    deals = []
    for item in soup.select(".list_title span a"):
        title = item.text.strip()
        link = "https://arca.live" + item.get("href")
        if keyword.lower() in title.lower():
            deals.append({"제목": title, "링크": link})

    return deals[:3]  # 최신 3개 항목만 반환

def main():
    st.title("핫딜 검색기 🔥")

    keyword = st.text_input("검색할 핫딜 키워드를 입력하세요:", "")

    if st.button("검색"):
        with st.spinner("검색 중..."):
            results = fetch_hotdeals(keyword)
            if results:
                df = pd.DataFrame(results)
                st.write(f"🔍 최근 3개의 결과를 찾았습니다!")
                st.dataframe(df)
            else:
                st.warning("❌ 해당 키워드에 대한 핫딜이 없습니다.")

if __name__ == "__main__":
    main()
