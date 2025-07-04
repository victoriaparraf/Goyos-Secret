from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from modules.restaurant.domain.table import Table

class ITableRepository(ABC):
    @abstractmethod
    def get_by_id(self, table_id: UUID) -> Optional[Table]:
        pass

    @abstractmethod
    def get_by_restaurant_id(self, restaurant_id: UUID) -> List[Table]:
        pass

    @abstractmethod
    def get_by_restaurant_and_table_number(self, restaurant_id: UUID, table_number: int) -> Optional[Table]:
        pass

    @abstractmethod
    def save(self, table: Table) -> None:
        pass

    @abstractmethod
    def delete(self, table_id: UUID) -> None:
        pass

    @abstractmethod
    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[Table]:
        pass
