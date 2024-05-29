from aiogram import types, Dispatcher
from aiogram.filters import Command

from functions import validate
from script import agregate

dp = Dispatcher()


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(f"Hi, {message.from_user.first_name}")


@dp.message()
async def output(message: types.Message):
    if not (await validate(message)):
        await message.answer("""Невалидный запрос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": 
                "2022-12-31T23:59:00", "group_type": "month"}""")
    else:
        answer = await agregate(eval(message.text))
        await message.answer(answer)