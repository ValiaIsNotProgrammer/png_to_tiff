import os
from PIL import Image
from loguru import logger


def get_images_from(dir_: str):
    files = [os.path.join(dir_, filename) for filename in os.listdir(dir_)]
    return files


def to_tiff(dir_: str):
    images = get_images_from(dir_)
    combine_images(columns=round(len(images)/2), space=20, images=images, dir_=dir_)


def combine_images(columns, space, images, dir_):

    #  рефернс: https://stackoverflow.com/questions/72723928/how-to-combine-several-images-to-one-image-in-a-grid-structure-in-python

    logger.info("Конвертация изображений в один .tiff файл")

    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    width_max = max([Image.open(image).width for image in images])
    height_max = max([Image.open(image).height for image in images])
    background_width = width_max*columns + (space*columns)-space
    background_height = height_max*rows + (space*rows)-space
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(image)
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        background.paste(img, (x+x_offset, y+y_offset))
        x += width_max + space
        if (i+1) % columns == 0:
            y += height_max + space
            x = 0

    filename = os.path.join(dir_, 'Result.tiff')
    background.save(filename)
    logger.success(f"Конвертация прошла успешна. Файл {filename} сохранен")

