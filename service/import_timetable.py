from typing import List

from sqlalchemy.orm import Session

from service.auditoriums import get_create_auditorium
from service.people_union import get_create_group

from natty import DateParser


async def import_timetable(db: Session, parsed_timetable: dict, thread_num: int) -> List[str]:
    errors = []
    for group_name, group_tt in parsed_timetable.items():
        group = get_create_group(db, group_name, f"{group_name[:1]} курс", thread_num)
        dp = DateParser('last monday')
        monday = dp.result().date

        for pair_data in group_tt:
            auditorium_name = pair_data.get('pair_auditorium')
            auditorium = None
            if auditorium_name:
                auditorium = get_create_auditorium(db, pair_data['pair_auditorium'])
            teacher = None
            pass

