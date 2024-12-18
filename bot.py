import asyncio
import logging
import sqlite3
import random
import sys

from typing import Any, Dict
from aiogram import Bot, Dispatcher, types, Router, F, html
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv
from aiogram.fsm.storage.memory import MemoryStorage




logging.basicConfig(level=logging.INFO)


router = Router()
bot = Bot(token='7943694116:AAHiz46pWD86pke4WhgVsXHqtKI2i13vOmo')
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)




def main_kb():
    kb_list = [
            [KeyboardButton(text="/кб"), KeyboardButton(text="/баланс")]
        ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,resize_keyboard=True,one_time_keyboard=True)
    return keyboard
@dp.message(Command('start'))
async def start_com(message: Message):
    await message.answer("Бот ",reply_markup=main_kb())





@router.message(Command('кб'))
async def start_cmd(message: types.Message):
    
    await bot.send_chat_action(message.chat.id, 'typing')
    msg = await message.answer_sticker('CAACAgIAAxkBAAENCn5nIRbp17LyzOpbHvncU8Vg8oAJawAC324AAp7OCwABhEHLNbbuyeg2BA')
    
    name = message.from_user.username
    con = sqlite3.connect("tgbot.db")
    cursor = con.cursor()
    cursor.execute('SELECT user_name FROM idkoin WHERE user_name = ?', (f'{name}',))
    data = cursor.fetchone()

    if data is None:
        con = sqlite3.connect("tgbot.db")
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO idkoin(user_name, koin) VALUES ('{name}', 100)")
        con.commit()
    await asyncio.sleep(1)
    works = ["Поражение", "Победа"]
    random_work = random.choice(works)
    await msg.delete()
    
    cursor.execute(f"SELECT * FROM idkoin WHERE user_name = '{name}'")  
    row = cursor.fetchone()  
    koin = row[1]
    if random_work == "Победа":
        print("Победа")
        koin = koin + 10
        cursor.execute(f"UPDATE idkoin set koin = {koin} where user_name = '{name}'")
        con.commit()
        await message.reply(f"{random_work}! {koin}")
        con.close()
        
    if random_work == "Поражение":
        print("Поражение")
        koin = koin - 10
        cursor.execute(f"UPDATE idkoin set koin = {koin} where user_name = '{name}'")
        con.commit()
        await message.reply(f"{random_work}! {koin}")
        con.close()
    

    





@router.message(Command('баланс'))
async def start(message: types.Message):
    name = message.from_user.username
    con = sqlite3.connect("tgbot.db")
    cursor = con.cursor()
    cursor.execute('SELECT user_name FROM idkoin WHERE user_name = ?', (f'{name}',))
    data = cursor.fetchone()

    if data is None:
        con = sqlite3.connect("tgbot.db")
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO idkoin(user_name, koin) VALUES ('{name}', 100)")
        con.commit()
    name = message.from_user.username
    con = sqlite3.connect("tgbot.db")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM idkoin WHERE user_name = '{name}'") 
    row = cursor.fetchone()  
    koin = row[1]
    await message.reply("Ваш баланс: " + str(koin))
    con.close()
    
    
   










async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
   