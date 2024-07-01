import asyncio
import sys

from loguru import logger

from utils.yandex import download_from_url
from utils.files import to_tiff


async def main(dirs: list[str]):
    for dir_ in dirs:
        await download_from_url(dir_)
        to_tiff(dir_)


def get_list_from_args(args: str) -> list[str]:
    clear_args = sys.argv[1].replace("[", "").replace("]", "")
    dirs = list(clear_args.split(','))
    check_dirs(dirs)
    return dirs


def check_dirs(dirs: list[str]):
    assert len(dirs) > 0
    for dir_ in dirs:
        assert dir_


if __name__ == "__main__":
    logger.info("Скрипт запущен")

    dirs = get_list_from_args(sys.argv[1])
    asyncio.run(main(dirs))





