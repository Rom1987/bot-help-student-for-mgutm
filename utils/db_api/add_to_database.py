from utils.db_api.db_commands import add_item

import asyncio

from utils.db_api.database import create_db


# Используем эту функцию, чтобы заполнить базу данных товарами
async def add_items():
    await add_item(name="Бакалавриат",
                   category_name="Выбрать профессию", category_code="Choose a profession",
                   photo="Бакалавриат.jpg")
    await add_item(name="Магистратура",
                   category_name="Выбрать профессию", category_code="Choose a profession",
                   photo="Магистратура.jpg")

    imageElectronics = "Electronics_image.jpg"
    await add_item(name="Xiaomi",
                   category_name="🔌 Электроника", category_code="Electronics",
                   photo=imageElectronics)

    imageAds = "Ads_image.jpg"
    await add_item(name="PewDiePie",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   photo=imageAds)
    await add_item(name="Топлес",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   photo=imageAds)
    await add_item(name="Орлёнок",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   photo=imageAds)
    await add_item(name="МДК",
                   category_name="🛍 Услуги Рекламы", category_code="Ads",
                   photo=imageAds)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())
