from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from modules.restaurant.domain.table import Table

class ITableRepository(ABC):
    @abstractmethod
    def get_by_id(self, table_id: UUID) -> Optional[Table]:
        """Obtener una mesa por su ID."""
        pass

    @abstractmethod
    def get_by_restaurant_id(self, restaurant_id: UUID) -> List[Table]:
        """Obtener todas las mesas de un restaurante por su ID."""
        pass

    @abstractmethod
    def get_by_restaurant_and_table_number(self, restaurant_id: UUID, table_number: int) -> Optional[Table]:
        """Obtener una mesa por el ID del restaurante y el número de mesa."""
        pass

    @abstractmethod
    def save(self, table: Table) -> None:
        """Guardar una mesa en la base de datos."""
        pass
    
    @abstractmethod
    def modify(self, table: Table) -> Table:
        """Modificar una mesa existente."""
        pass

    @abstractmethod
    def delete(self, table_id: UUID) -> None:
        """Eliminar una mesa por su ID."""
        pass

    @abstractmethod
    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[Table]:
        """Obtener mesas disponibles en un restaurante según la capacidad y ubicación."""
        pass
