from uuid import UUID, uuid4

class Table:
    def __init__(self, id: UUID, restaurant_id: UUID, table_number: int, capacity: int, location: str):
        if not 2 <= capacity <= 12:
            raise ValueError("La capacidad de la mesa debe estar entre 2 y 12.")
        
        self.id = id
        self.restaurant_id = restaurant_id
        self.table_number = table_number
        self.capacity = capacity
        self.location = location

    @staticmethod
    def create(restaurant_id: UUID, table_number: int, capacity: int, location: str) -> "Table":
        return Table(uuid4(), restaurant_id, table_number, capacity, location)
