"""₹500 crore deployment sizing for the selected winner."""

from __future__ import annotations

import math
from typing import Any

import pandas as pd


def deployment_plan(market: pd.DataFrame, assumptions: dict[str, Any], ticker: str = "CAMS") -> pd.DataFrame:
    cfg = assumptions["portfolio"]
    price = float(market.loc[ticker, "price_inr"])
    capital = float(cfg["capital_cr"])
    position_value = capital * float(cfg["target_weight"])
    max_value = capital * float(cfg["max_weight"])
    shares = math.floor(position_value * 1e7 / price)
    actual_value = shares * price / 1e7
    tranche_values = [position_value * weight for weight in cfg["tranches"]]
    tranche_shares = [math.floor(value * 1e7 / price) for value in tranche_values]
    adv = float(cfg["adv_assumption_cr"])
    daily_capacity = adv * float(cfg["participation_cap"])
    days_to_build = math.ceil(position_value / daily_capacity)

    rows = []
    for index, (weight, value, tranche_shares_count) in enumerate(
        zip(cfg["tranches"], tranche_values, tranche_shares), start=1
    ):
        rows.append(
            {
                "ticker": ticker,
                "line": f"tranche_{index}",
                "weight_of_position": weight,
                "target_value_cr": value,
                "price_inr": price,
                "shares": tranche_shares_count,
                "actual_value_cr": tranche_shares_count * price / 1e7,
                "trigger": {
                    1: "Initiation at current price; valuation gate passes",
                    2: "Q2 FY27 results confirm revenue growth >=10% and EBITDA margin >=45%",
                    3: "Price <= ₹725 or FY28 EPS visibility improves; whichever first",
                }[index],
            }
        )
    rows.append(
        {
            "ticker": ticker,
            "line": "total",
            "weight_of_position": 1.0,
            "target_value_cr": position_value,
            "price_inr": price,
            "shares": shares,
            "actual_value_cr": actual_value,
            "trigger": f"Build over {days_to_build} trading days at <=15% of assumed ₹{adv:.0f} cr ADV",
        }
    )
    rows.append(
        {
            "ticker": ticker,
            "line": "risk_limits",
            "weight_of_position": cfg["max_weight"],
            "target_value_cr": max_value,
            "price_inr": price,
            "shares": math.floor(max_value * 1e7 / price),
            "actual_value_cr": math.floor(max_value * 1e7 / price) * price / 1e7,
            "trigger": "Hard cap 5% of sleeve; no leverage; review if position exceeds 5.5% on mark-to-market",
        }
    )
    return pd.DataFrame(rows)
