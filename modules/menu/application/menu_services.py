from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.pre_order_item import PreOrderItem
from typing import Optional, List
from uuid import UUID

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
    def create_menu_item(self, name: str, description: str, category: str, price: float, available_stock: int, restaurant_id: UUID, image_url: Optional[str] = None) -> MenuItem:
        from uuid import uuid4
        if not name or not description or not category or price is None or available_stock is None or not restaurant_id:
            raise ValueError("All fields except image_url are required")

        # El nombre debe ser único dentro del mismo restaurante
        menu_items = self.menu_repo.get_all_by_restaurant(restaurant_id)
        for item in menu_items:
            if item.name.lower() == name.lower():
                from fastapi import HTTPException
                raise HTTPException(status_code=409, detail="Menu item with this name already exists in this restaurant.")

        menu_item = MenuItem(
            id=uuid4(),
            name=name,
            description=description,
            category=category,
            price=price,
            available_stock=available_stock,
            restaurant_id=restaurant_id,
            image_url=image_url
        )
        return self.menu_repo.create_menu_item(menu_item)

# Caso de uso: Modificar menu item
    def modify_menu_item(self, menu_item_id: str, name: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, price: Optional[float] = None, available_stock: Optional[int] = None, image_url: Optional[str] = None) -> MenuItem:
        if not menu_item_id:
            raise ValueError("Menu item ID is required")
        existing_item = self.menu_repo.get_menu_item_by_id(menu_item_id)
        if not existing_item:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Menu item not found.")

        # Solo actualiza los campos que no son None
        update_data = {
            "name": name if name is not None else existing_item.name,
            "description": description if description is not None else existing_item.description,
            "category": category if category is not None else existing_item.category,
            "price": price if price is not None else existing_item.price,
            "available_stock": available_stock if available_stock is not None else existing_item.available_stock,
            "image_url": image_url if image_url is not None else existing_item.image_url,
        }
        updated_item = MenuItem(
            id=existing_item.id,
            **update_data
        )
        return self.menu_repo.modify_menu_item(updated_item)

# Caso de uso: Eliminar menu item
    def delete_menu_item(self, menu_item_id: str) -> None:
        if not menu_item_id:
            raise ValueError("Menu item ID is required")
        self.menu_repo.delete_menu_item(menu_item_id)
