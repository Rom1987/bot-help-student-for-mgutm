from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from keyboards.inline.menu_keyboards import menu_cd, categories_keyboard, \
    items_keyboard, item_keyboard
from loader import dp
from utils.db_api.db_commands import get_item


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await list_categories(message)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await categories_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        splash_screen = open("./media/Заставка.jpg", 'rb')
        await message.answer_photo(photo=splash_screen,
                                   caption="Смотри, что у нас есть", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        media = InputMediaPhoto(
            media='https://pbs.twimg.com/media/EXL3ll8XYAUghMI.jpg:large',
            caption="Смотри, что у нас есть")
        await call.message.edit_media(
            media=media,
            reply_markup=markup
        )


# Функция, которая отдает кнопки с Названием и ценой товара, по выбранной категории и подкатегории
async def list_items(callback: CallbackQuery, category, **kwargs):
    markup = await items_keyboard(category)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    media = InputMediaPhoto(
        media='https://lapkins.ru/upload/uf/f79/f795e55cc07bda34c64a596af9ac28e1.jpg',
        caption="Смотри, что у нас есть")
    await callback.message.edit_media(
        media=media,
        reply_markup=markup
    )


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_item(callback: CallbackQuery, category, item_id):
    markup = item_keyboard(category, item_id)

    # Берем запись о нашем товаре из базы данных
    item = await get_item(item_id)
    text = f"Купи {item.name}"
    # Отправляем фотку товара с подписью и кнопкой "купить"
    dir_media = "./media/" + item.category_code + "/" + item.photo
    media = InputMediaPhoto(media=open(dir_media, 'rb'), caption=text)
    await callback.message.edit_media(
        media=media,
        reply_markup=markup
    )


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category = callback_data.get("category")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    item_id = int(callback_data.get("item_id"))

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_categories,  # Отдаем категории
        "1": list_items,  # Отдаем товары
        "2": show_item  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        category=category,
        item_id=item_id
    )
