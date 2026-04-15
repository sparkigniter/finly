"""Module providing holdings functionality."""

from dataclasses import dataclass


@dataclass
class Holdings:
    """Class to represent the user's holdings."""

    symbol: str
    quantity: int
    average_price: float
    last_price: float
    pnl: float
    exchange: str
