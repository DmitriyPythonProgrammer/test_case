import bson
from dateutil.parser import parse
import datetime
import calendar
import pymongo
# pymongo, хоть напрямую не используется, нужен для работы функции decode_all библиотеки bson

testcase = {
    "input": {
       "dt_from": "2022-02-01T00:00:00",
       "dt_upto": "2022-02-02T00:00:00",
       "group_type": "hour"
    },
    "output": {
        "dataset": [8177, 8407, 4868, 7706, 8353, 7143, 6062, 11800, 4077, 8820, 4788, 11045, 13048, 2729, 4038, 9888,
            7490, 11644, 11232, 12177, 2741, 5341, 8730, 4718, 0],
        "labels": ["2022-02-01T00:00:00", "2022-02-01T01:00:00", "2022-02-01T02:00:00", "2022-02-01T03:00:00",
           "2022-02-01T04:00:00", "2022-02-01T05:00:00", "2022-02-01T06:00:00", "2022-02-01T07:00:00",
           "2022-02-01T08:00:00", "2022-02-01T09:00:00", "2022-02-01T10:00:00", "2022-02-01T11:00:00",
           "2022-02-01T12:00:00", "2022-02-01T13:00:00", "2022-02-01T14:00:00", "2022-02-01T15:00:00",
           "2022-02-01T16:00:00", "2022-02-01T17:00:00", "2022-02-01T18:00:00", "2022-02-01T19:00:00",
           "2022-02-01T20:00:00", "2022-02-01T21:00:00", "2022-02-01T22:00:00", "2022-02-01T23:00:00",
           "2022-02-02T00:00:00"]

    }
}
# Левая граница
left = parse(testcase["input"]["dt_from"])
# Правая граница общего промежутка
end = parse(testcase["input"]["dt_upto"])

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
        if testcase["input"]["group_type"] == "month":
            right = left + datetime.timedelta(days=calendar.monthrange(left.year, left.month)[1])

        elif testcase["input"]["group_type"] == "day":
            right = left + datetime.timedelta(days=1)

        elif testcase["input"]["group_type"] == "hour":
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

#Тест
assert end_result == testcase["output"]
