from aiogram import types


async def validate(message: types.Message):
    try:
        data = eval(message.text)
    except:
        return False
    if "dt_from" not in data or "dt_upto" not in data or "group_type" not in data:
        return False
    return True