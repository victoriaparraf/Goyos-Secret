from sqlmodel import Session, select
from typing import Optional, List

from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface   
from modules.menu.infrastructure.menu_item_db_model import MenuItemDB
from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB
from modules.menu.domain.pre_order_item import PreOrderItem


class MenuRepository(MenuRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_menu_item_by_category(self, category: str) -> Optional[MenuItem]:
        statement = select(MenuItemDB).where(MenuItemDB.category == category)
        result = self.db.exec(statement).first()
        return result

    def get_available_menu_item(self) -> List[MenuItem]:
        statement = select(MenuItemDB).where(MenuItemDB.available_stock > 0)
        result = self.db.exec(statement).all()
        return result

    def get_pre_order_items_by_reservation(self, reservation_id: str) -> List[PreOrderItem]:
        statement = select(PreOrderItemDB).where(PreOrderItemDB.reservation_id == reservation_id)
        result = self.db.exec(statement).all()
        return result

    def create_pre_order_items(self, items: List[PreOrderItem]) -> List[PreOrderItem]:
        for item in items:
            self.db.add(item)
        self.db.commit()
        return items

    def create_menu_item(self, menu_item: MenuItem) -> MenuItem:
        self.db.add(menu_item)
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def modify_menu_item(self, menu_item: MenuItem) -> MenuItem:
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def delete_menu_item(self, menu_item_id: str) -> None:
        menu_item = self.db.get(MenuItemDB, menu_item_id)
        if menu_item:
            self.db.delete(menu_item)
            self.db.commit()

