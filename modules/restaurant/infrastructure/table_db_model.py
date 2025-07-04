from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from modules.core.db_connection import Base

class TableDBModel(Base):
    __tablename__ = 'tables'

    id = Column(UUID(as_uuid=True), primary_key=True)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('restaurants.id'), nullable=False)
    table_number = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    restaurant = relationship("RestaurantDBModel")
