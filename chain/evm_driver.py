import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rich import print as rprint


def evm_data_driver():
    chromedriver_path = '/Users/yuvan/Downloads/chromedriver-mac-x64/chromedriver'

    # 设置 Chrome 选项
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://evm.ink/address/0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        # page source
        page_content = driver.page_source
        # soup = BeautifulSoup(page_content, 'html.parser')
        root_element = driver.find_element(By.ID, "root")
        data_elements = root_element.find_elements(By.XPATH, ".//*")
        h1_elements = root_element.find_elements(By.CSS_SELECTOR,
                                                 "h1.text-2xl.font-bold.text-blue-600.uppercase.dark\\:text-blue-400")
        h1_elements = driver.find_elements(By.CSS_SELECTOR, "h1")
        for tr in h1_elements:
            rprint(tr.text)

    finally:
        driver.quit()


def baidu_driver():
    url = "https://evm.ink/address/0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303"
    # url = 'http://www.baidu.com'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver_path = '/Users/yuvan/Downloads/chromedriver-mac-x64/chromedriver'
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(url)
    print('open success')
    input('')
