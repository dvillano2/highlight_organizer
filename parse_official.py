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
