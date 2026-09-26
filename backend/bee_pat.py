"""
Bureau of Energy Efficiency (BEE) PAT Scheme (Perform, Achieve and Trade) Engine
Calculates Specific Energy Consumption reductions, compliance targets, and ESCerts (Energy Saving Certificates).
Compliant with India's Energy Conservation Act, 2001 & BEE Industrial Sector Target Guidelines.
"""

from typing import Dict, Any

class BEEPatSchemeEngine:
    def __init__(self):
        # BEE PAT Sectoral Benchmarks for Foundry & Steel Induction Melting
        self.baseline_sec_toe_per_t = 0.0731   # Baseline specific energy (toe/t) ~ 850 kWh/t
        self.target_sec_toe_per_t = 0.0537     # PAT Cycle Target (toe/t) ~ 625 kWh/t (IGBT Standard)
        self.kwh_to_toe = 0.000086             # 1 kWh = 8.6 x 10^-5 Tonnes of Oil Equivalent (toe)
        self.escert_market_price_inr = 2150.0  # Current trading price per ESCert on Indian Energy Exchange (IEX)
        self.mtoe_per_escert = 1.0             # 1 ESCert = 1 metric tonne of oil equivalent saved

    def evaluate_batch_pat_compliance(self, energy_kwh: float, output_tonnes: float) -> Dict[str, Any]:
        """Calculates PAT scheme performance and ESCerts earned for a heat."""
        if output_tonnes <= 0:
            output_tonnes = 1.5
            
        actual_sec_kwh_per_t = energy_kwh / output_tonnes
        actual_sec_toe_per_t = actual_sec_kwh_per_t * self.kwh_to_toe
        baseline_kwh_per_t = self.baseline_sec_toe_per_t / self.kwh_to_toe  # ~850 kWh/t
        target_kwh_per_t = self.target_sec_toe_per_t / self.kwh_to_toe      # ~625 kWh/t
        
        # Energy savings vs baseline
        energy_saved_kwh_per_t = max(0.0, baseline_kwh_per_t - actual_sec_kwh_per_t)
        batch_energy_saved_kwh = energy_saved_kwh_per_t * output_tonnes
        batch_energy_saved_toe = batch_energy_saved_kwh * self.kwh_to_toe
        
        # ESCerts earned (1 ESCert = 1 toe saved below baseline target)
        escerts_earned = batch_energy_saved_toe / self.mtoe_per_escert
        escerts_value_inr = escerts_earned * self.escert_market_price_inr
        
        # Annualized projection for a typical 2,500 MT/year MSME foundry
        annual_batches = 2500.0 / output_tonnes
        annual_escerts = escerts_earned * annual_batches
        annual_escert_revenue_inr = annual_escerts * self.escert_market_price_inr
        
        # Compliance status
        compliance_status = "PAT COMPLIANT" if actual_sec_kwh_per_t <= target_kwh_per_t else (
            "INTERMEDIATE SAVINGS" if actual_sec_kwh_per_t < baseline_kwh_per_t else "PAT DEFICIT"
        )

        return {
            "actual_sec_kwh_per_t": round(actual_sec_kwh_per_t, 1),
            "actual_sec_toe_per_t": round(actual_sec_toe_per_t, 5),
            "bee_pat_baseline_sec": round(baseline_kwh_per_t, 1),
            "bee_pat_target_sec": round(target_kwh_per_t, 1),
            "energy_saved_vs_baseline_kwh": round(batch_energy_saved_kwh, 1),
            "escerts_earned_per_batch": round(escerts_earned, 4),
            "escert_value_inr_per_batch": round(escerts_value_inr, 2),
            "projected_annual_escerts": round(annual_escerts, 1),
            "projected_annual_revenue_inr": round(annual_escert_revenue_inr, 0),
            "iex_escert_market_price_inr": self.escert_market_price_inr,
            "compliance_status": compliance_status
        }
