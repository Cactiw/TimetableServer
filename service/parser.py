#!/bin/python

from model.exceptions.EmptyPairException import EmptyPairException

from functools import reduce

import xlrd
import re
import pprint as pp


DELETE_TEACHER_WORDS = {
    "доцент", "профессор"
}
teacher_regex = re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, DELETE_TEACHER_WORDS)))


def get_book_by_path(path):
    return xlrd.open_workbook(path, formatting_info=True)


def get_book_by_file(file):
    return xlrd.open_workbook(file_contents=file, formatting_info=True, on_demand=False)


def get_sheet(book, num):
    return book.sheet_by_index(num)


def get_day(sheet, num):
    # Getting raw day data
    merged_cells = sheet.merged_cells # x_start, x_end + 1, y_start, y_end + 1
    day_dirty = []
    for i in range(2 + num % 10 + num * 10, 13 + num % 10 + num * 10):
        day_data = []
        for j, value in enumerate(sheet.row_values(i)):
            day_data.append((value, any(map(
                lambda merge_data: merge_data[0] <= i < merge_data[1] and merge_data[2] <= j < merge_data[3],
                merged_cells
            ))))
        day_dirty.append(day_data)
    # day_dirty = [[i for i in sheet.row_values(j)] for j in range(2 + num % 10 + num * 10, 13 + num % 10 + num * 10)]

    day = [day_dirty[0]]

    for i in range(2, len(day_dirty), 2):
        # Appending time
        day.append([day_dirty[i-1][0]])
        for j in range(1, len(day_dirty[i])):
            day[i//2].append([day_dirty[i-1][j], day_dirty[i][j]])
    return day


def get_groups(sheet):
    return list(map(lambda text_merged: text_merged[0], get_day(sheet, 0)[0][1:]))


def get_group_day(day, num):
    group = [day[0][0]]
    for i in range(1, len(day)):
        group.append([day[i][0], day[i][1 + int(num) - int(day[0][1][0])]])
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
    (pair_time, pair_time_merged), ((pair_subject, pair_subject_merged), (pair_teacher, pair_teacher_merger)) = \
        pair_data
    pair_auditorium = None

    if not pair_subject and not pair_teacher:
        raise EmptyPairException()

    # Поиск скорректированного времени в расписании
    corrected_time = re.match("(\\d+\\.\\d+ \\- \\d+\\.\\d+) (.+)", pair_subject)
    if corrected_time is not None:
        pair_time, pair_subject = corrected_time.groups()

    if not pair_teacher:
        return make_dict(pair_time, pair_subject, pair_teacher, None, pair_subject_merged)

    short_teacher = re.search("(\\w+ \\w\\.[\\w ]\\.?)\\s+(\\w+)", pair_teacher)
    if short_teacher is not None:
        pair_teacher, pair_auditorium = short_teacher.groups()
    else:
        pair_auditorium = pair_subject.split()[-1]
        pair_subject = " ".join(pair_subject.split()[:-1])
    return make_dict(pair_time, pair_subject, pair_teacher, pair_auditorium, pair_subject_merged)


def make_dict(pair_time, pair_subject, pair_teacher, pair_auditorium, pair_subject_merged: bool = False) -> dict:
    if pair_teacher:
        pair_teacher = teacher_regex.sub("", pair_teacher).replace("  ", " ").strip()
    return {
        "time": pair_time.replace(".", ":"), "subject": " ".join(pair_subject.split()).strip(),
        "teacher": pair_teacher.strip(), "pair_auditorium": pair_auditorium,
        "merged": pair_subject_merged
    }


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
