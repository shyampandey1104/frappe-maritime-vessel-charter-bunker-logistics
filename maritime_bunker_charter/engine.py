"""Maritime Vessel Charter Party, Bunker Fuel & Laytime Demurrage Engine."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

@dataclass
class CharterPartyContract:
    contract_id: str
    vessel_name: str
    imo_number: str
    charterer_name: str
    daily_hire_rate_usd: float
    demurrage_rate_per_day_usd: float
    despatch_rate_per_day_usd: float  # Usually 50% of demurrage
    allowed_laytime_hours: float
    laytime_terms: str = "SHINC"      # SHINC (Sundays & Holidays Included) or SHEX (Excluded)

@dataclass
class BunkerConsumptionLog:
    voyage_id: str
    fuel_grade: str                    # VLSFO, LSMGO
    beginning_stock_mt: float
    fuel_consumed_mt: float
    fuel_bunkered_mt: float = 0.0
    sulphur_content_pct: float = 0.45  # IMO 2020 limit max 0.50%

class MaritimeCharterBunkerEngine:
    def __init__(self):
        self.contracts: Dict[str, CharterPartyContract] = {}
        self.bunker_logs: List[BunkerConsumptionLog] = []

    def register_charter_party(self, contract: CharterPartyContract) -> Dict[str, Any]:
        self.contracts[contract.contract_id] = contract
        return {"contract_id": contract.contract_id, "vessel": contract.vessel_name}

    def calculate_laytime_demurrage(self, contract_id: str, actual_laytime_used_hours: float) -> Dict[str, Any]:
        if contract_id not in self.contracts:
            raise ValueError(f"Charter party {contract_id} not found.")
        c = self.contracts[contract_id]
        
        diff_hours = actual_laytime_used_hours - c.allowed_laytime_hours
        if diff_hours > 0:
            # Demurrage incurred
            demurrage_days = diff_hours / 24.0
            amount = round(demurrage_days * c.demurrage_rate_per_day_usd, 2)
            settlement_type = "DEMURRAGE_PAYABLE_BY_CHARTERER"
        elif diff_hours < 0:
            # Despatch earned (money saved)
            saved_days = abs(diff_hours) / 24.0
            amount = round(saved_days * c.despatch_rate_per_day_usd, 2)
            settlement_type = "DESPATCH_PAYABLE_TO_CHARTERER"
        else:
            amount = 0.0
            settlement_type = "EVEN_NO_SETTLEMENT"

        return {
            "contract_id": contract_id,
            "allowed_laytime_hours": c.allowed_laytime_hours,
            "actual_laytime_used_hours": actual_laytime_used_hours,
            "variance_hours": diff_hours,
            "settlement_type": settlement_type,
            "settlement_amount_usd": amount
        }

    def record_bunker_consumption(self, log: BunkerConsumptionLog) -> Dict[str, Any]:
        if log.sulphur_content_pct > 0.50:
            raise ValueError(f"Sulphur {log.sulphur_content_pct}% breaches IMO 2020 MARPOL Annex VI statutory ceiling of 0.50%!")
        ending_stock = round(log.beginning_stock_mt - log.fuel_consumed_mt + log.fuel_bunkered_mt, 2)
        self.bunker_logs.append(log)
        return {
            "voyage_id": log.voyage_id,
            "fuel_grade": log.fuel_grade,
            "fuel_consumed_mt": log.fuel_consumed_mt,
            "ending_stock_mt": ending_stock,
            "imo_2020_compliant": True
        }
