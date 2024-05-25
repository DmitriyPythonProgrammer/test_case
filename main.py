import bson
from dateutil.parser import parse
import datetime
import calendar
import pymongo
# pymongo, хоть напрямую не используется, нужен для работы функции decode_all библиотеки bson

testcase = {
    "input": {
        "dt_from": "2022-10-01T00:00:00",
        "dt_upto": "2022-11-30T23:59:00",
        "group_type": "day"
    },
    "output": {
        "dataset": [0, 0, 0, 195028, 190610, 193448, 203057, 208605, 191361, 186224, 181561, 195264, 213854, 194070,
            208372, 184966, 196745, 185221, 196197, 200647, 196755, 221695, 189114, 204853, 194652, 188096, 215141,
            185000, 206936, 200164, 188238, 195279, 191601, 201722, 207361, 184391, 203336, 205045, 202717, 182251,
            185631, 186703, 193604, 204879, 201341, 202654, 183856, 207001, 204274, 204119, 188486, 191392, 184199,
            202045, 193454, 198738, 205226, 188764, 191233, 193167, 205334],
        "labels": [
            "2022-10-01T00:00:00", "2022-10-02T00:00:00", "2022-10-03T00:00:00", "2022-10-04T00:00:00",
               "2022-10-05T00:00:00", "2022-10-06T00:00:00", "2022-10-07T00:00:00", "2022-10-08T00:00:00",
               "2022-10-09T00:00:00", "2022-10-10T00:00:00", "2022-10-11T00:00:00", "2022-10-12T00:00:00",
               "2022-10-13T00:00:00", "2022-10-14T00:00:00", "2022-10-15T00:00:00", "2022-10-16T00:00:00",
               "2022-10-17T00:00:00", "2022-10-18T00:00:00", "2022-10-19T00:00:00", "2022-10-20T00:00:00",
               "2022-10-21T00:00:00", "2022-10-22T00:00:00", "2022-10-23T00:00:00", "2022-10-24T00:00:00",
               "2022-10-25T00:00:00", "2022-10-26T00:00:00", "2022-10-27T00:00:00", "2022-10-28T00:00:00",
               "2022-10-29T00:00:00", "2022-10-30T00:00:00", "2022-10-31T00:00:00", "2022-11-01T00:00:00",
               "2022-11-02T00:00:00", "2022-11-03T00:00:00", "2022-11-04T00:00:00", "2022-11-05T00:00:00",
               "2022-11-06T00:00:00", "2022-11-07T00:00:00", "2022-11-08T00:00:00", "2022-11-09T00:00:00",
               "2022-11-10T00:00:00", "2022-11-11T00:00:00", "2022-11-12T00:00:00", "2022-11-13T00:00:00",
               "2022-11-14T00:00:00", "2022-11-15T00:00:00", "2022-11-16T00:00:00", "2022-11-17T00:00:00",
               "2022-11-18T00:00:00", "2022-11-19T00:00:00", "2022-11-20T00:00:00", "2022-11-21T00:00:00",
               "2022-11-22T00:00:00", "2022-11-23T00:00:00", "2022-11-24T00:00:00", "2022-11-25T00:00:00",
               "2022-11-26T00:00:00", "2022-11-27T00:00:00", "2022-11-28T00:00:00", "2022-11-29T00:00:00",
               "2022-11-30T00:00:00"
        ]
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
        # Берем следующий промежуток
        left = right

#Тест
assert end_result == testcase["output"]