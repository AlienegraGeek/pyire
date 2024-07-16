import codecs
import posixpath
import re
from itertools import chain
from urllib.parse import urljoin
import random
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
from lxml import etree


class CreateMarkdown:
    """ Create GitHub Markdown """

    def __init__(self):
        self.url = 'https://github.com/AlienegraGeek/pyire'
        self.template_file = '../_template.md'

    def readme_handler(self):
        readme_url = posixpath.join(self.url, "blob/main/README.md")
        response = requests.get(readme_url)
        if response.status_code != 200:
            print(f"Failed to fetch README: {response.status_code}")
            return
        html = etree.HTML(response.text)
        elements = html.xpath('//*[contains(@href,"t.me")]/@href')
        for element in elements:
            yield element.replace('\\"', '')

    def issues_handler(self):
        issues_url = posixpath.join(self.url, "issues")
        response = requests.get(issues_url)
        if response.status_code != 200:
            print(f"Failed to fetch issues: {response.status_code}")
            return
        html = etree.HTML(response.text)
        elements = html.xpath("//div[contains(@role,'group')]//a[contains(@id,'issue_')]/@href")
        for element in elements:
            issues_title_url = urljoin(self.url, element)
            iss_resp = requests.get(issues_title_url)
            iss_html = etree.HTML(iss_resp.text)
            iss_elements = iss_html.xpath("//a[contains(@href,'t.me')]/@href")[0]
            yield iss_elements

    def url_join(self, *args):
        return chain(*args)

    def get_info(self, urls):
        for idx, url in enumerate(urls):
            print(idx, ' ---> ', url)
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch URL: {url} with status code {response.status_code}")
                continue
            html = etree.HTML(response.text)

            tg_me_page_url = url

            try:
                tg_me_page_title_raw = dict(enumerate(html.xpath(
                    "//div[contains(@class,'tgme_page')]//div[contains(@class,'tgme_page_title')]//span/text()"))).get(
                    0)
                tg_me_page_title = tg_me_page_title_raw.replace('|', '')
            except:
                continue

            tg_me_page_extra = dict(enumerate(
                html.xpath(
                    "//div[contains(@class,'tgme_page')]//div[contains(@class,'tgme_page_extra')]/text()"))).get(
                0)

            try:
                tg_me_page_description_raw = dict(enumerate(html.xpath(
                    "//div[contains(@class,'tgme_page')]//div[contains(@class,'tgme_page_description')]/text()"))).get(
                    0)
                if 'If you have' in tg_me_page_description_raw:
                    continue

                tg_me_page_description = tg_me_page_description_raw.replace('|', '')

            except Exception as e:
                print(f"Error fetching description: {e}")
                tg_me_page_description = None

            # 数据处理
            tg_me_audience = None
            tg_me_category = None
            if '@' in tg_me_page_extra:
                tg_me_category = '机器人'
                tg_me_audience = None
            elif 'subscribers' in tg_me_page_extra:
                tg_me_category = '频道'
                tg_me_audience = re.match(r'\d+', re.sub(' ', '', tg_me_page_extra)).group()
            elif 'members' in tg_me_page_extra:
                tg_me_category = '群组'
                tg_me_audience = re.match(r'\d+', re.sub(' ', '', tg_me_page_extra)).group()

            yield {
                'tg_me_page_url': tg_me_page_url,
                'tg_me_page_title': tg_me_page_title,
                'tg_me_audience': tg_me_audience,
                'tg_me_page_description': tg_me_page_description,
                'tg_me_category': tg_me_category,
            }

    # def create_md(self, repo):
    #     if not repo:
    #         print("No data to create markdown.")
    #         return
    #     with open('_template.md', 'r', encoding='utf-8') as file:
    #         template = Template(file.read(), trim_blocks=True)
    #         rendered_file = template.render(repo=repo)
    #         output_file = codecs.open("README.md", "w", "utf-8")
    #         output_file.write(rendered_file)
    #         output_file.close()
    #     print("Markdown file created successfully.")

    def create_md(self, groups):
        with open(self.template_file, 'r', encoding='utf-8') as file:
            template = Template(file.read(), trim_blocks=True)
            rendered_file = template.render(groups=groups)
            output_file = codecs.open("../README.md", "w", "utf-8")
            output_file.write(rendered_file)
            output_file.close()
        print("Markdown file created successfully.")

    def shuffle(self, generator):
        lst = list(generator)
        lst = list(set(lst))
        random.shuffle(lst)
        return (y for y in lst)

    def search_telegram_chat_groups(self, keyword):
        url = 'https://github.com/AlienegraGeek/pyire'
        response = requests.get(url)
        if response.status_code != 200:
            # rprint(f"Failed to retrieve data: {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')

        inner_groups = []
        for group in soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12 item-div'):
            title = group.find('h4').text.strip()
            link = group.find('a')['href']
            description_tag = group.find_all('p')[1] if len(group.find_all('p')) > 1 else None
            description = description_tag.get_text(separator=' ', strip=True) if description_tag else ""
            members_tag = group.find('i', class_='fa fa-group item-icon')
            members_text = members_tag.find_parent().text if members_tag else ""
            members_match = re.search(r'(\d[\d,]*)', members_text)
            members = members_match.group(1) if members_match else "N/A"
            inner_groups.append({
                'title': self.escape_markdown(title),
                'link': self.escape_markdown(link),
                'description': self.escape_markdown(description),
                'members': self.escape_markdown(members),
                'keyword': self.escape_markdown(keyword),
            })
        return inner_groups

    def transform_link(self, link):
        base_url = "https://telegram.me/"
        if link.startswith("/group/"):
            username = link.split("/group/")[1].split(".")[0]
            return urljoin(base_url, username)
        elif link.startswith("/channel/"):
            return None
        return link

    def escape_markdown(self, text):
        return text.replace('|', '\\|')

    def search_group(self, keyword):
        groups = self.search_telegram_chat_groups(keyword)
        transformed_groups = []
        for group in groups:
            new_link = self.transform_link(group['link'])
            group['link'] = self.transform_link(group['link'])
            if new_link:
                group['link'] = new_link
                transformed_groups.append(group)
        # console = Console()
        # rprint(json.dumps(transformed_groups, indent=2))
        return transformed_groups

    def start(self):
        # issues = self.issues_handler()
        # readme = self.readme_handler()
        # urls = self.url_join(issues, readme)
        # suf = self.shuffle(urls)
        # info = self.get_info(suf)
        # if not info:
        #     print("No information fetched.")
        # self.create_md(info)
        keyword = "geopolitics"
        groups = self.search_group(keyword)
        self.create_md(groups)


if __name__ == '__main__':
    cm = CreateMarkdown()
    cm.start()
