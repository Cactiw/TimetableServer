from sqlalchemy.orm import Session

from model.Pair import Pair
from model.User import User


def count_timetable_score(session: Session):
    pairs = session.query(Pair).filter(Pair.pair_to_change_id.is_(None)).all()
    teachers = set(map(lambda p: p.teacher, pairs))
    teachers_2 = session.query(User).filter(User.role == User.TEACHER).all()
    if None in teachers:
        teachers.remove(None)
    print(teachers)

    score = 0
    for teacher in teachers:
        teacher_pairs = list(filter(lambda p: p.teacher == teacher, pairs))
        pairs_divided = list(map(
            lambda day_of_week: list(sorted(
                filter(lambda p: p.begin_time.weekday() == day_of_week, teacher_pairs),
                key=lambda p: p.begin_time.time()
            )),
            range(7)
        ))
        print(pairs_divided)

        for day_of_week, day_pairs in enumerate(pairs_divided):
            if 0 < len(day_pairs) < 3:
                score += 0.1

    return score

