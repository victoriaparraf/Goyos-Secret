from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from modules.restaurant.domain.restaurant import Restaurant

class IRestaurantRepository(ABC):
    @abstractmethod
    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        """Obtiene un restaurante por su ID"""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Restaurant]:
        """Obtiene un restaurante por su nombre"""
        pass

    @abstractmethod
    def save(self, restaurant: Restaurant) -> None:
        """Guarda un restaurante"""
        pass

    @abstractmethod
    def delete(self, restaurant_id: UUID) -> None:
        """Elimina un restaurante por su ID"""
        pass
