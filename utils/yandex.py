import os
from urllib import parse

import aiofiles
import aiohttp
from loguru import logger

from config import PUBLIC_KEY


def get_urls_from(json: dict) -> list[str]:
    items = json['_embedded']['items']
    urls = []
    for item in items:
        url = item['sizes'][0]["url"]
        urls.append(url)
    return urls


async def get_ya_data_from(public_key: str, path: str = None) -> dict:

    logger.info(f"Запрос на получение метаданных с {path}")

    encoded_public_key = parse.quote(public_key, safe='')
    params = {'public_key': encoded_public_key}
    if path:
        params['path'] = '/' + path
    url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, params=params)
    if response.status == 200:

        logger.success(f"Метаданные с {path} успешно получены")

        return await response.json()
    logger.error(f"Не получилось взять метаданные с {path}. Детали: {await response.json()}")


async def download_file(url: str, dir_: str) -> None:
    filename = os.path.basename(url.split("?")[0]) + ".png"
    if not os.path.exists(dir_):
        logger.info(f"Создана директория {dir_}, т.к. ее не существует")
        os.makedirs(dir_)

    async with aiohttp.ClientSession() as session:
        logger.info(f"Запрос на получение файла по адресу {url}")
        async with session.get(url) as response:

            if response.status != 200:
                logger.error(f"Не получилось скачать файл {filename}\n\t{await response.json()}")
                return

            async with aiofiles.open(os.path.join(dir_, filename), "wb") as f:
                logger.info(f"Скачивание файла {filename}")
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        logger.success(f"Файл {os.path.join(dir_, filename)} успешно скачан")
                        break
                    await f.write(chunk)


async def download_files(urls: list[str], dir_: str) -> None:
    for url in urls:
        await download_file(url, dir_)


async def download_from_url(dir_: str) -> None:
    json = await get_ya_data_from(PUBLIC_KEY, path=dir_)
    urls = get_urls_from(json)
    await download_files(urls, dir_)
