import asyncio
import logging
import os
import re

from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from sqlalchemy.exc import NoResultFound

from tg_bot.tg_models import News, User
from tg_bot.database.connection import db


# Включение логирования, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TG_TOKEN"))

dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "Привет! Я бот для отправки спортивных новостей о чемпионате Испании." \
           "Список доступных команд:" \
           "\n/start - начать работу" \
           "\n/news - получить топ новостей" \
           "\n/status - посмотреть статистику своего профиля" \
           "\n/help - список команд"
    await message.answer(text)


def remove_html_tags_content(text: str) -> str:
    bs = BeautifulSoup(text, "lxml")
    return re.sub(r"\s{2}", '', bs.get_text())


@dp.message(Command("news"))
async def cmd_get_news(message: types.Message):

    all_news = await News.get_all()
    last_five_news = all_news[-5:]
    answer_text = ""

    for news in last_five_news:
        content = remove_html_tags_content(news.content)
        answer_text += f"<a href=\"http://127.0.0.1:8000/news/{news.id}\">{news.title}</a>\n{content}\n\n"

    await message.answer(answer_text, parse_mode="html")
    # await message.answer("Your fresh news!")


@dp.message(Command("status"))
async def status(message: types.Message) -> None:
    try:
        user = await User.get(tg_id=message.from_user.id)
    except NoResultFound:
        await message.answer("Зарегистрируйтесь на сайте ....")

    else:
        await message.answer(
            f"Вы зарегистрированы на сайте:\n"
            f"{user.username}, {user.id}, {user.date_joined}"
        )


# Запуск процесса поллинга новых апдейтов
async def main():
    db.init()  # Подключение к базе
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
