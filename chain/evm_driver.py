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
        embedded_html_match = re.search(r'(<tr class="text-left border-b-2 text-md dark:text-white border-b-stone-800">.*?</tr>)', page_content, re.DOTALL)
        if embedded_html_match:
            embedded_html = embedded_html_match.group(1)

            # 使用 BeautifulSoup 解析提取出的 HTML 字符串
            soup = BeautifulSoup(embedded_html, 'html.parser')

            # 查找并打印 h1 标签
            h1_elements = soup.find_all("h1", class_="text-2xl font-bold text-blue-600 uppercase dark:text-blue-400")
            for h1 in h1_elements:
                print(h1.text)

            # 查找并打印 tr 和 td 标签内容
            tr_elements = soup.find_all("tr", class_="text-left border-b-2 text-md dark:text-white border-b-stone-800")
            for tr in tr_elements:
                print(tr.text)

            td_elements = soup.find_all("td", class_="px-2 py-4")
            for td in td_elements:
                print(td.text)
            # soup = BeautifulSoup(page_content, 'html.parser')
            # root_element = driver.find_element(By.ID, "root")
            # data_elements = root_element.find_elements(By.XPATH, ".//*")
            inner_groups = []
            # for group in soup.find_all('div', class_='text-2xl font-bold text-blue-600 uppercase dark:text-blue-400'):
            # for group in soup.find_all('div', class_='w-full overflow-x-auto rounded-t-3xl'):
            # 查找所有具有特定类名的 <tr> 元素
            # h1_elements = root_element.find_elements(By.CSS_SELECTOR, "h1.text-2xl.font-bold.text-blue-600.uppercase.dark\\:text-blue-400")
            # h1_elements = driver.find_elements(By.CSS_SELECTOR, "h1")
            # for tr in h1_elements:
            #     rprint(tr.text)
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
