from loguru import logger

from django.conf import settings
from tg_bot.database.base import Base  # какую передавать сюда базу??
from news.models import News, NewsSource
from joining_parser import JoiningParser
from sport_express import SportExpressParser

# SECONDS_TO_REFRESH_NEWS = 60.0

settings.configure()


def get_title_news(parsers: list[JoiningParser]) -> list[News]:
    """Loads news from all sources."""
    all_news_titles = []
    for parser in parsers:
        all_news_titles += parser.get_titles_news()
    return all_news_titles


if __name__ == '__main__':

    logger.info('Application is started.')

    news_sources: list[NewsSource] = [
        SportExpressParser(),  # TODO передать MundoDeportivoParser
        ]

    database = Base()  # какую базу вызывать??
    database.insert_news_sources(news_sources)

    # while True:
    #     titles = get_title_news(news_sources)
    #     new_titles = database.filter_out_old_headlines(titles)
    #     database.insert_headlines(new_titles)
    #     logger.info(f'{len(titles)} titles are downloaded. '
    #                 f'{len(new_titles)} of them are new.')
    #     time.sleep(SECONDS_TO_REFRESH_NEWS)
