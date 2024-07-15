import json

import requests
from bs4 import BeautifulSoup
from rich import print as rprint


def search_evm_data(address):
    # 0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303
    # url = f'https://evm.ink/address/{address}'
    # url = f'https://gapi.evm.ink/v1.InscriptionService/GetBrc20UserBalances'
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                   "Chrome/91.0.4472.124 Safari/537.36"
    # }

    url = "https://gapi.evm.ink/v1.InscriptionService/GetBrc20UserBalances"


    # 设置请求头
    headers = {
        "accept": "*/*",
        "accept-language": "zh,en;q=0.9,zh-CN;q=0.8",
        "authorization": "Bearer undefined",
        "connect-protocol-version": "1",
        "content-type": "application/json",
        "origin": "https://evm.ink",
        "priority": "u=1, i",
        "referer": "https://evm.ink/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    # 设置请求体
    data = {
        "networkId": "eip155:56",
        "ownerAddress": "0xf6372ef94026f71e5e48f0ff2ff5ceb06fdff303",
        "limit": "200"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    # response = requests.get(url)
    # response = requests.get(url, headers=headers)
    if response.status_code != 200:
        rprint(f"Failed to retrieve data: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    inner_groups = []
    for group in soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12 item-div'):
        title = group.find('h4').text.strip()
        link = group.find('a')['href']
        description = group.find('p').text.strip()
        inner_groups.append({
            'title': title,
            'link': link,
            'description': description
        })
    return inner_groups
