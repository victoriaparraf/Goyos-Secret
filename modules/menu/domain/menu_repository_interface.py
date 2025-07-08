from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.pre_order_item import PreOrderItem


class MenuRepositoryInterface(ABC):
    
    @abstractmethod
    def get_all_by_restaurant(self, restaurant_id: UUID) -> List[MenuItem]:
        """Obtiene todos los menu items de un restaurante"""
        pass
    
    @abstractmethod
    def get_menu_item_by_category(self, category: str) -> Optional[MenuItem]:
        """Obtiene un menu item por su categoria"""
        pass

    @abstractmethod
    def get_menu_item_by_name(self, name: str) -> Optional[MenuItem]:
        """Obtiene un menu item por su nombre"""
        pass

    @abstractmethod
    def get_available_menu_item(self) -> List[MenuItem]:
        """Obtiene todos los menu items disponibles"""
        pass

    @abstractmethod
    def get_pre_order_items_by_reservation(self, reservation_id: str) -> List[PreOrderItem]:
        """Obtiene todos los pre-order items para una reserva específica"""
        pass

    @abstractmethod
    def create_pre_order_items(self, items: List[PreOrderItem]) -> List[PreOrderItem]:
        """Crea multiple pre-order items"""
        pass

    @abstractmethod
    def create_menu_item(self, menu_item: MenuItem) -> MenuItem:
        """Crea un menu item"""
        pass

    @abstractmethod
    def modify_menu_item(self, menu_item: MenuItem) -> MenuItem:
        """Actualiza un menu item"""
        pass

    @abstractmethod
    def delete_menu_item(self, menu_item_id: str) -> None:
        """Elimina un menu item"""
        pass
    
    @abstractmethod
    def save_pre_order_item(self, pre_order_item):
        """
        Guarda un PreOrderItemDB en la base de datos.
        Debe ser implementado por la clase concreta del repositorio.
        """
        raise NotImplementedError