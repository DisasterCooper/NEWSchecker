from abc import ABC
from datetime import datetime, date

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

    def get_last_news(self) -> list[dict]:
        response = requests.get(self.source.link, timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            news_div = soup.find_all("div", class_="se-grid2col")
            results = []
            for item in news_div:
                title = item.find("h1", class_="se-material-page__title").text.strip()
                link = item.find("h1", class_="se-material-page__title")["href"]
                content = item.find("div", class_="se-material-page__content").text.strip()
                published = item.find("p", class_="se-material-page__date").text.strip()
                # Converting to a datetime object
                published = datetime.strptime(published, "%d.%m.%Y %H:%M")
                if date is None or published.date() == date:
                    results.append({"title": title, "link": link, "content": content, "published": published})
            return results
        else:
            print(f"Error when requesting the page. Response status: {response.status_code}")
