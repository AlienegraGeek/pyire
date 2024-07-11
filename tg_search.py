import requests
from bs4 import BeautifulSoup
import json


def search_telegram_chat_groups(keyword):
    # url = f'https://tdirectory.me/search/{keyword}#groups'
    url = f'https://tdirectory.me/search/geopolitics#groups'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    inner_groups = []
    for group in soup.find_all('div', class_='tg-channel-item'):
        title = group.find('h4').text.strip()
        link = group.find('a', class_='btn')['href']
        description = group.find('p').text.strip()
        inner_groups.append({
            'title': title,
            'link': link,
            'description': description
        })
    return inner_groups


def search_telegram_chat_groups2(keyword):
    url = f'https://telegramchannels.me/?s={keyword}'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    groups = []
    for group in soup.find_all('div', class_='featured-channel'):
        title = group.find('div', class_='featured-channel-title').text.strip()
        link = group.find('a', class_='btn')['href']
        description = group.find('div', class_='featured-channel-description').text.strip()
        groups.append({
            'title': title,
            'link': link,
            'description': description
        })
    return groups


if __name__ == "__main__":
    import sys

    keyword = sys.argv[1]
    groups = search_telegram_chat_groups(keyword)
    print(json.dumps(groups, indent=2))
    print(json.dumps(groups))
