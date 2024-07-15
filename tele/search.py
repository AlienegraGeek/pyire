import requests
from bs4 import BeautifulSoup
import json
import sys
import logging
from rich.logging import RichHandler
from rich import print as rprint
from rich.console import Console
from urllib.parse import urljoin

logging.basicConfig(level="NOTSET", handlers=[RichHandler()])
logger = logging.getLogger("rich")


def search_telegram_chat_groups(keyword):
    url = f'https://tdirectory.me/search/{keyword}#groups'
    # url = f'https://tdirectory.me/search/geopolitics#groups'
    response = requests.get(url)
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


def search_telegram_chat_groups2(keyword):
    url = f'https://telegramchannels.me/?s={keyword}'
    response = requests.get(url)
    if response.status_code != 200:
        rprint(f"Failed to retrieve data: {response.status_code}")
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


def transform_link(link):
    base_url = "https://telegram.me/"
    if link.startswith("/group/"):
        username = link.split("/group/")[1].split(".")[0]
        return urljoin(base_url, username)
    elif link.startswith("/channel/"):
        return None
    return link


def search_group(keyword):
    # keyword = sys.argv[1]
    groups = search_telegram_chat_groups(keyword)
    transformed_groups = []
    for group in groups:
        new_link = transform_link(group['link'])
        group['link'] = transform_link(group['link'])
        if new_link:
            group['link'] = new_link
            transformed_groups.append(group)
    console = Console()
    # console.print_json(json.dumps(groups))
    rprint(json.dumps(transformed_groups, indent=2))
