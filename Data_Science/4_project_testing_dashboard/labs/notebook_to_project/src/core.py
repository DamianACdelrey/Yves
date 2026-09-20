from pathlib import Path
import pandas as pd


def load_data(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def normalize_city(trips: pd.DataFrame) -> pd.DataFrame:
    trips = trips.copy()
    trips["city"] = trips["city"].str.strip().str.title()
    return trips

def parse_dates(trips: pd.DataFrame) -> pd.DataFrame:
    trips = trips.copy()
    trips["date"] = pd.to_datetime(trips["date"], errors="coerce", dayfirst=False)
    return trips

def parse_numerics(trips: pd.DataFrame) -> pd.DataFrame:
    trips = trips.copy()
    trips["days_spent"] = pd.to_numeric(trips["days_spent"], errors="coerce")
    trips["budget_eur"] = pd.to_numeric(trips["budget_eur"], errors="coerce")
    return trips

def remove_duplicates(trips: pd.DataFrame) -> pd.DataFrame:
    return trips.drop_duplicates()

def clean_trips(trips: pd.DataFrame) -> pd.DataFrame:
    trips = normalize_city(trips)
    trips = parse_dates(trips)
    trips = parse_numerics(trips)
    trips = remove_duplicates(trips)
    return trips

def trips_by_city(trips: pd.DataFrame) -> pd.Series:
    return trips["city"].value_counts()

def save_clean_trips(trips: pd.DataFrame, file_path: Path) -> bool:
    try:
        trips.to_csv(file_path, index=False)
        return True
    except Exception:
        return False