import requests
from bs4 import BeautifulSoup
import json


def search_telegram_chat_groups3(keyword):
    url = f'https://telegramchannels.me/search?q={keyword}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    groups = []
    for group in soup.find_all('div', class_='group-card'):
        title = group.find('h3').text.strip()
        link = group.find('a', class_='btn')['href']
        description = group.find('p').text.strip()
        groups.append({
            'title': title,
            'link': link,
            'description': description
        })
    return groups


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search_telegram.py <keyword>")
        sys.exit(1)
    keyword = sys.argv[1]
    groups = search_telegram_chat_groups3(keyword)
    print(json.dumps(groups, indent=2))
