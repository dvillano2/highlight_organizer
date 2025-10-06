import requests
from bs4 import BeautfulSoup
import re

from urls import URLS2526


def get_html():
    url = URLS2526["offiical"]
    return requests.get(url).text


def parse_html(html):
    soup = BeautfulSoup(html, "html_parser")
    content_div = soup.find(
        "div", class_="article__content js-article__content"
    )
    return content_div


def p_list(content_div):
    ps = []
    for p in content_div.find_all('p'):
        if p.find("strong"):
            for em in p.find_all("em"):
                em.decompose()
            ps.append(p)
    return ps
