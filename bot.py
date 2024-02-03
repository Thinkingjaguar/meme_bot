import asyncio
import random
import os
import uuid
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from keyboard import get_choose_tag, for_admins
from aiogram.types import FSInputFile
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()
admins = [5602350846, 1506907277]
separator = '/'

'''--------------- ОСНОВНАЯ РАБОТА ----------------'''


@dp.message(Command('start'))
async def start(message: types.Message):
    await sending_main_message(message.from_user.id)


@dp.callback_query(F.data == 'tag_study')
@dp.callback_query(F.data == 'tag_music')
@dp.callback_query(F.data == 'tag_prog')
@dp.callback_query(F.data == 'tag_neprog')
async def kartinochka_smotret(callback: types.CallbackQuery):
    await callback.message.delete()
    captions = {'prog': 'Закрой телеграм и иди дебажить!', 'music': 'А позаниматься спец?', 'study': 'Такие дела',
                'neprog': '-_-'}
    tag = callback.data[4:]
    pict = get_picture(tag)
    await callback.message.answer_photo(FSInputFile(pict), caption=captions[tag])
    await sending_main_message(callback.from_user.id)
    await callback.answer()


def get_picture(tag):
    path = __file__[:__file__.rfind(separator) + 1] + tag + separator
    return path + random.choice(os.listdir(path))


async def sending_main_message(chat_idi):
    await bot.send_message(chat_id=chat_idi, text='Выбери тему:', reply_markup=get_choose_tag())


'''--------------- АДМИНКА ----------------'''


@dp.message(F.photo)
async def add_pict(message: types.Message):
    await message.delete()
    if message.from_user.id not in admins:
        await message.answer('Только админы могут добавлять мемы')
    else:
        pict = __file__[:__file__.rfind(separator) + 1] + 'all' + separator + str(uuid.uuid4())
        await bot.download(message.photo[-1], destination=pict)
        await message.answer_photo(caption='В какую категорию это закинуть?',reply_markup=for_admins(),photo=FSInputFile(pict))


@dp.callback_query(F.data == 'add_study')
@dp.callback_query(F.data == 'add_music')
@dp.callback_query(F.data == 'add_prog')
@dp.callback_query(F.data == 'add_neprog')
async def kartinochka_dobavlat(callback: types.CallbackQuery):
    await callback.message.delete()
    path = __file__[:__file__.rfind(separator) + 1] + callback.data[4:] + separator + str(uuid.uuid4()) + '.png'
    await bot.download(callback.message.photo[-1], destination=path)
    await callback.message.answer('Успешно добавлено')
    await sending_main_message(callback.from_user.id)
    await callback.answer()

'''----------------- ЗАПУСК -------------------'''


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())