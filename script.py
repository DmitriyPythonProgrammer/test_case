import bson
from dateutil.parser import parse
import datetime
import calendar
import pymongo


# pymongo, хоть напрямую не используется, нужен для работы функции decode_all библиотеки bson
async def agregate(input: eval) -> eval:
    # Левая граница
    left = parse(input["dt_from"])
    # Правая граница общего промежутка
    end = parse(input["dt_upto"])

    end_result = {
        "dataset": [],
        "labels": []
    }

    with open('sample_collection.bson', 'rb') as file:
        data = bson.decode_all(file.read())
        # Сдвигаем левую границу к правой, пока левая меньше правой.
        while left < end:
            result = 0
            # Не во всех месяцах 30 дней, поэтому с помощью calendar определяем. И берем правую границу.
            if input["group_type"] == "month":
                right = left + datetime.timedelta(days=calendar.monthrange(left.year, left.month)[1])

            elif input["group_type"] == "day":
                right = left + datetime.timedelta(days=1)

            elif input["group_type"] == "hour":
                right = left + datetime.timedelta(hours=1)

            # Проходимся по бд и ищем то, что входит в промежуток
            for item in data:
                if left <= item["dt"] < right:
                    result += item["value"]

            # Записываем конечных результат
            end_result["dataset"].append(result)
            end_result["labels"].append(parse(str(left)).isoformat())

            # Обрабатываем исключения
            if end == right and str(end.time()) == "00:00:00":
                end_result["dataset"].append(0)
                end_result["labels"].append(parse(str(right)).isoformat())

            # Берем следующий промежуток
            left = right

    return end_result
