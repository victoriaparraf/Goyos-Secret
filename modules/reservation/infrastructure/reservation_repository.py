from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from modules.reservation.domain.reservation_repository_interface import IReservationRepository
from modules.reservation.domain.reservation import Reservation
from modules.restaurant.infrastructure.table_db_model import TableDBModel
from modules.reservation.infrastructure.reservation_db_model import ReservationDBModel, to_domain, to_db

class ReservationRepository(IReservationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        res = self.db.get(ReservationDBModel, reservation_id)
        return to_domain(res) if res else None

    def get_by_user(self, user_id: UUID) -> List[Reservation]:
        stmt = select(ReservationDBModel).where(ReservationDBModel.user_id == user_id)
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def get_active_by_user_and_time(self, user_id: UUID, start_time: datetime, end_time: datetime) -> List[Reservation]:
        stmt = select(ReservationDBModel).where(
            (ReservationDBModel.user_id == user_id) &
            (ReservationDBModel.start_time < end_time) &
            (ReservationDBModel.end_time > start_time) &
            (ReservationDBModel.status.in_(["PENDING", "CONFIRMED"]))
        )
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def get_active_by_table_and_time(self, table_id: UUID, start_time: datetime, end_time: datetime) -> List[Reservation]:
        stmt = select(ReservationDBModel).where(
            (ReservationDBModel.table_id == table_id) &
            (ReservationDBModel.start_time < end_time) &
            (ReservationDBModel.end_time > start_time) &
            (ReservationDBModel.status.in_(["PENDING", "CONFIRMED"]))
        )
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def save(self, reservation: Reservation) -> Reservation:
        db_res = to_db(reservation)
        self.db.add(db_res)
        self.db.commit()
        self.db.refresh(db_res)
        return to_domain(db_res)

    def update(self, reservation: Reservation) -> Reservation:
        db_res = self.db.get(ReservationDBModel, reservation.uuid)
        if not db_res:
            raise Exception("Reservation not found")

        updated = to_db(reservation)
        for field, value in updated.model_dump().items():
            setattr(db_res, field, value)

        self.db.add(db_res)
        self.db.commit()
        self.db.refresh(db_res)
        return to_domain(db_res)

    def delete(self, reservation_id: UUID) -> None:
        db_res = self.db.get(ReservationDBModel, reservation_id)
        if db_res:
            self.db.delete(db_res)
            self.db.commit()

    def get_all_by_restaurant(self, restaurant_id: UUID) -> List[Reservation]:
        stmt = select(ReservationDBModel).join_from(ReservationDBModel, TableDBModel).where(
            TableDBModel.restaurant_id == restaurant_id
        )
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def get_by_date_range(self, start: datetime, end: datetime) -> List[Reservation]:
        stmt = select(ReservationDBModel).where(
            (ReservationDBModel.start_time >= start) &
            (ReservationDBModel.start_time <= end)
        )
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def get_all(self) -> List[Reservation]:
        stmt = select(ReservationDBModel)
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]

    def get_active_by_restaurant_and_time_range(self, restaurant_id: UUID, start_time: datetime, end_time: datetime) -> List[Reservation]:
        stmt = select(ReservationDBModel).join_from(ReservationDBModel, TableDBModel).where(
            (TableDBModel.restaurant_id == restaurant_id) &
            (ReservationDBModel.start_time < end_time) &
            (ReservationDBModel.end_time > start_time) &
            (ReservationDBModel.status.in_(["PENDING", "CONFIRMED"]))
        )
        results = self.db.exec(stmt).all()
        return [to_domain(r) for r in results]
