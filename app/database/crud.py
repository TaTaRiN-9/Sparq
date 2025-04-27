from sqlalchemy.orm import Session

from models import test_model as models
import schema

async def create_group_controller(
    db: Session, group: schema.GroupCreate
) -> models.Group:
    new_group = models.Group(address=group.address, name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


async def create_message_controller(
    db: Session, user: models.User, group_id: int, text: str
) -> models.Message:
    message = models.Message(
        text=text, sender_id=user.id, sender_name=user.username, group_id=group_id
    )
    db.add(message)
    db.commit()
    return message


async def group_members_by_id(
    group_id: int,
    db: Session,
) -> list[models.User]:
    return (
        db.query(models.User)
        .join(models.GroupMember)
        .filter(models.GroupMember.group_id == group_id)
        .all()
    )


async def get_group_by_id(
    group_id: int,
    db: Session,
) -> models.Group:
    return db.query(models.Group).filter_by(id=group_id).first()

# поиск чата по его названию
async def get_group_by_address(
    address: str,
    db: Session,
) -> models.Group:
    return db.query(models.Group).filter_by(address=address).first()


async def join_member_to_group(
    db: Session,
    user: schema.User,
    group: models.Group,
    role: schema.UserRole = schema.UserRole.member,
):
    group_member = models.GroupMember(
        user_id=user.id,
        group_id=group.id,
        role=role,
    )
    db.add(group_member)
    db.commit()


async def get_message_by_id(
    message_id: int,
    user_id: int,
    db: Session,
) -> models.Message | None:
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message and user_id == message.sender_id:
        return message
    return None