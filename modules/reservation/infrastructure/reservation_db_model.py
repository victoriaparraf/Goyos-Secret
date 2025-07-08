from sqlmodel import Column, SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Optional
from modules.reservation.domain.reservation import Reservation, ReservationStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB

class ReservationDBModel(SQLModel, Reservation, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    table_id: UUID = Field(foreign_key="tabledbmodel.id", index=True)
    start_time: datetime
    end_time: datetime
    num_people: int
    special_instructions: Optional[str] = None
    status: ReservationStatus = Field(default=ReservationStatus.PENDING)
    # Relación muchos a muchos con PreOrderItemDB
    pre_orders: List["PreOrderItemDB"] = Relationship(back_populates="reservation")

def to_domain(res: ReservationDBModel) -> Reservation:
    return Reservation(
        uuid=res.uuid,
        user_id=res.user_id,
        table_id=res.table_id,
        start_time=res.start_time,
        end_time=res.end_time,
        num_people=res.num_people,
        special_instructions=res.special_instructions,
        # pre_orders es la relación, puedes mapearla si lo necesitas
        status=res.status
    )

def to_db(res: Reservation) -> ReservationDBModel:
    return ReservationDBModel(
        uuid=res.uuid,
        user_id=res.user_id,
        table_id=res.table_id,
        start_time=res.start_time,
        end_time=res.end_time,
        num_people=res.num_people,
        special_instructions=res.special_instructions,
        status=res.status
    )
