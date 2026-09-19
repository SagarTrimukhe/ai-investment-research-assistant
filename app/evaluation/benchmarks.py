from typing import Dict, Any


def evaluate_kpis(asset_a_metrics: Dict[str, Any], asset_b_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compare key valuation metrics between two assets."""
    comparison = {}
    for key in ["pe_ratio", "forward_pe", "market_cap"]:
        val_a = asset_a_metrics.get(key)
        val_b = asset_b_metrics.get(key)
        comparison[key] = {
            "target": val_a,
            "benchmark": val_b,
        }
    return comparison
