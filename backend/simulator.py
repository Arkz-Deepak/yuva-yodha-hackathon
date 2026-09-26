"""
Induction Furnace Physics & Telemetry Engine (EcoCast Digital Twin)
Models thermodynamic heat transfer, electrical efficiency, radiation loss,
and holding waste for a 1.5 MT medium-frequency coreless induction furnace.
"""

import time
import math
import random
from datetime import datetime
from typing import Dict, Any, List

class InductionFurnaceSimulator:
    def __init__(self, capacity_kg: float = 1500.0, rated_power_kw: float = 750.0):
        self.capacity_kg = capacity_kg      # Rated melt batch size (1.5 Metric Tonnes)
        self.rated_power_kw = rated_power_kw # 750 kW IGBT inverter
        
        # State machine: IDLE, CHARGING, MELTING, REFINING, SUPERHEATING, HOLDING, TAPPING
        self.state = "IDLE"
        self.batch_id = 1042
        self.batch_weight_kg = 1500.0
        
        # Thermal & Electrical Parameters
        self.temperature_c = 28.0           # Pyrometer bath temperature
        self.target_temperature_c = 1520.0  # Tapping setpoint for gray/ductile iron
        self.active_power_kw = 0.0          # Instantaneous active power
        self.reactive_power_kvar = 0.0      # Instantaneous reactive power
        self.power_factor = 0.96            # Power factor
        self.voltage_v = 1200.0             # Coil voltage
        self.current_a = 0.0                # Coil current
        self.coil_water_in_c = 28.0         # Coil cooling water inlet temp
        self.coil_water_out_c = 34.0        # Coil cooling water outlet temp
        
        # Physical Mechanisms
        self.lid_is_closed = True           # True = insulated lid closed, False = radiation escape
        self.tilt_angle_deg = 0.0           # Hydraulic tilt angle (0 to 75 deg)
        self.molten_fraction = 0.0          # 0.0 (solid scrap) to 1.0 (fully liquid)
        
        # Energy & Metrics
        self.cumulative_kwh = 0.0           # Total kWh for current batch
        self.sec_kwh_per_tonne = 0.0        # Specific Energy Consumption (kWh/t)
        self.batch_start_time = None
        self.last_tick_time = time.time()
        
        # Holding Loss Tracking (The critical MSME efficiency leak)
        self.holding_seconds = 0.0
        self.holding_energy_kwh = 0.0
        self.holding_cost_inr = 0.0
        self.holding_co2_kg = 0.0
        
        # Simulation speed multiplier (e.g. 5x or 10x for interactive hackathon demo)
        self.time_compression = 12.0  # 1 real second = 12 simulation seconds (a 60-min melt finishes in ~5 mins demo)
        self.is_paused = False

    def start_batch(self, weight_kg: float = 1500.0, target_temp_c: float = 1520.0):
        """Initializes a new melting batch."""
        self.batch_id += 1
        self.batch_weight_kg = weight_kg
        self.target_temperature_c = target_temp_c
        self.temperature_c = 32.0
        self.molten_fraction = 0.0
        self.cumulative_kwh = 0.0
        self.sec_kwh_per_tonne = 0.0
        self.holding_seconds = 0.0
        self.holding_energy_kwh = 0.0
        self.holding_cost_inr = 0.0
        self.holding_co2_kg = 0.0
        self.tilt_angle_deg = 0.0
        self.lid_is_closed = True
        self.state = "CHARGING"
        self.batch_start_time = datetime.now()
        self.last_tick_time = time.time()
        print(f"[EcoCast Simulator] Started Batch #{self.batch_id} ({weight_kg} kg, target {target_temp_c}°C)")

    def toggle_lid(self) -> bool:
        """Toggles the furnace cover lid open/closed."""
        self.lid_is_closed = not self.lid_is_closed
        return self.lid_is_closed

    def trigger_holding_delay(self):
        """Simulates a shop-floor delay (e.g., ladle crane not ready, molds delayed)."""
        if self.state in ["MELTING", "SUPERHEATING", "REFINING"]:
            self.temperature_c = max(self.temperature_c, 1515.0)
            self.molten_fraction = 1.0
            self.state = "HOLDING"
            self.active_power_kw = 135.0  # Holding equilibrium power
            print("[EcoCast Simulator] UNPRODUCTIVE HOLDING STATE TRIGGERED - Ladle delay simulated!")

    def tap_furnace(self):
        """Triggers tapping into ladle."""
        if self.temperature_c >= 1480.0:
            self.state = "TAPPING"
            self.active_power_kw = 25.0
            self.lid_is_closed = False
            print("[EcoCast Simulator] Tapping metal into transport ladle...")

    def reset_to_idle(self):
        """Resets furnace to idle state."""
        self.state = "IDLE"
        self.active_power_kw = 0.0
        self.current_a = 0.0
        self.temperature_c = 30.0
        self.tilt_angle_deg = 0.0
        self.lid_is_closed = True

    def tick(self, active_tariff_rate: float = 8.50) -> Dict[str, Any]:
        """
        Advances the physical simulation by elapsed real time * time_compression.
        Returns the instantaneous telemetry snapshot.
        """
        now = time.time()
        real_dt = now - self.last_tick_time
        self.last_tick_time = now
        
        if self.is_paused or real_dt <= 0:
            return self.get_telemetry(active_tariff_rate)
            
        dt_sim = real_dt * self.time_compression  # Simulated seconds elapsed
        dt_hours = dt_sim / 3600.0
        
        # State machine transition & power dynamics
        if self.state == "IDLE":
            self.active_power_kw = 0.0
            self.temperature_c = max(30.0, self.temperature_c - 0.05 * dt_sim)
            self.tilt_angle_deg = 0.0
            
        elif self.state == "CHARGING":
            self.active_power_kw = 60.0  # Low scrap pre-warming
            self.temperature_c = 40.0 + random.uniform(-1, 1)
            # Auto-advance charging after 15 simulated seconds
            if self.cumulative_kwh > 5.0 or dt_sim > 5:
                self.state = "MELTING"
                
        elif self.state == "MELTING":
            # High efficiency ramp phase
            target_kw = 715.0 + random.uniform(-10, 10)
            self.active_power_kw = min(self.rated_power_kw, target_kw)
            
            # Specific heat cp of steel ~ 0.68 kJ/(kg K)
            # Latent heat of fusion L ~ 270 kJ/kg (between 1350°C and 1450°C)
            # Input energy delta (kWh)
            energy_in_kwh = self.active_power_kw * dt_hours
            
            # Loss calculations
            # Radiation loss: Q_rad = eps * sigma * Area * (T_melt^4 - T_amb^4)
            # When lid is closed: loss is suppressed by 85%
            lid_factor = 0.15 if self.lid_is_closed else 1.0
            rad_loss_kw = 45.0 * lid_factor * ((self.temperature_c + 273.15) / 1793.15) ** 4
            coil_loss_kw = self.active_power_kw * 0.16  # ~16% coil cooling water loss
            elec_loss_kw = self.active_power_kw * 0.05  # Inverter & busbar losses
            
            net_useful_kw = max(0.0, self.active_power_kw - (rad_loss_kw + coil_loss_kw + elec_loss_kw))
            useful_energy_kj = net_useful_kw * dt_sim  # kW * s = kJ
            
            # Temperature rise
            # In solid phase (T < 1350°C):
            if self.temperature_c < 1350.0:
                heat_cap_kj_per_c = self.batch_weight_kg * 0.68
                self.temperature_c += useful_energy_kj / heat_cap_kj_per_c
                self.molten_fraction = max(0.0, (self.temperature_c - 1000.0) / 450.0)
            # In phase change (1350°C to 1450°C):
            elif self.temperature_c < 1450.0:
                latent_needed_kj = self.batch_weight_kg * 270.0
                latent_added_kj = useful_energy_kj
                self.temperature_c += (useful_energy_kj / (self.batch_weight_kg * 0.68)) * 0.35
                self.molten_fraction = min(1.0, 0.4 + 0.6 * ((self.temperature_c - 1350.0) / 100.0))
            else:
                # Liquid superheating
                self.molten_fraction = 1.0
                heat_cap_kj_per_c = self.batch_weight_kg * 0.82
                self.temperature_c += useful_energy_kj / heat_cap_kj_per_c
                
            if self.temperature_c >= 1430.0:
                self.state = "REFINING"
                
        elif self.state == "REFINING":
            # Power reduced for slag skimming, ferroalloy additions, and sampling
            self.active_power_kw = 480.0 + random.uniform(-15, 15)
            dt_energy = self.active_power_kw * dt_hours
            self.temperature_c += (dt_sim * 0.08)  # Gradual rise
            if self.temperature_c >= 1485.0:
                self.state = "SUPERHEATING"
                
        elif self.state == "SUPERHEATING":
            # Final power push to target tapping temp (1520°C)
            self.active_power_kw = 640.0 + random.uniform(-10, 10)
            self.temperature_c += (dt_sim * 0.12)
            if self.temperature_c >= self.target_temperature_c:
                # Automatically enter holding if not immediately tapped
                self.state = "HOLDING"
                print(f"[EcoCast Simulator] Batch reached target tapping temp {self.target_temperature_c}°C! Switched to HOLDING.")
                
        elif self.state == "HOLDING":
            # Unproductive hold! Power holds temperature around setpoint (1515 - 1525°C)
            # Burning ~125-145 kW continuously
            self.active_power_kw = 135.0 + random.uniform(-5, 5)
            self.temperature_c = self.target_temperature_c + math.sin(time.time()) * 3.0
            
            # Accumulate holding waste
            hold_kwh = self.active_power_kw * dt_hours
            self.holding_seconds += dt_sim
            self.holding_energy_kwh += hold_kwh
            self.holding_cost_inr += hold_kwh * active_tariff_rate
            self.holding_co2_kg += hold_kwh * 0.82  # CEA grid emission factor
            
        elif self.state == "TAPPING":
            # Furnace tilts to pour molten metal
            self.active_power_kw = 25.0
            if self.tilt_angle_deg < 65.0:
                self.tilt_angle_deg += 1.5 * (dt_sim / 2.0)
            else:
                # Tapping complete
                self.state = "IDLE"
                self.tilt_angle_deg = 0.0
                self.temperature_c = 150.0
                print(f"[EcoCast Simulator] Tapping finished for Batch #{self.batch_id}!")

        # Energy accumulation
        batch_energy_step = self.active_power_kw * dt_hours
        self.cumulative_kwh += batch_energy_step
        tonnes = self.batch_weight_kg / 1000.0
        self.sec_kwh_per_tonne = self.cumulative_kwh / tonnes if tonnes > 0 else 0.0
        
        # Electrical harmonics & cooling
        self.reactive_power_kvar = self.active_power_kw * 0.28 + random.uniform(-3, 3)
        self.power_factor = 0.965 if self.active_power_kw > 100 else 0.88
        self.current_a = (self.active_power_kw * 1000.0) / (math.sqrt(3) * self.voltage_v * self.power_factor) if self.active_power_kw > 10 else 0.0
        self.coil_water_out_c = self.coil_water_in_c + (self.active_power_kw * 0.018)

        return self.get_telemetry(active_tariff_rate)

    def get_telemetry(self, active_tariff_rate: float = 8.50) -> Dict[str, Any]:
        """Returns the full digital twin status packet."""
        tonnes = self.batch_weight_kg / 1000.0
        
        # Radiation loss estimate in kW
        lid_loss_factor = 0.15 if self.lid_is_closed else 1.0
        rad_loss_kw = round(45.0 * lid_loss_factor * ((self.temperature_c + 273.15) / 1793.15) ** 4, 1)
        
        # Real-time holding cost burn rate (INR/hour and INR/min)
        holding_burn_rate_inr_per_min = round((self.active_power_kw / 60.0) * active_tariff_rate, 2) if self.state == "HOLDING" else 0.0
        
        return {
            "batch_id": self.batch_id,
            "state": self.state,
            "is_holding_alert": self.state == "HOLDING",
            "temperature_c": round(self.temperature_c, 1),
            "target_temperature_c": self.target_temperature_c,
            "molten_fraction": round(self.molten_fraction, 2),
            "batch_weight_kg": self.batch_weight_kg,
            "batch_weight_tonnes": tonnes,
            "active_power_kw": round(self.active_power_kw, 1),
            "rated_power_kw": self.rated_power_kw,
            "reactive_power_kvar": round(self.reactive_power_kvar, 1),
            "power_factor": round(self.power_factor, 3),
            "current_a": round(self.current_a, 1),
            "voltage_v": round(self.voltage_v, 1),
            "coil_water_in_c": round(self.coil_water_in_c, 1),
            "coil_water_out_c": round(self.coil_water_out_c, 1),
            "lid_is_closed": self.lid_is_closed,
            "radiation_loss_kw": rad_loss_kw,
            "tilt_angle_deg": round(self.tilt_angle_deg, 1),
            "cumulative_kwh": round(self.cumulative_kwh, 2),
            "sec_kwh_per_tonne": round(self.sec_kwh_per_tonne, 1),
            "bee_benchmark_sec": 625.0,
            "holding_minutes": round(self.holding_seconds / 60.0, 1),
            "holding_energy_kwh": round(self.holding_energy_kwh, 2),
            "holding_cost_inr": round(self.holding_cost_inr, 2),
            "holding_co2_kg": round(self.holding_co2_kg, 2),
            "holding_burn_rate_inr_per_min": holding_burn_rate_inr_per_min,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
