import requests
from bs4 import BeautifulSoup
import json


def search_telegram_chat_groups(keyword):
    url = f'https://telegramchannels.me/?s={keyword}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    groups = []
    for group in soup.find_all('div', class_='group-card'):
        title = group.find('h3').text
        link = group.find('a', class_='join-btn')['href']
        description = group.find('p').text.strip()
        if 'chat' in description.lower() or 'group' in description.lower():
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
    print(json.dumps(groups))
