"""
EU Carbon Border Adjustment Mechanism (CBAM) Compliance & Carbon Ledger Engine
Quantifies specific carbon intensity (tCO2/t casting) and potential CBAM duty liabilities.
"""

from typing import Dict, Any, List

class CBAMLedger:
    def __init__(self):
        # Emission factors and benchmarks
        self.grid_emission_factor_kg_kwh = 0.82  # CEA India Baseline (kg CO2 / kWh)
        self.india_foundry_benchmark_tco2_per_t = 2.50  # Typical Indian casting carbon intensity
        self.eu_foundry_benchmark_tco2_per_t = 1.50     # EU modern foundry benchmark
        self.eu_ets_carbon_price_eur = 79.68           # Current EU ETS carbon allowance price per tCO2
        self.eur_to_inr = 93.50                         # Current exchange rate
        
    def calculate_batch_carbon(self, energy_kwh: float, output_tonnes: float) -> Dict[str, Any]:
        """Calculates carbon footprint and CBAM duty exposure for a single batch."""
        if output_tonnes <= 0:
            output_tonnes = 1.0
            
        # Scope 2 emissions from induction melting electricity
        melt_co2_kg = energy_kwh * self.grid_emission_factor_kg_kwh
        melt_co2_tonnes = melt_co2_kg / 1000.0
        
        # Specific energy consumption & carbon intensity
        sec_kwh_per_t = energy_kwh / output_tonnes
        scope2_intensity_tco2_per_t = melt_co2_tonnes / output_tonnes
        
        # Total estimated intensity (Scope 1 raw materials + Scope 2 electricity + Scope 3 auxiliary)
        # For induction MSME, Scope 2 electricity represents ~70-75% of gate-to-gate emissions
        estimated_total_intensity = scope2_intensity_tco2_per_t / 0.72
        
        # CBAM liability calculation (Excess over EU benchmark)
        excess_carbon_per_t = max(0.0, estimated_total_intensity - self.eu_foundry_benchmark_tco2_per_t)
        cbam_duty_eur_per_t = excess_carbon_per_t * self.eu_ets_carbon_price_eur
        cbam_duty_inr_per_t = cbam_duty_eur_per_t * self.eur_to_inr
        
        batch_total_cbam_liability_eur = cbam_duty_eur_per_t * output_tonnes
        batch_total_cbam_liability_inr = cbam_duty_inr_per_t * output_tonnes
        
        # Baseline comparison (Unoptimized Kolhapur foundry @ 850 kWh/t)
        unoptimized_sec = 850.0
        unoptimized_co2_t = (unoptimized_sec * self.grid_emission_factor_kg_kwh / 1000.0) / 0.72
        unoptimized_excess = max(0.0, unoptimized_co2_t - self.eu_foundry_benchmark_tco2_per_t)
        unoptimized_cbam_eur_per_t = unoptimized_excess * self.eu_ets_carbon_price_eur
        
        cbam_savings_eur_per_t = max(0.0, unoptimized_cbam_eur_per_t - cbam_duty_eur_per_t)
        cbam_savings_inr_per_t = cbam_savings_eur_per_t * self.eur_to_inr

        return {
            "batch_energy_kwh": round(energy_kwh, 2),
            "batch_tonnes": round(output_tonnes, 2),
            "sec_kwh_per_t": round(sec_kwh_per_t, 1),
            "scope2_emissions_kg": round(melt_co2_kg, 1),
            "scope2_emissions_tonnes": round(melt_co2_tonnes, 3),
            "carbon_intensity_tco2_per_t": round(estimated_total_intensity, 3),
            "india_average_benchmark_tco2": self.india_foundry_benchmark_tco2_per_t,
            "eu_target_benchmark_tco2": self.eu_foundry_benchmark_tco2_per_t,
            "cbam_excess_tco2_per_t": round(excess_carbon_per_t, 3),
            "cbam_duty_liability_eur_per_t": round(cbam_duty_eur_per_t, 2),
            "cbam_duty_liability_inr_per_t": round(cbam_duty_inr_per_t, 0),
            "batch_total_cbam_liability_inr": round(batch_total_cbam_liability_inr, 0),
            "cbam_savings_vs_unoptimized_inr_per_t": round(cbam_savings_inr_per_t, 0),
            "ets_carbon_price_eur": self.eu_ets_carbon_price_eur,
            "export_readiness_status": "EXCELLENT" if estimated_total_intensity <= 1.8 else ("MODERATE" if estimated_total_intensity <= 2.2 else "HIGH_RISK")
        }
