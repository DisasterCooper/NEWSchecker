from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import Tag

from news.models import NewsSource


class JoiningParser(ABC):
    """
    Abstract class for all sources of news.
    """

    def __init__(self):
        self.source = self._create_source()
        self.title = self._get_title()
        self.content = self._get_content()
        self.link = self._get_link()

    @abstractmethod
    def get_last_news(self) -> list[dict]:
        """Returns last news from chosen source."""
        raise NotImplementedError("This method should be implemented in subclasses")

    @abstractmethod
    def _create_source(self) -> NewsSource:
        pass

    @abstractmethod
    def _get_title(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_content(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_link(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_published(self, item: Tag) -> datetime:
        pass
