"""
casased - Casablanca Stock Exchange Data Retriever
==================================================

A Python library for retrieving stock market data from the Casablanca Stock Exchange.
"""

from .load import get_history, loadata, loadmany, get_intraday, getIntraday
from .notation import notation, notation_code, notation_value, list_assets, get_isin_by_name
from .tech import getCours, getKeyIndicators, getDividend, getIndex, getPond, getIndexRecap

__version__ = "0.1.5"

__all__ = [
    # Data loading functions
    "get_history",
    "loadata",
    "loadmany",
    "get_intraday",
    "getIntraday",
    # Notation/asset functions
    "notation",
    "notation_code",
    "notation_value",
    "list_assets",
    "get_isin_by_name",
    # Technical data functions
    "getCours",
    "getKeyIndicators",
    "getDividend",
    "getIndex",
    "getPond",
    "getIndexRecap",
]