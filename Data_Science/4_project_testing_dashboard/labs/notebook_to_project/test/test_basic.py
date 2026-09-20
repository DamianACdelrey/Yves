from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core import (
    load_data,
    normalize_city,
    parse_dates,
    parse_numerics,
    remove_duplicates,
    clean_trips,
    trips_by_city,
    save_clean_trips,
)


def test_load_data(tmp_path: Path) -> None:
    sample = tmp_path / "trips.csv"
    sample.write_text("city,date,days_spent,budget_eur\nBerlin,2026-01-01,3,450\n")
    trips = load_data(sample)
    assert len(trips) == 1
    assert list(trips.columns) == ["city", "date", "days_spent", "budget_eur"]


def test_normalize_city() -> None:
    trips = pd.DataFrame({"city": [" berlin ", "PARIS"]})
    result = normalize_city(trips)
    assert result["city"].tolist() == ["Berlin", "Paris"]


def test_parse_dates() -> None:
    trips = pd.DataFrame({"date": ["2026-01-01", "not-a-date"]})
    result = parse_dates(trips)
    assert pd.notna(result.loc[0, "date"])
    assert pd.isna(result.loc[1, "date"])


def test_parse_numerics() -> None:
    trips = pd.DataFrame({"days_spent": ["3", ""], "budget_eur": ["450.0", "bad"]})
    result = parse_numerics(trips)
    assert result.loc[0, "days_spent"] == 3.0
    assert pd.isna(result.loc[1, "days_spent"])
    assert result.loc[0, "budget_eur"] == 450.0
    assert pd.isna(result.loc[1, "budget_eur"])


def test_remove_duplicates() -> None:
    trips = pd.DataFrame({"city": ["Berlin", "Berlin"], "days_spent": [3, 3]})
    result = remove_duplicates(trips)
    assert len(result) == 1


def test_clean_trips() -> None:
    trips = pd.DataFrame(
        {
            "city": [" berlin ", "berlin"],
            "date": ["2026-01-01", "2026-01-01"],
            "days_spent": ["3", "3"],
            "budget_eur": ["450", "450"],
        }
    )
    result = clean_trips(trips)
    assert len(result) == 1
    assert result.loc[0, "city"] == "Berlin"
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result.loc[0, "days_spent"] == 3.0
    assert result.loc[0, "budget_eur"] == 450.0


def test_trips_by_city_counts() -> None:
    trips = pd.DataFrame({"city": ["New York", "New York", "Chicago"]})
    cities = trips_by_city(trips)
    assert cities.loc["New York"] == 2
    assert cities.loc["Chicago"] == 1


def test_save_clean_trips(tmp_path: Path) -> None:
    trips = pd.DataFrame({"city": ["Berlin"], "budget_eur": [450.0]})
    out = tmp_path / "clean.csv"
    assert save_clean_trips(trips, out) is True
    assert out.exists()
    loaded = pd.read_csv(out)
    assert loaded.loc[0, "city"] == "Berlin"
