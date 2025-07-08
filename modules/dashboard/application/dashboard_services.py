from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List
from sqlmodel import Session, select, func
from modules.reservation.infrastructure.reservation_db_model import ReservationDBModel
from modules.restaurant.infrastructure.table_db_model import TableDBModel
from modules.restaurant.infrastructure.restaurant_db_model import RestaurantDBModel

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_reservations_summary(self) -> Dict[str, Dict[str, int]]:
        result = self.db.exec(select(ReservationDBModel)).all()
        daily = defaultdict(int)
        weekly = defaultdict(int)

        for r in result:
            date_str = r.start_time.date().isoformat()
            week_str = f"{r.start_time.year}-W{r.start_time.isocalendar()[1]}"
            daily[date_str] += 1
            weekly[week_str] += 1

        return {
            "by_day": dict(daily),
            "by_week": dict(weekly),
        }

    def get_top_preordered_dishes(self, top_n: int = 5) -> Dict[str, int]:
        from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB
        result = self.db.exec(select(PreOrderItemDB)).all()
        dish_counter = Counter()
        for pre_order in result:
            dish_counter[str(pre_order.menu_item_id)] += pre_order.quantity if pre_order.quantity else 1
        return dict(dish_counter.most_common(top_n))

    def get_occupancy_percentage(self) -> List[Dict[str, object]]:
        restaurants = self.db.exec(select(RestaurantDBModel)).all()
        data = []

        for rest in restaurants:
            # Total de mesas del restaurante
            total_tables_result = self.db.exec(
                select(func.count()).select_from(TableDBModel).where(TableDBModel.restaurant_id == rest.id)
            ).first()
            if isinstance(total_tables_result, (tuple, list)):
                total_tables = total_tables_result[0]
            else:
                total_tables = total_tables_result or 0

            # Mesas reservadas (únicas)
            reserved_tables_result = self.db.exec(
                select(func.count(func.distinct(ReservationDBModel.table_id))).where(
                    ReservationDBModel.start_time >= datetime.now(),
                    ReservationDBModel.table_id.in_(
                        select(TableDBModel.id).where(TableDBModel.restaurant_id == rest.id)
                    )
                )
            ).first()
            if isinstance(reserved_tables_result, (tuple, list)):
                reserved_tables = reserved_tables_result[0]
            else:
                reserved_tables = reserved_tables_result or 0

            # Calcular ocupación solo si hay mesas
            occupancy = (reserved_tables / total_tables * 100) if total_tables > 0 else 0.0

            data.append({
                "restaurant_id": str(rest.id),
                "restaurant_name": rest.name,
                "occupancy_percentage": round(occupancy, 2)
            })

        return data

