from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from modules.reservation.domain.reservation import Reservation

class IReservationRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, reservation_id: UUID) -> Optional[Reservation]:
        """Obtener una reserva por su ID"""
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[Reservation]:
        """Obtener todas las reservas de un cliente"""
        pass

    @abstractmethod
    def get_active_by_user_and_time(self, user_id: UUID, start_time: datetime, end_time: datetime) -> List[Reservation]:
        """Obtener reservas activas de un usuario en un rango de tiempo"""
        pass

    @abstractmethod
    def get_active_by_table_and_time(self, table_id: UUID, start_time: datetime, end_time: datetime) -> List[Reservation]:
        """Obtener reservas activas para una mesa en un rango de tiempo"""
        pass

    @abstractmethod
    def save(self, reservation: Reservation) -> Reservation:
        """Crear una nueva reserva"""
        pass

    @abstractmethod
    def update(self, reservation: Reservation) -> Reservation:
        """Actualizar una reserva existente (ej: cancelar, confirmar, completar)"""
        pass

    @abstractmethod
    def delete(self, reservation_id: UUID) -> None:
        """Eliminar una reserva"""
        pass

    @abstractmethod
    def get_all_by_restaurant(self, restaurant_id: UUID) -> List[Reservation]:
        """Obtener todas las reservas de un restaurante (solo admin)"""
        pass

    @abstractmethod
    def get_by_date_range(self, start: datetime, end: datetime) -> List[Reservation]:
        """Obtener todas las reservas en un rango de fechas"""
        pass
