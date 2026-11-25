from __future__ import annotations

from pathlib import Path

from database.warehouse import build_star_schema
from modules.preprocessing import load_dataset, prepare_processed_dataset


def run_etl(csv_path: str | Path, db_path: str | Path):
    raw_df = load_dataset(csv_path)
    cleaned_df, summary = prepare_processed_dataset(raw_df)
    db_path = Path(db_path)
    db_path.parent.mkdir(exist_ok=True, parents=True)
    schema_loaded = build_star_schema(db_path, cleaned_df)
    return {
        "raw_rows": len(raw_df),
        "cleaned_rows": len(cleaned_df),
        "summary": summary,
        "warehouse_status": schema_loaded,
        "cleaned_data": cleaned_df,
    }
