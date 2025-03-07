import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import shutil
import os

def get_chromedriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Streamlit Cloud 또는 서버 환경에 따라 크롬 드라이버 경로 자동 설정
    chrome_path = shutil.which("chromedriver")
    if chrome_path:
        service = Service(chrome_path)
    else:
        st.error("❌ ChromeDriver가 설치되어 있지 않습니다. 관리자에게 문의하세요.")
        return None
    
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_hotdeals(keyword):
    url = f"https://arca.live/b/hotdeal?target=all&keyword={keyword}"  # 아카라이브 핫딜 검색 URL
    st.write(f"🔹 [1] 요청할 URL: {url}")
    
    driver = get_chromedriver()
    if driver is None:
        return []
    
    driver.get(url)
    time.sleep(3)  # 페이지 로딩 대기
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # 크롤러 종료
    
    st.write("🔹 [2] HTML 파싱 완료")
    
    deals = []
    for item in soup.select(".vrow"):  # 게시글 리스트에서 정보 가져오기
        title_tag = item.select_one(".title a")  # 게시글 제목
        if title_tag:
            title = title_tag.text.strip()
            link = "https://arca.live" + title_tag.get("href")
            deals.append({"제목": title, "링크": link})
    
    st.write(f"🔹 [3] 추출된 핫딜 개수: {len(deals)}")
    
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
