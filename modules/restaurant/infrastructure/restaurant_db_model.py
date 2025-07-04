from sqlalchemy import Column, String, Time
from sqlalchemy.dialects.postgresql import UUID
from modules.core.db_connection import Base

class RestaurantDBModel(Base):
    __tablename__ = 'restaurants'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
