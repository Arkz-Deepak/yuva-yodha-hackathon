"""
Time-of-Use (ToU) Electricity Tariff Engine for Indian MSME Foundry Clusters
Based on Maharashtra State Electricity Distribution Co. Ltd. (MSEDCL) HT Industrial Tariffs
(Kolhapur Cluster Benchmark)
"""

from datetime import datetime, time
from typing import Dict, Any, List

class ToUTariffEngine:
    def __init__(self):
        # MSEDCL Industrial Tariff Slabs (INR per kWh)
        self.base_rate = 8.50  # Normal base tariff (INR/kWh)
        self.night_rebate = 1.50  # Night off-peak incentive (22:00 - 06:00): -1.50 INR/kWh
        self.peak_surcharge = 1.50  # Evening peak surcharge (18:00 - 22:00): +1.50 INR/kWh
        
    def get_tariff_for_time(self, dt: datetime = None) -> Dict[str, Any]:
        """Returns the active tariff slab and rate for the given timestamp."""
        if dt is None:
            dt = datetime.now()
            
        current_time = dt.time()
        
        # Slabs:
        # Off-Peak / Night: 22:00 to 06:00 -> Base - Rebate = 7.00 INR/kWh
        # Evening Peak: 18:00 to 22:00 -> Base + Surcharge = 10.00 INR/kWh
        # Normal Day: 06:00 to 18:00 -> Base = 8.50 INR/kWh
        
        if current_time >= time(22, 0) or current_time < time(6, 0):
            zone = "Off-Peak Night"
            rate = self.base_rate - self.night_rebate
            status_color = "#10b981"  # Green (Optimal)
            description = "Off-Peak Night Incentive active (-₹1.50/kWh rebate). Ideal for melting."
        elif time(18, 0) <= current_time < time(22, 0):
            zone = "Evening Peak"
            rate = self.base_rate + self.peak_surcharge
            status_color = "#ef4444"  # Red (Heavy Surcharge)
            description = "Peak Surcharge active (+₹1.50/kWh penalty). Shift melting if possible."
        else:
            zone = "Normal Day"
            rate = self.base_rate
            status_color = "#3b82f6"  # Blue (Standard)
            description = "Standard operational tariff slab."
            
        return {
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": dt.hour,
            "zone": zone,
            "rate_inr_kwh": rate,
            "base_rate": self.base_rate,
            "status_color": status_color,
            "description": description
        }

    def get_24h_schedule(self) -> List[Dict[str, Any]]:
        """Returns the full 24-hour tariff profile for schedule visualization."""
        schedule = []
        for hour in range(24):
            if hour >= 22 or hour < 6:
                zone = "Off-Peak Night"
                rate = self.base_rate - self.night_rebate
                surcharge_delta = -self.night_rebate
            elif 18 <= hour < 22:
                zone = "Evening Peak"
                rate = self.base_rate + self.peak_surcharge
                surcharge_delta = self.peak_surcharge
            else:
                zone = "Normal Day"
                rate = self.base_rate
                surcharge_delta = 0.0
                
            schedule.append({
                "hour": hour,
                "label": f"{hour:02d}:00",
                "zone": zone,
                "rate": rate,
                "delta": surcharge_delta
            })
        return schedule

    def optimize_batch_start(self, batch_duration_mins: float = 65.0, est_energy_kwh: float = 900.0, current_dt: datetime = None) -> Dict[str, Any]:
        """
        Calculates optimal start time for next batch to minimize electricity bill.
        Compares starting immediately vs advancing/delaying to capture off-peak rebates.
        """
        if current_dt is None:
            current_dt = datetime.now()
            
        curr_tariff = self.get_tariff_for_time(current_dt)
        curr_cost = est_energy_kwh * curr_tariff["rate_inr_kwh"]
        
        # Test offset windows (-30, 0, +15, +30, +45, +60, +90, +120 mins)
        candidates = []
        for offset_mins in [0, 15, 30, 45, 60, 90, 120]:
            from datetime import timedelta
            start_cand = current_dt + timedelta(minutes=offset_mins)
            mid_cand = start_cand + timedelta(minutes=batch_duration_mins / 2)
            tariff_info = self.get_tariff_for_time(mid_cand)
            cand_cost = est_energy_kwh * tariff_info["rate_inr_kwh"]
            savings = curr_cost - cand_cost
            
            candidates.append({
                "offset_minutes": offset_mins,
                "start_time": start_cand.strftime("%H:%M"),
                "zone": tariff_info["zone"],
                "rate": tariff_info["rate_inr_kwh"],
                "projected_cost_inr": round(cand_cost, 2),
                "potential_savings_inr": round(savings, 2)
            })
            
        # Best candidate with max savings
        best = max(candidates, key=lambda c: c["potential_savings_inr"])
        
        recommendation = "Start immediately. Current tariff is favorable."
        if best["potential_savings_inr"] > 0:
            recommendation = (
                f"Shift next batch start by +{best['offset_minutes']} mins (to {best['start_time']}) "
                f"to hit {best['zone']} slab and save ₹{best['potential_savings_inr']:.0f} on this batch."
            )
            
        return {
            "current_start": current_dt.strftime("%H:%M"),
            "current_tariff_zone": curr_tariff["zone"],
            "current_rate_inr": curr_tariff["rate_inr_kwh"],
            "baseline_batch_cost_inr": round(curr_cost, 2),
            "best_option": best,
            "all_options": candidates,
            "recommendation": recommendation
        }
