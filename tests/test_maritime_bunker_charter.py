import unittest
from maritime_bunker_charter.engine import CharterPartyContract, BunkerConsumptionLog, MaritimeCharterBunkerEngine

class TestMaritimeCharterBunkerEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MaritimeCharterBunkerEngine()
        self.contract = CharterPartyContract(
            contract_id="CP-2026-MUM-ROTTERDAM", vessel_name="M/V Sagar Kanti",
            imo_number="IMO9812401", charterer_name="Glencore Commodities",
            daily_hire_rate_usd=28000.0, demurrage_rate_per_day_usd=30000.0,
            despatch_rate_per_day_usd=15000.0, allowed_laytime_hours=72.0
        )
        self.engine.register_charter_party(self.contract)

    def test_demurrage_settlement(self):
        res = self.engine.calculate_laytime_demurrage("CP-2026-MUM-ROTTERDAM", actual_laytime_used_hours=96.0)
        self.assertEqual(res["settlement_type"], "DEMURRAGE_PAYABLE_BY_CHARTERER")
        self.assertEqual(res["settlement_amount_usd"], 30000.0)

    def test_despatch_settlement(self):
        res = self.engine.calculate_laytime_demurrage("CP-2026-MUM-ROTTERDAM", actual_laytime_used_hours=48.0)
        self.assertEqual(res["settlement_type"], "DESPATCH_PAYABLE_TO_CHARTERER")
        self.assertEqual(res["settlement_amount_usd"], 15000.0)

    def test_bunker_fuel_imo_compliance(self):
        log = BunkerConsumptionLog(
            voyage_id="VOY-449", fuel_grade="VLSFO",
            beginning_stock_mt=850.0, fuel_consumed_mt=45.0, sulphur_content_pct=0.48
        )
        bunk = self.engine.record_bunker_consumption(log)
        self.assertTrue(bunk["imo_2020_compliant"])
        self.assertEqual(bunk["ending_stock_mt"], 805.0)

if __name__ == "__main__":
    unittest.main()
