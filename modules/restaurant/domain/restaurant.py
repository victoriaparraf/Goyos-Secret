from uuid import UUID, uuid4
from datetime import time

class Restaurant:
    def __init__(self, id: UUID, name: str, location: str, opening_time: time, closing_time: time):
        if opening_time >= closing_time:
            raise ValueError("La hora de apertura debe ser anterior a la hora de cierre.")
        
        self.id = id
        self.name = name
        self.location = location
        self.opening_time = opening_time
        self.closing_time = closing_time

    @staticmethod
    def create(name: str, location: str, opening_time: time, closing_time: time) -> "Restaurant":
        return Restaurant(uuid4(), name, location, opening_time, closing_time)
