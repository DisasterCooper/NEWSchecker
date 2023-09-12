from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import ResultSet, Tag

from news.models import News, NewsSource


class JoiningParser(ABC):
    """
    Abstract class for all sources of news.
    """

    def __init__(self):
        self.source = self._create_source()

    def get_titles_news(self) -> list[News]:
        """Returns titles of the News from chosen source."""
        try:
            response = requests.get(self.source.link, timeout=4)
            response.raise_for_status()
        except requests.RequestException:
            return []
        return self._parse_response(response.text)

    def get_last_news(self) -> list[dict]:
        raise NotImplementedError("This method should be implemented in subclasses")

    def _parse_response(self, response_text: str) -> list[News]:
        titles = []
        for title_item in self._get_title_items(response_text):
            title = self._parse_title_item(title_item)
            if title is not None:
                titles.append(title)
        return titles

    def _parse_title_item(self, item: Tag) -> News | None:
        try:
            link = self._get_link(item)
            title = self._get_title(item)
            published_at = self._get_published_at(item)
        except Exception:
            # if any error occurs, then this title is not valid
            return None
        return News(self.source.id_name, link, title, published_at)

    @abstractmethod
    def _create_source(self) -> NewsSource:
        pass

    @abstractmethod
    def _get_title_items(self, response_text: str) -> ResultSet[Tag]:
        pass

    def _get_title(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_content(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_link(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_published_at(self, item: Tag) -> datetime:
        pass
