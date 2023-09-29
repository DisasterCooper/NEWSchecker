from datetime import datetime

from celery.app import shared_task

from news.models import NewsSource, News
from chatgpt.translator import Translator
from parser.sport_express import SportExpressParser


@shared_task()
def parse_sports_express():
    """
    Task for the site `www.sport-express.ru`.
    """
    # Получение или создание источника новостей
    # Второй параметр `_` => возвращает `True` или `False` не нужен => поэтому просто `_`
    source, _ = NewsSource.objects.get_or_create(
        source="sport-express.ru",
        defaults={
            "link": "https://www.sport-express.ru/football/spain/",
        },
    )

    # Получение `datetime` последней новости для данного источника
    if News.objects.filter(source=source).order_by("-published").exists():
        last_news_datetime: datetime = (
            News.objects.filter(source=source)
            .order_by("-published")
            .latest("published")
            .published
        )
    else:
        last_news_datetime = datetime.fromtimestamp(0)

    parser = SportExpressParser()  # do Parser
    all_news = parser.get_last_news(from_datetime=last_news_datetime)

    for one_news in all_news:
        # Translator
        one_news["title"] = Translator(one_news["title"]).to_eng()
        one_news["content"] = Translator(one_news["content"]).to_eng()

        # NewsType содержит такие же поля, как и модель News =>
        # распаковка словаря через **
        News.objects.create(**one_news, source=source)
