"""Decision matrix and weight-sensitivity tests."""

from __future__ import annotations

from typing import Any

import pandas as pd


def decision_matrix(assumptions: dict[str, Any], expected: pd.DataFrame) -> pd.DataFrame:
    weights = assumptions["decision_matrix"]["weights"]
    scores = assumptions["decision_matrix"]["scores"]
    expected_map = expected.set_index("ticker").to_dict(orient="index")
    rows = []
    for ticker, company_scores in scores.items():
        weighted = sum(weights[criterion] * company_scores[criterion] for criterion in weights)
        rows.append(
            {
                "ticker": ticker,
                **{f"score_{criterion}": company_scores[criterion] for criterion in weights},
                "weighted_score": weighted,
                "expected_total_return_pct": expected_map[ticker]["expected_total_return_pct"],
                "bear_downside_pct": expected_map[ticker]["bear_downside_pct"],
                "base_target_price": expected_map[ticker]["base_target_price"],
            }
        )
    frame = pd.DataFrame(rows).sort_values("weighted_score", ascending=False).reset_index(drop=True)
    frame["rank"] = frame.index + 1
    return frame


def weight_sensitivity(assumptions: dict[str, Any]) -> pd.DataFrame:
    base_weights = assumptions["decision_matrix"]["weights"].copy()
    scores = assumptions["decision_matrix"]["scores"]
    rows = []

    def weighted(weights: dict[str, float], ticker: str) -> float:
        return sum(weights[key] * scores[ticker][key] for key in weights)

    def add_case(name: str, weights: dict[str, float]) -> None:
        ranking = sorted(
            ((ticker, weighted(weights, ticker)) for ticker in scores),
            key=lambda item: item[1],
            reverse=True,
        )
        rows.append(
            {
                "case": name,
                "winner": ranking[0][0],
                "winner_score": ranking[0][1],
                "runner_up": ranking[1][0],
                "runner_up_score": ranking[1][1],
                "cams_score": weighted(weights, "CAMS"),
                "cams_rank": [ticker for ticker, _ in ranking].index("CAMS") + 1,
                **{f"weight_{key}": value for key, value in weights.items()},
            }
        )

    add_case("base", base_weights)
    add_case("equal_weights", {key: 1 / len(base_weights) for key in base_weights})

    for criterion in base_weights:
        for delta in (-0.10, 0.10):
            adjusted = base_weights.copy()
            adjusted[criterion] = max(0.0, adjusted[criterion] + delta)
            total = sum(adjusted.values())
            adjusted = {key: value / total for key, value in adjusted.items()}
            add_case(f"{criterion}_{delta:+.0%}", adjusted)

    return pd.DataFrame(rows)
