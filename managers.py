from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import streamlit as st 

class ChromeDriverManager:

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    
    def install_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=ChromeDriverManager.options,
        )

    def get_driver():
        try:
            driver = ChromeDriverManager.install_driver()        # *** On streamlit cloud
        except:
            driver = webdriver.Chrome()  # *** On local

        return driver