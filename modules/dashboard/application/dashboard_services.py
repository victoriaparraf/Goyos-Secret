from typing import List, Dict, Any
from datetime import datetime, date, timedelta
from collections import Counter
from uuid import UUID

from fastapi import HTTPException, status

from modules.reservation.domain.reservation_repository_interface import IReservationRepository
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository

class DashboardService:
    def __init__(
        self,
        reservation_repo: IReservationRepository,
        menu_repo: MenuRepositoryInterface,
        table_repo: ITableRepository,
        restaurant_repo: IRestaurantRepository
    ):
        self.reservation_repo = reservation_repo
        self.menu_repo = menu_repo
        self.table_repo = table_repo
        self.restaurant_repo = restaurant_repo

    def get_total_reservations_by_date_range(self, start_date: date, end_date: date) -> Dict[date, int]:
        reservations = self.reservation_repo.get_by_date_range(datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()))
        
        reservation_counts = Counter()
        for res in reservations:
            reservation_counts[res.start_time.date()] += 1
        
        # Ensure all dates in range are present, even if count is 0
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        return {d: reservation_counts[d] for d in date_range}

    def get_top_preordered_dishes(self, limit: int = 5) -> List[Dict[str, Any]]:
        all_reservations = self.reservation_repo.get_all()
        
        dish_counts = Counter()
        for res in all_reservations:
            if res.preordered_dishes:
                for dish_id in res.preordered_dishes:
                    dish_counts[dish_id] += 1
        
        top_dishes = []
        for dish_id, count in dish_counts.most_common(limit):
            menu_item = self.menu_repo.get_menu_item_by_id(dish_id) # Assuming a get_menu_item_by_id method exists
            if menu_item:
                top_dishes.append({"dish_id": str(dish_id), "name": menu_item.name, "count": count})
            else:
                top_dishes.append({"dish_id": str(dish_id), "name": "Unknown Dish", "count": count}) # Handle case where menu item not found
        
        return top_dishes

    def get_occupancy_percentage(self, restaurant_id: str) -> Dict[str, float]:
        restaurant_uuid = UUID(restaurant_id)
        restaurant = self.restaurant_repo.get_by_id(restaurant_uuid)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found.")

        total_tables = self.table_repo.get_total_tables_by_restaurant(restaurant_uuid) # Assuming this method exists
        if total_tables == 0:
            return {"occupancy_percentage": 0.0}

        # Get active reservations for today for this restaurant
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        active_reservations = self.reservation_repo.get_active_by_restaurant_and_time_range(restaurant_uuid, start_of_day, end_of_day) # Assuming this method exists
        occupied_tables = len(set([res.table_id for res in active_reservations]))

        occupancy_percentage = (occupied_tables / total_tables) * 100
        return {"occupancy_percentage": round(occupancy_percentage, 2)}
