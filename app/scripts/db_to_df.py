import pandas as pd
from tqdm import tqdm

from app.database.container import movement_service


def get_df_from_db() -> pd.DataFrame:
    movements = movement_service.get_all()

    data = []
    for movement in tqdm(movements, total=len(movements), desc="Заполнение датафрейма"):
        data.append({
            "Имя человека": movement.person.full_name,
            "Социальный статус": movement.person.social_status,
            "День недели": movement.week_day,
            "Место отправления": movement.departure_place_type,
            "Место прибытия": movement.arrival_place_type,
            "Время отправления": movement.departure_time,
            "lat": movement.departure_lat,
            "lon": movement.departure_lon,
        })

    df = pd.DataFrame(data)
    return df
