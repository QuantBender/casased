import requests
import pandas as pd
import datetime
from typing import Optional, Union
from .notation import notation_code


_USER_AGENT = {'User-Agent': 'Mozilla/5.0'}


def _resolve_isin(identifier: str) -> str:
    """Return an ISIN string for a given asset name or ISIN.
    If the identifier looks like an ISIN (starts with 'MA' or contains 'MA'), it's returned uppercased.
    Otherwise the notation mapping is used to find the ISIN by name (case-insensitive).
    """
    if not isinstance(identifier, str):
        raise ValueError("identifier must be a string (asset name or ISIN)")
    idu = identifier.strip()
    # simple ISIN heuristic
    if idu.upper().startswith("MA"):
        return idu.upper()
    for action in notation_code():
        if action["name"].lower() == idu.lower():
            return action["ISIN"]
    raise ValueError(f"Unknown asset name or ISIN: {identifier}")


def get_history(identifier: str, start: Optional[Union[str, datetime.date]] = None,
                end: Optional[Union[str, datetime.date]] = None) -> pd.DataFrame:
    """Get historical daily data for a listed asset (by name or ISIN) or for MASI/MSI20.

    Returns a pandas DataFrame indexed by date with columns: Value, Min, Max, Variation, Volume
    """
    # Handle indices
    if identifier.upper() == "MASI":
        link = "https://medias24.com/content/api?method=getMasiHistory&periode=10y&format=json"
    elif identifier.upper() == "MSI20":
        link = "https://medias24.com/content/api?method=getIndexHistory&ISIN=msi20&periode=10y&format=json"
    else:
        isin = _resolve_isin(identifier)
        # default dates
        if start is None and end is None:
            start = "2011-09-18"
            end = str(datetime.datetime.today().date())
        # accept datetime.date or string
        s = pd.to_datetime(start).strftime("%Y-%m-%d")
        e = pd.to_datetime(end).strftime("%Y-%m-%d")
        link = f"https://medias24.com/content/api?method=getPriceHistory&ISIN={isin}&format=json&from={s}&to={e}"

    resp = requests.get(link, headers=_USER_AGENT)
    resp.raise_for_status()
    data = resp.json()
    # stock price history: result is a list of records with Date etc.
    if "result" in data and isinstance(data["result"], list):
        df = pd.DataFrame(data["result"])
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            df.set_index("Date", inplace=True)
            # ensure consistent columns
            df = df.rename(columns={c: c.strip() for c in df.columns})
            return df
    # index history: result contains labels (timestamps)
    # try to build DataFrame from labels
    if "result" in data and isinstance(data["result"], dict):
        res = data["result"]
        if "labels" in res and isinstance(res["labels"], list):
            labels = [datetime.datetime.fromtimestamp(int(x)).date() for x in res["labels"]]
            # other values may be in res['values'] or res.get('data')
            # try to find a numeric column
            values = None
            for k, v in res.items():
                if k != "labels" and isinstance(v, list):
                    values = v
                    break
            if values is None:
                # fallback: wrap the raw result
                return pd.DataFrame(res)
            df = pd.DataFrame(values, index=labels, columns=["Value"]) if not isinstance(values[0], list) else pd.DataFrame(values[0], index=labels, columns=["Value"]) 
            return df

    # If parsing failed, return raw DataFrame
    return pd.DataFrame(data)


# Backwards-compatible aliases
loadata = get_history


def loadmany(*args, start=None, end=None, feature: str = "Value") -> pd.DataFrame:
    """Load the data of many equities and return a DataFrame with one column per asset.

    Accepts either a list as single argument or multiple string arguments.
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        assets = args[0]
    else:
        assets = list(args)
    result = pd.DataFrame()
    for asset in assets:
        df = get_history(asset, start=start, end=end)
        if feature not in df.columns:
            raise ValueError(f"Feature '{feature}' not found for asset '{asset}'. Available: {list(df.columns)}")
        result[asset] = df[feature]
    return result


def get_intraday(identifier: str) -> pd.DataFrame:
    """Get intraday data for an asset (name or ISIN), or market/index intraday for MASI/MSI20.

    Returns a DataFrame indexed by time (labels) with a 'Value' column.
    """
    if identifier.upper() == "MASI":
        link = "https://medias24.com/content/api?method=getMarketIntraday&format=json"
    elif identifier.upper() == "MSI20":
        link = "https://medias24.com/content/api?method=getIndexIntraday&ISIN=msi20&format=json"
    else:
        isin = _resolve_isin(identifier)
        link = f"https://medias24.com/content/api?method=getStockIntraday&ISIN={isin}&format=json"

    resp = requests.get(link, headers=_USER_AGENT)
    resp.raise_for_status()
    data = resp.json()
    if "result" in data and isinstance(data["result"], list):
        # some intraday data is nested
        try:
            r = data["result"][0]
            if "labels" in r and "data" in r:
                df = pd.DataFrame(r.get("data") if isinstance(r.get("data"), list) else [r.get("data")], index=r["labels"])
                df.index = pd.to_datetime(df.index).time
                df.columns = ["Value"]
                return df
        except Exception:
            pass
    # fallback: raw DataFrame
    return pd.DataFrame(data)


# Backwards-compatible alias
getIntraday = get_intraday