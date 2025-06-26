from fastapi import APIRouter, Depends, HTTPException, Security
from sqlmodel import Session
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.menu.infrastructure.menu_repository import MenuRepository
from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.pre_order_item import PreOrderItem
from modules.core.db_connection import get_db
from typing import List

router = APIRouter()

def get_menu_repository(db: Session = Depends(get_db)) -> MenuRepositoryInterface:
    repository = MenuRepository(db)
    return MenuRepositoryInterface(repository)

# Caso de uso: Obtener menu item por categoría
@router.get("/menu-item/{category}")
async def get_menu_item_by_category(
    category: str,
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    menu_item = menu_repo.get_menu_item_by_category(category)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {
        "message": "Menu item retrieved successfully", 
        "menu_item": menu_item
    }

# Caso de uso: Obtener todos los menu items disponibles
@router.get("/menu-item")
async def get_available_menu_items(
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    menu_items = menu_repo.get_available_menu_items()
    return {
        "message": "Menu items retrieved successfully", 
        "menu_items": menu_items
    }

# Caso de uso: Obtener todos los pre-order items para una reserva específica
@router.get("/pre-order-item/{reservation_id}")
async def get_pre_order_items_by_reservation(
    reservation_id: str,
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    pre_order_items = menu_repo.get_pre_order_items_by_reservation(reservation_id)
    return {
        "message": "Pre-order items retrieved successfully", 
        "items": pre_order_items
    }

# Caso de uso: Crear multiple pre-order items
@router.post("/pre-order-item")
async def create_pre_order_items(
    items: List[PreOrderItem],
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    created_items = menu_repo.create_pre_order_items(items)
    return {
        "message": "Pre-order items created successfully", 
        "items": created_items
    }

# Caso de uso: Crear menu item
@router.post("/menu-item")
async def create_menu_item(
    menu_item: MenuItem,
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    created_menu_item = menu_repo.create_menu_item(menu_item)
    return {
        "message": "Menu item created successfully", 
        "menu_item": created_menu_item
    }

# Caso de uso: Modificar menu item
@router.put("/menu-item/{menu_item_id}")
async def modify_menu_item(
    menu_item_id: str,
    menu_item: MenuItem,
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    modified_menu_item = menu_repo.modify_menu_item(menu_item_id, menu_item)
    return {
        "message": "Menu item modified successfully", 
        "menu_item": modified_menu_item
    }

# Caso de uso: Eliminar menu item
@router.delete("/menu-item/{menu_item_id}")
async def delete_menu_item(
    menu_item_id: str,
    menu_repo: MenuRepositoryInterface = Depends(get_menu_repository)
):
    menu_repo.delete_menu_item(menu_item_id)
    return {
        "message": "Menu item deleted successfully"
    }

