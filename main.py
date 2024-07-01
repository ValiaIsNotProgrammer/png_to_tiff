import asyncio

from loguru import logger

from utils.yandex import download_from_url
from utils.files import to_tiff


async def main(dirs: list[str]):
    for dir_ in dirs:
        await download_from_url(dir_)
        to_tiff(dir_)


if __name__ == "__main__":
    logger.info("Скрипт запущен")
    dirs = [
        '1369_12_Наклейки 3-D_3',
        '1388_12_Наклейки 3-D_3',
        '1388_2_Наклейки 3-D_1',
        '1388_6_Наклейки 3-D_2'
            ]
    asyncio.run(main(dirs))





