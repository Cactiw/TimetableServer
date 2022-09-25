from sqlalchemy.orm import Session

from model.PeopleUnion import PeopleUnion


def get_create_group(db: Session, name: str, parent_name, thread_num) -> PeopleUnion:
    true_name = name.lower().strip()
    group = db.query(PeopleUnion).filter_by(name=true_name).first()
    if group is None:
        parent = db.query(PeopleUnion).filter_by(name=parent_name).first()
        parent_thread = None
        if parent is None:
            parent = PeopleUnion(name=parent_name, type_id=1)
            db.add(parent)
            db.commit()

            parent_thread = PeopleUnion(name=f"{thread_num} поток", type_id=2, parent=parent)
            db.add(parent_thread)
            db.commit()
        if not parent_thread:
            parent_thread = list(filter(lambda thread: str(thread_num) in thread.name, parent.children))[0]
        group = PeopleUnion(name=true_name, parent=parent_thread, type_id=3)
        db.add(group)
        db.commit()
    return group
