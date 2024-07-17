import codecs
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


def search_teleteg_chat_groups(keyword):
    url = f'https://teleteg.com/search-results/?query={keyword}&filters=groups'
    response = requests.get(url)
    if response.status_code != 200:
        rprint(f"Failed to retrieve data: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    inner_groups = []
    for group in soup.find_all('tr'):
        a_tag = group.find('a')
        link = a_tag['href'] if a_tag else None

        td_tags = group.find_all('td')
        if len(td_tags) > 3:
            title = td_tags[1].get_text(strip=True)
            title = decode_unicode_escape(title)
            description = td_tags[2].get_text(strip=True)
            description = decode_unicode_escape(description)
            members = td_tags[3].get_text(strip=True)
            inner_groups.append({
                'title': title,
                'link': link,
                'description': description,
                'members': members,
                'keyword': keyword
            })
    return inner_groups


def search_teleteg_group(keyword):
    # keyword = sys.argv[1]
    groups = search_teleteg_chat_groups(keyword)
    # console.print_json(json.dumps(groups))
    print(json.dumps(groups, indent=2))


def decode_unicode_escape(text):
    try:
        return text.encode('utf-8').decode('unicode-escape').encode('latin1').decode('utf-8')
    except Exception as e:
        print(f"Decoding error: {e}")
        return text
