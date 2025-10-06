import requests
from bs4 import BeautifulSoup
import re

from urls import URLS2526


def get_html():
    url = URLS2526["official"]
    return requests.get(url).text


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find(
        "div", class_="article__content js-article__content"
    )
    return content_div


def p_list(content_div):
    ps = []
    for p in content_div.find_all("p"):
        if p.find("strong"):
            for em in p.find_all("em"):
                em.decompose()
            ps.append(p)
    return ps


def info_list(p_list):
    return [sub_p.text for p in p_list for sub_p in p if str(sub_p) != "<br/>"]
