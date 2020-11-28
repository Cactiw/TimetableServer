#!/bin/python

from model.exceptions.EmptyPairException import EmptyPairException

from functools import reduce

import xlrd
import re
import pprint as pp


def get_book_by_path(path):
    return xlrd.open_workbook(path)


def get_book_by_file(file):
    return xlrd.open_workbook(file_contents=file, on_demand=False)


def get_sheet(book, num):
    return book.sheet_by_index(num)


def get_day(sheet, num):
    # Getting raw day data
    day_dirty = [[i for i in sheet.row_values(j)] for j in range(2 + num % 10 + num * 10, 13 + num % 10 + num * 10)]

    day = [day_dirty[0]]

    for i in range(2, len(day_dirty), 2):
        # Appending time
        day.append([day_dirty[i-1][0]])
        for j in range(1, len(day_dirty[i])):
            day[i//2].append([day_dirty[i-1][j], day_dirty[i][j]])
    return day


def get_groups(sheet):
    return get_day(sheet, 0)[0][1:]


def get_group_day(day, num):
    group = [day[0][0]]
    for i in range(1, len(day)):
        group.append([day[i][0], day[i][1 + int(num) - int(day[0][1])]])
    return group


def get_group(sheet, num):
    return [get_group_day(get_day(sheet, i), num) for i in range(5)]


def generate_pretty_group(l: list):
    res = []
    for day_of_week, day_info in enumerate(l):
        day_name, timetable = day_info[0], day_info[1:]
        for pair_data in timetable:
            try:
                res.append({"dayOfWeek": day_of_week, **parse_pair(pair_data)})
            except EmptyPairException:
                pass
    return res


def parse_pair(pair_data: list) -> dict:
    pair_time, (pair_subject, pair_teacher) = pair_data
    pair_auditorium = None

    if not pair_subject and not pair_teacher:
        raise EmptyPairException()

    # Поиск скорректированного времени в расписании
    corrected_time = re.match("(\\d+\\.\\d+ \\- \\d+\\.\\d+) (.+)", pair_subject)
    if corrected_time is not None:
        pair_time, pair_subject = corrected_time.groups()

    if not pair_teacher:
        return make_dict(pair_time, pair_subject, pair_teacher, None)

    short_teacher = re.search("(\\w+ \\w\\.[\\w ]\\.?)\\s+(\\w+)", pair_teacher)
    if short_teacher is not None:
        pair_teacher, pair_auditorium = short_teacher.groups()
    else:
        pair_auditorium = pair_subject.split()[-1]
        pair_subject = " ".join(pair_subject.split()[:-1])
    return make_dict(pair_time, pair_subject, pair_teacher, pair_auditorium)


def make_dict(pair_time, pair_subject, pair_teacher, pair_auditorium) -> dict:
    return {"time": pair_time, "subject": " ".join(pair_subject.split()).strip(),
            "teacher": pair_teacher.strip(), "pair_auditorium": pair_auditorium}


def parse_xls(file=None, path=None):
    printer = pp.PrettyPrinter()
    if file:
        book = get_book_by_file(file)
    else:
        book = get_book_by_path(path)
    sheet = get_sheet(book, 0)
    groups = get_groups(sheet)
    group = get_group(sheet, 207)
    printer.pprint(group)
    # result = [get_day(sheet, i) for i in range(5)]
    result = reduce(lambda d, cur_group: dict({cur_group: generate_pretty_group(get_group(sheet, cur_group)), **d}),
                    groups, {})
    printer.pprint(result)
    return result
    # day = get_day(sheet, 1)
    # printer.pprint(group)
