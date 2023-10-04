from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup, Tag

from joining_parser import JoiningParser, NewsType


class MundoDeportivoParser(JoiningParser, ABC):
    def get_web_link(self) -> str:
        return "https://www.mundodeportivo.com/futbol/fc-barcelona"

    def get_last_news(self, from_datetime: datetime) -> list[NewsType]:
        results = []
        response = requests.get(self.get_web_link(), timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "lxml")
            news_div = soup.find_all("li", class_="result-news")

            with ThreadPoolExecutor(max_workers=len(news_div)) as request_executor:
                # Find links to news.
                # Execute add_news for performance in multithreading.
                # The number of threads is determined by the number of found news.
                for news in news_div:
                    request_executor.submit(
                        self.add_news, str(news["data-url"]), from_datetime, results
                    )

            return results
        else:
            print(
                f"Error when requesting the page. Response status: {response.status_code}"
            )
            return []

    def add_news(self, url: str, from_datetime: datetime, result_list: list[NewsType]):
        print(url)
        response = requests.get(url, timeout=4)
        if response.status_code != 200:
            return

        news_soup = BeautifulSoup(response.text, "lxml")

        published_datetime = self._get_published(news_soup)
        if published_datetime <= from_datetime:
            return

        # Check if there is content and add news
        if self._has_content(news_soup):
            result_list.append(
                {
                    "title": self._get_title(news_soup),
                    "link": url,
                    "content": self._get_content(news_soup),
                    "published": published_datetime,
                }
            )
            print("added")

    def _get_title(self, item: Tag) -> str:
        title = item.find("h1", class_="title")
        # strip=True для удаления пробельных символов в начале и конце текста
        return title.get_text(strip=True) if title else ""

    def _get_content(self, item: Tag) -> str:
        content = item.find("div", class_="article-modules")
        if content is None:
            return ""
        # Find all CSS links on the page
        links = item.find_all("link", attrs={"rel": "stylesheet"})
        # Combine into a single string
        styles_link = "".join(map(str, links))
        # Remove the block that will not be displayed
        exclude = content.find("iframe")
        if exclude:
            exclude.decompose()

        return styles_link + str(content).strip()

    def _get_published(self, item: Tag) -> datetime:
        published = item.find("div", class_="date-time")

        if published is not None:
            return datetime.strptime(published.get_text(strip=True), "%Y-%m-%d %H:%M:%S")
        else:
            return datetime.now()

    def _has_content(self, item: Tag) -> bool:
        content = item.find("div", class_="article-modules")
        return content is not None
