from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from modules.menu.domain.pre_order_item import PreOrderItem
from modules.menu.domain.menu_item import MenuItem
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .menu_item_db_model import MenuItemDB

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.reservation.infrastructure.reservation_db_model import ReservationDBModel

class PreOrderItemDB(SQLModel, PreOrderItem, table=True):
    __tablename__ = "pre_order_items"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    menu_item_id: UUID = Field(foreign_key="menu_items.id")
    reservation_id: UUID = Field(foreign_key="reservationdbmodel.uuid")
    quantity: int
    special_instructions: Optional[str]
    
    # Relationships
    menu_item: Optional["MenuItemDB"] = Relationship(back_populates="pre_orders")
    reservation: Optional["ReservationDBModel"] = Relationship(back_populates="pre_orders")

# Convertir de PreOrderItemDB (infraestructura) a PreOrderItem (dominio)
def to_domain(pre_order_item_db: PreOrderItemDB) -> PreOrderItem:
    return PreOrderItem(
        id=pre_order_item_db.id,
        menu_item_id=pre_order_item_db.menu_item_id,
        reservation_id=pre_order_item_db.reservation_id,
        quantity=pre_order_item_db.quantity,
        special_instructions=pre_order_item_db.special_instructions
    )

# Convertir de PreOrderItem (dominio) a PreOrderItemDB (infraestructura)
def to_db(pre_order_item: PreOrderItem) -> PreOrderItemDB:
    return PreOrderItemDB(
        menu_item_id=pre_order_item.menu_item_id,
        reservation_id=pre_order_item.reservation_id,
        quantity=pre_order_item.quantity,
        special_instructions=pre_order_item.special_instructions
    )