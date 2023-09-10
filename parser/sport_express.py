from abc import ABC
from datetime import datetime

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from joining_parser import JoiningParser
from news.models import NewsSource


class SportExpressParser(JoiningParser, ABC):

    def _create_source(self) -> NewsSource:
        return NewsSource("sport_express", "sport-express.ru", "https://www.sport-express.ru/football/spain/")

    def _get_title_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "lxml")
        titles_div = soup.find(name="div", class_="se-titled-block__content")
        title_class = "se-material se-material--type-text"
        title_result_soup = titles_div.find_all("title", class_=title_class)
        # print(title_result_soup)
        return title_result_soup
