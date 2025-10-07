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


def info_list(ps):
    return [
        sub_p.text.replace("*", "")
        for p in ps
        for sub_p in p
        if str(sub_p) != "<br/>"
    ]


def remove_parentheses(info_list):
    return [re.sub(r" *\(.*\)", "", info) for info in info_list]

def organize(info_nop):
    matchweek = None
    day_of_week = None
    day = None
    month = None
    year = None
    


def test():
    html = get_html()
    content_div = parse_html(html)
    ps = p_list(content_div)
    info = info_list(ps)
    info_nop = remove_parentheses(info)
    for line in info_nop:
        print(line)
