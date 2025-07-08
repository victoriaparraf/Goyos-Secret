from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID

from modules.menu.domain.menu_item import MenuItem
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface   
from modules.menu.infrastructure.menu_item_db_model import MenuItemDB, to_db, to_domain
from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB, to_db as to_db_pre_order, to_domain as to_domain_pre_order
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
        db_items = []
        for item in items:
            db_item = to_db_pre_order(item)
            self.db.add(db_item)
            db_items.append(db_item)
        self.db.commit()
        for db_item in db_items:
            self.db.refresh(db_item)
        return [to_domain_pre_order(db_item) for db_item in db_items]

    def get_all_by_restaurant(self, restaurant_id: UUID) -> List[MenuItem]:
        statement = select(MenuItemDB).where(MenuItemDB.restaurant_id == restaurant_id)
        results = self.db.exec(statement).all()
        return [to_domain(r) for r in results]

    def get_menu_item_by_name(self, name: str) -> Optional[MenuItem]:
        statement = select(MenuItemDB).where(MenuItemDB.name == name)
        result = self.db.exec(statement).first()
        return to_domain(result) if result else None

    def get_menu_item_by_id(self, menu_item_id: UUID) -> Optional[MenuItem]:
        statement = select(MenuItemDB).where(MenuItemDB.id == menu_item_id)
        result = self.db.exec(statement).first()
        return to_domain(result) if result else None

    def create_menu_item(self, menu_item: MenuItem) -> MenuItem:
        menu_item_db = to_db(menu_item)
        self.db.add(menu_item_db)
        self.db.commit()
        self.db.refresh(menu_item_db)
        return to_domain(menu_item_db)

    def modify_menu_item(self, menu_item: MenuItem) -> MenuItem:
        self.db.commit()
        self.db.refresh(menu_item)
        return menu_item

    def delete_menu_item(self, menu_item_id: str) -> None:
        menu_item = self.db.get(MenuItemDB, menu_item_id)
        if menu_item:
            self.db.delete(menu_item)
            self.db.commit()

