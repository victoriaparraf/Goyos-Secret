from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from modules.menu.domain.menu_item import MenuItem
from typing import Optional
from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB

class MenuItemDB(SQLModel, MenuItem, table=True):
    __tablename__ = "menu_items"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    description: str
    category: str
    price: float
    available_stock: int
    restaurant_id: UUID = Field(foreign_key="restaurantdbmodel.id", index=True)
    image_url: Optional[str]

    # Relación inversa con PreOrderItemDB
    pre_orders: list["PreOrderItemDB"] = Relationship(back_populates="menu_item")

# Convertir de MenuItemDB (infraestructura) a MenuItem (dominio)
def to_domain(menu_item_db: MenuItemDB) -> MenuItem:
    return MenuItem(
        id=menu_item_db.id,
        name=menu_item_db.name,
        description=menu_item_db.description,
        category=menu_item_db.category,
        price=menu_item_db.price,
        available_stock=menu_item_db.available_stock,
        restaurant_id=menu_item_db.restaurant_id,
        image_url=menu_item_db.image_url
    )

# Convertir de MenuItem (dominio) a MenuItemDB (infraestructura)
def to_db(menu_item: MenuItem) -> MenuItemDB:
    return MenuItemDB(
        name=menu_item.name,
        description=menu_item.description,
        category=menu_item.category,
        price=menu_item.price,
        available_stock=menu_item.available_stock,
        restaurant_id=menu_item.restaurant_id,
        image_url=menu_item.image_url
    )