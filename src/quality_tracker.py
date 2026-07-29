import logging
from typing import Any

import pandas as pd

logger = logging.getLogger("quality_tracker")


class AdvancedDataQualityTracker:
    """Computes production-grade data quality metrics profiles across operational data lake frames."""

    def __init__(self, currency_whitelist: list[str] = None) -> None:
        self.currency_whitelist = currency_whitelist or [
            "USD",
            "EUR",
            "GBP",
            "NGN",
            "KES",
        ]

    def profile_transaction_dataset(self, df: pd.DataFrame) -> dict[str, Any]:
        """Audits structural data matrices and compiles an observability data quality metric card."""
        if df.empty:
            logger.warning(
                "Data quality profiling aborted: Ingested DataFrame is empty."
            )
            return {
                "completeness": 0.0,
                "uniqueness": 0.0,
                "validity": 0.0,
                "passed_gate": False,
            }

        total_rows = len(df)

        # 1. COMPLETENESS: Audit missing null identifiers across key fields
        null_counts = df[["transaction_id", "amount", "timestamp"]].isnull().sum().sum()
        total_cells = total_rows * 3
        completeness_pct = float(((total_cells - null_counts) / total_cells) * 100)

        # 2. UNIQUENESS: Audit primary identity collision ratios
        unique_ids = df["transaction_id"].nunique()
        uniqueness_pct = float((unique_ids / total_rows) * 100)

        # 3. VALIDITY: Validate commercial business logic constraints
        valid_amount_mask = df["amount"].fillna(0) >= 0
        valid_currency_mask = df["currency"].fillna("").isin(self.currency_whitelist)
        valid_rows = df[valid_amount_mask & valid_currency_mask]
        validity_pct = float((len(valid_rows) / total_rows) * 100)

        # Quality Gate Verification Invariant
        passed_gate = (
            completeness_pct > 95.0 and uniqueness_pct == 100.0 and validity_pct > 90.0
        )

        metrics_report = {
            "total_records_audited": total_rows,
            "completeness_score_pct": round(completeness_pct, 2),
            "uniqueness_score_pct": round(uniqueness_pct, 2),
            "validity_score_pct": round(validity_pct, 2),
            "passed_quality_gate": passed_gate,
        }

        logger.info(
            f"DQ Audit Finished - Completeness: {metrics_report['completeness_score_pct']}% | "
            f"Uniqueness: {metrics_report['uniqueness_score_pct']}% | "
            f"Validity: {metrics_report['validity_score_pct']}%"
        )
        return metrics_report
