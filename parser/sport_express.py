from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag

from joining_parser import JoiningParser
from news.models import NewsSource


class SportExpressParser(JoiningParser):

    def _create_source(self) -> NewsSource:
        return NewsSource(
            "sport_express",
            "sport-express.ru",
            "https://www.sport-express.ru/football/spain/"
        )

    def get_last_news(self) -> list[dict]:
        response = requests.get(self.source.link, timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            news_div = soup.find_all("div", class_="se-grid2col")
            results = []
            for item in news_div:
                results.append({
                    "title": self._get_title(item),
                    "link": self._get_link(item),
                    "content": self._get_content(item),
                    "published": self._get_published(item)
                })
                print(results)
            return results
        else:
            print(f"Error when requesting the page. Response status: {response.status_code}")
            return []

    def _get_title(self, item: Tag) -> Optional[str]:
        return item.find("h1", class_="se-material-page__title").get_text()

    def _get_content(self, item: Tag) -> Optional[str]:
        return item.find("div", class_="se-material-page__content").get_text()

    def _get_link(self, item: Tag) -> Optional[str]:
        return item.find("h1", class_="se-material-page__title").get("href")

    def _get_published(self, item: Tag) -> datetime:
        published = item.find("p", class_="se-material-page__date").get_text()
        published = datetime.fromisoformat(f"{published[:10]}T{published[11:]}")
        return published
