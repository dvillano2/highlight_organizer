from typing import Dict
from typing import Union
from typing import Optional
import re
import json
import requests
from bs4 import BeautifulSoup

UrlsDictType = Dict[str, Union[str, Dict[str, str]]]


def get_urls() -> UrlsDictType:
    with open("schedule_urls.json", "r", encoding="utf=8") as f:
        urls = json.load(f)
    return urls


def get_response(
    mw_or_beginnig: str, urls: UrlsDictType, mw_num: Optional[int] = None
) -> requests.Response:
    if mw_or_beginnig == "beginning":
        url = urls["season_start"]
    else:
        by_mw = urls.get("by_mw")
        assert isinstance(by_mw, dict)
        if isinstance(mw_num, int):
            url = by_mw[str(mw_num)]
        else:
            raise ValueError("Need a mw number to if getting urls by mw")
    return requests.get(url)


# For season start/beginning data


def info_list(ps):
    return [
        sub_p.text.replace("*", "")
        for p in ps
        for sub_p in p
        if str(sub_p) != "<br/>"
    ]


def remove_parentheses(info_list):
    return [re.sub(r" *\(.*\)", "", info) for info in info_list]


def parse_beginning_response(response: requests.Response):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find(
        "div", class_="article__content js-article__content"
    )

    ps = []
    for p in content_div.find_all("p"):
        if p.find("strong"):
            ps.append(p)

    info = info_list(ps)
    return remove_parentheses(info)

# For by mw data

def parse_by_mw_respone(response: requests.Response) -> Dict:
    return json.loads(response.text)
