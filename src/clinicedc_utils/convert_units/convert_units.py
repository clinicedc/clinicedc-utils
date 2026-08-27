from __future__ import annotations

__all__ = ["convert_units"]

from .units_converter import UnitsConverter


def convert_units(
    *,
    label: str,
    value: int | float,
    units_from: str,
    units_to: str,
    places: int | None = None,
    mw: float | None = None,
) -> int | float:
    return UnitsConverter(
        label=label,
        value=value,
        units_from=units_from,
        units_to=units_to,
        places=places,
        mw=mw,
    ).converted_value
