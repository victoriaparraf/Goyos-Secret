from sqlmodel import Column, SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Optional
from modules.reservation.domain.reservation import Reservation, ReservationStatus

class ReservationDBModel(SQLModel, Reservation, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    table_id: UUID = Field(foreign_key="tabledbmodel.id", index=True)
    start_time: datetime
    end_time: datetime
    num_people: int
    special_instructions: Optional[str] = None
    preordered_dishes: Optional[List[UUID]] = Field(default_factory=list)
    status: ReservationStatus = Field(default=ReservationStatus.PENDING)

def to_domain(res: ReservationDBModel) -> Reservation:
    return Reservation(
        uuid=res.uuid,
        user_id=res.user_id,
        table_id=res.table_id,
        start_time=res.start_time,
        end_time=res.end_time,
        num_people=res.num_people,
        special_instructions=res.special_instructions,
        preordered_dishes=res.preordered_dishes,
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
        preordered_dishes=res.preordered_dishes,
        status=res.status
    )
