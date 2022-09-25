from sqlalchemy.orm import Session

from model.Auditorium import Auditorium


def get_create_auditorium(db: Session, name: str) -> Auditorium:
    true_name = name.lower().strip()
    auditorium = db.query(Auditorium).filter_by(name=true_name).first()
    if auditorium is None:
        auditorium = Auditorium(name=true_name)
        db.add(auditorium)
        db.commit()
    return auditorium
