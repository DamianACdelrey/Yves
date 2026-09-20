from pathlib import Path
import argparse
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core import load_data, clean_trips, trips_by_city, save_clean_trips


def main() -> None:
    parser = argparse.ArgumentParser(description="Load, clean, and save trips data")
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "trips_raw.csv",
        help="Path to raw trips CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "data" / "trips_cleaned.csv",
        help="Path for cleaned trips CSV",
    )
    args = parser.parse_args()

    trips = load_data(args.input)
    trips = clean_trips(trips)

    if not save_clean_trips(trips, args.output):
        raise SystemExit(f"Could not save cleaned trips to {args.output}")

    print(trips_by_city(trips))
    print(f"Saved cleaned trips to {args.output}")


if __name__ == "__main__":
    main()
