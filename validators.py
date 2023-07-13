from pandas import Series

from exceptions import RawHasEmptyCellException


def validate_raw_from_excel(raw: Series) -> None:
    if raw.isna().any():
        raise RawHasEmptyCellException("Raw has an empty cell")
