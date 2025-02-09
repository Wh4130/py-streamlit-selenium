import streamlit as st
from managers import *

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""




if st.button("點擊開始爬蟲"):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
    from selenium.webdriver.common.by import By
    import time
    import re
    import random
    import pandas as pd

    # @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    try:
        driver = get_driver()        # *** On streamlit cloud
        driver.get("https://www.cna.com.tw/list/aall.aspx")   
    except:
        driver = webdriver.Chrome()  # *** On local
        driver.get("https://www.cna.com.tw/list/aall.aspx")   


    


    # * load all news
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element(By.XPATH, '//*[@id="SiteContent_uiViewMoreBtn"]').click()
        except:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element(By.XPATH, '//*[@id="SiteContent_uiViewMoreBtn_Style3"]').click()
            except:
                break

        time.sleep(0.4)

    # * scarping all li tag
    container = driver.find_element(By.ID, 'jsMainList')
    elements = container.find_elements(By.TAG_NAME, 'li')

    result = pd.DataFrame()

    with st.spinner("scraping main page"):
        for li in elements:
            news_info = li.find_element(By.TAG_NAME, 'a').text
            title, timestamp = re.search(r"(.*)(\d{4}/\d{2}/\d{2} \d{2}:\d{2})", news_info, re.DOTALL).groups()
            url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
            result.loc[len(result), ['title', 'timestamp', 'url']] = [title.strip(), timestamp, url]

    
    # driver.quit()
    BOX = st.empty()
    bar = st.progress(0, "(0%)scraping...")
    with st.spinner("scraping news content..."):
    
        for _, row in result.iterrows():
            BOX.empty()
            with BOX.container():
            # try:
            #     driver = get_driver()                             
            # except:
            #     driver = webdriver.Chrome()
                time.sleep(random.uniform(1,5))
                driver.get(result.loc[_, 'url'])
                driver.implicitly_wait(20)
                body = driver.find_element(By.CLASS_NAME, 'article')
                driver.implicitly_wait(20)
                content = body.find_elements(By.CLASS_NAME, 'paragraph')[0].text
               
                    
                
                
                result.loc[_, 'content'] = content
                st.dataframe(result[['title', 'content', 'timestamp', 'url']])
            bar.progress((_ + 1) / len(result), f"({round((_ + 1) / len(result) * 100)}%) scraping...")
            

        # driver.quit()
    bar.empty()

    st.write(len("".join(result['content'])))
    # st.dataframe(result)
    driver.quit()

        