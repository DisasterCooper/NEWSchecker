from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup, Tag

from .joining_parser import JoiningParser, NewsType


class SportExpressParser(JoiningParser):
    def get_web_link(self) -> str:
        return "https://www.sport-express.ru/football/spain/"

    def get_last_news(self, from_datetime: datetime) -> list[NewsType]:
        results = []
        response = requests.get(self.get_web_link(), timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode("utf-8", "ignore"), "lxml")
            news_div = soup.find_all("li", class_="se-mainnews-item")

            with ThreadPoolExecutor(max_workers=len(news_div)) as request_executor:
                # Находит ссылки на новости.
                # Выполнение add_news для производительности в многопотоке.
                # Кол-во потоков определяется по кол-ву найденных новостей
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
        if published_datetime.timestamp() <= from_datetime.timestamp():
            return

        # Проверить, что есть содержимое и можно добавлять новость

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
        title = item.find("h1", class_="se-material-page__title")
        return title.get_text() if title is not None else ""

    def _get_content(self, item: Tag) -> str:
        content = item.find("div", class_="se-material-page__content")
        if content is None:
            return ""
        # Нахождение на странице всех ссылок на CSS
        links = item.find_all("link", attrs={"rel": "stylesheet"})
        # Объединение в одну строку
        styles_link = "".join(map(str, links))
        # Удаление блока, который не будет отражаться
        exclude = content.find("iframe")
        if exclude:
            exclude.decompose()

        # Формирование изображения для команды
        for team_image in content.find_all("img", class_="se-compot-team_imager") or []:
            team_image["src"] = "https:" + team_image["data-lazy"]

        return styles_link + str(content).strip()

    def _get_published(self, item: Tag) -> datetime:
        months_dict = {
            "января": "January",
            "февраля": "February",
            "марта": "March",
            "апреля": "April",
            "мая": "May",
            "июня": "June",
            "июля": "July",
            "августа": "August",
            "сентября": "September",
            "октября": "October",
            "ноября": "November",
            "декабря": "December",
        }
        published = item.find("p", class_="se-material-page__date")
        # Получение строки и превращение в объект datetime
        if published is not None:
            # Разбивка на строку по `, `
            # Проверка на наличие "Сегодня", либо деление "15 сентября" на число и месяц
            news_datetime = published.get_text()
            date_, time_ = news_datetime.split(", ")
            if date_ == "Сегодня":
                date_str = datetime.now().strftime("%d %B")
            else:
                day, ru_month = date_.split()
                date_str = f"{day} {months_dict.get(ru_month)}"
            # Формирование строки в формате "15 September 2023 22:23"
            return datetime.strptime(
                f"{date_str} {datetime.now().year} {time_}", "%d %B %Y %H:%M"
            )

        return datetime.fromtimestamp(0)
