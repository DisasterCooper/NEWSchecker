import requests
from bs4 import BeautifulSoup
import json


def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.",

        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.5810.220 Safari/537.36"
    }

    req = requests.get(url=url, headers=headers)
    src = req.text

    with open("index.html", "w") as file:
        file.write(src)

    with open("index.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_titles = soup.find_all("div", class_="se-material__title")
    for title_url in all_titles:
        title_url = title_url.find("a").get("href")
        print(title_url)


def main():
    get_data("https://www.sport-express.ru/football/spain/")


if __name__ == '__main__':
    main()
