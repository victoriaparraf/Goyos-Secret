from uuid import UUID, uuid4
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import HTTPException
from modules.reservation.domain.reservation import Reservation, ReservationStatus
from modules.reservation.domain.reservation_repository_interface import IReservationRepository
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.reservation.application.dtos.reservation_create_dto import ReservationCreateDto
from modules.reservation.application.dtos.reservation_response_dto import ReservationResponseDto
from modules.notifications.notifications import notificacion
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository

class ReservationService:
    def __init__(
        self,
        reservation_repo: IReservationRepository,
        table_repo: ITableRepository,
        menu_repo: MenuRepositoryInterface,
        restaurant_repo: IRestaurantRepository
    ):
        self.reservation_repo = reservation_repo
        self.table_repo = table_repo
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    @notificacion("Reserva confirmada para {fecha} en {restaurante}.", data_extractor=lambda r: {"fecha": r.start_time.strftime("%Y-%m-%d %H:%M"), "restaurante": r.restaurant_name})
    def create_reservation(self, user_id: UUID, dto: ReservationCreateDto) -> ReservationResponseDto:
        # Validar duración
        duration = dto.end_time - dto.start_time
        if duration > timedelta(hours=4) or duration.total_seconds() <= 0:
            raise HTTPException(status_code=400, detail="Invalid reservation duration (max 4 hours).")

        # Validar mesa existente
        table = self.table_repo.get_by_id(dto.table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found.")
        
        restaurant = self.restaurant_repo.get_by_id(table.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found for this table.")

        # Validar que no haya solapamiento por cliente
        overlapping_user = self.reservation_repo.get_active_by_user_and_time(user_id, dto.start_time, dto.end_time)
        if overlapping_user:
            raise HTTPException(status_code=409, detail="You already have a reservation in this time slot.")

        # Validar que no haya solapamiento por mesa
        overlapping_table = self.reservation_repo.get_active_by_table_and_time(dto.table_id, dto.start_time, dto.end_time)
        if overlapping_table:
            raise HTTPException(status_code=409, detail="This table is already reserved at that time.")

        # Validar platos (si existen)
        if dto.preordered_dishes:
            if len(dto.preordered_dishes) > 5:
                raise HTTPException(status_code=400, detail="Cannot pre-order more than 5 dishes.")
            menu_items = self.menu_repo.get_all_by_restaurant(table.restaurant_id)
            menu_ids = {dish.id for dish in menu_items if dish.available_stock > 0}
            for dish_id in dto.preordered_dishes:
                if dish_id not in menu_ids:
                    raise HTTPException(status_code=400, detail=f"Dish {dish_id} is not available for this restaurant.")
            # Notificación de pre-orden
            from modules.notifications.notifications import registrar_preorden
            registrar_preorden(n_platos=len(dto.preordered_dishes))

        reservation = Reservation(
            uuid=uuid4(),
            user_id=user_id,
            table_id=dto.table_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            num_people=dto.num_people,
            special_instructions=dto.special_instructions,
            status=ReservationStatus.PENDING
        )

        saved = self.reservation_repo.save(reservation)
        response_dto_data = saved.model_dump()
        response_dto_data["preordered_dishes"] = dto.preordered_dishes
        if not restaurant: # Defensive check
            raise HTTPException(status_code=500, detail="Restaurant information missing after initial check.")
        response_dto_data["restaurant_name"] = restaurant.name
        return ReservationResponseDto(**response_dto_data)

    @notificacion("Reserva cancelada (ID: {id_reserva}).", data_extractor=lambda r: {"id_reserva": r.uuid})
    def cancel_reservation(self, reservation_id: UUID, current_user_id: UUID, is_admin: bool = False) -> None:
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found.")

        if not is_admin and reservation.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="You can only cancel your own reservations.")

        # Cliente solo puede cancelar si falta al menos 1 hora
        if not is_admin:
            if reservation.start_time <= datetime.utcnow() + timedelta(hours=1):
                raise HTTPException(status_code=400, detail="You can only cancel at least 1 hour in advance.")

        reservation.status = ReservationStatus.CANCELLED
        self.reservation_repo.update(reservation)
        return reservation

    def get_reservations_by_user(self, user_id: UUID) -> List[ReservationResponseDto]:
        reservations = self.reservation_repo.get_by_user(user_id)
        return [ReservationResponseDto(**r.model_dump()) for r in reservations]

    def get_reservation_by_id(self, reservation_id: UUID) -> ReservationResponseDto:
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found.")
        return ReservationResponseDto(**reservation.model_dump())

    def get_all_by_restaurant(self, restaurant_id: UUID) -> List[ReservationResponseDto]:
        reservations = self.reservation_repo.get_all_by_restaurant(restaurant_id)
        return [ReservationResponseDto(**r.model_dump()) for r in reservations]

    def get_by_date_range(self, start: datetime, end: datetime) -> List[ReservationResponseDto]:
        reservations = self.reservation_repo.get_by_date_range(start, end)
        return [ReservationResponseDto(**r.model_dump()) for r in reservations]
