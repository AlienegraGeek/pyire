import re

import requests
from bs4 import BeautifulSoup
import json
import logging
from rich.logging import RichHandler
from rich import print as rprint
from rich.console import Console
from urllib.parse import urljoin

logging.basicConfig(level="NOTSET", handlers=[RichHandler()])
logger = logging.getLogger("rich")


def search_telegram_chat_groups(keyword):
    url = 'https://github.com/AlienegraGeek/pyire'
    response = requests.get(url)
    if response.status_code != 200:
        rprint(f"Failed to retrieve data: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    inner_groups = []
    for group in soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12 item-div'):
        title = group.find('h4').text.strip()
        link = group.find('a')['href']
        # description = group.find('p').text.strip()
        description_tag = group.find_all('p')[1] if len(group.find_all('p')) > 1 else None
        description = description_tag.get_text(strip=True) if description_tag else ""
        members_tag = group.find('i', class_='fa fa-group item-icon')
        members_text = members_tag.find_parent().text if members_tag else ""
        members_match = re.search(r'(\d[\d,]*)', members_text)
        members = members_match.group(1) if members_match else "N/A"
        inner_groups.append({
            'title': title,
            'link': link,
            'description': description,
            'members': members,
            'keyword': keyword
        })
    return inner_groups


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
