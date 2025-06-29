from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.pre_order_item import PreOrderItem
from typing import Optional, List

class MenuServices:
    def __init__(self, menu_repo: MenuRepositoryInterface):
        self.menu_repo = menu_repo

# Caso de uso: Obtener menu item por categoría
    def get_menu_item_by_category(self, category: str) -> Optional[MenuItem]:
        if not category:
            raise ValueError("Category is required")
        return self.menu_repo.get_menu_item_by_category(category)

# Caso de uso: Obtener todos los menu items disponibles
    def get_available_menu_item(self) -> List[MenuItem]:
        return self.menu_repo.get_available_menu_item()

# Caso de uso: Obtener todos los pre-order items para una reserva específica
    def get_pre_order_items_by_reservation(self, reservation_id: str) -> List[PreOrderItem]:
        if not reservation_id:
            raise ValueError("Reservation ID is required")
        return self.menu_repo.get_pre_order_items_by_reservation(reservation_id)

# Caso de uso: Crear multiple pre-order items
    def create_pre_order_items(self, items: List[PreOrderItem]) -> List[PreOrderItem]:
        if not items:
            raise ValueError("Items are required")
        return self.menu_repo.create_pre_order_items(items)

# Caso de uso: Crear menu item
    def create_menu_item(self, menu_item: MenuItem) -> MenuItem:
        if not menu_item:
            raise ValueError("Menu item is required")
        return self.menu_repo.create_menu_item(menu_item)

# Caso de uso: Modificar menu item
    def modify_menu_item(self, menu_item: MenuItem) -> MenuItem:
        if not menu_item:
            raise ValueError("Menu item is required")
        return self.menu_repo.modify_menu_item(menu_item)

# Caso de uso: Eliminar menu item
    def delete_menu_item(self, menu_item_id: str) -> None:
        if not menu_item_id:
            raise ValueError("Menu item ID is required")
        self.menu_repo.delete_menu_item(menu_item_id)
