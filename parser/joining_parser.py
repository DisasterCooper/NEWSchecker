from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypedDict
from bs4 import Tag


class NewsType(TypedDict):
    """
    Helps to understand the type of news dictionary.
    """
    title: str
    link: str
    content: str
    published: datetime


class JoiningParser(ABC):
    """
    Abstract class for all sources of news.
    """

    @abstractmethod
    def get_last_news(self, from_datetime: datetime) -> list[NewsType]:
        """
        Returns last news from chosen source.
        """
        raise NotImplementedError("This method should be implemented in subclasses")

    @abstractmethod
    def get_web_link(self) -> str:
        pass

    @abstractmethod
    def _get_title(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_content(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_published(self, item: Tag) -> datetime:
        pass
