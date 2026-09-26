"""
EcoCast AI - FastAPI Gateway & Digital Twin Orchestrator
Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric)
Challenge 4: Smart Manufacturing - Industrial Energy & Process Efficiency
"""

import os
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.simulator import InductionFurnaceSimulator
from backend.tou_optimizer import ToUTariffEngine
from backend.cbam_ledger import CBAMLedger
from backend.ml_engine import MeltPredictorML

app = FastAPI(
    title="EcoCast AI - Induction Furnace Digital Twin",
    description="Edge decision-support digital twin for MSME foundries (Kolhapur Cluster Benchmark)",
    version="1.0.0"
)

# Enable CORS for React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate core engines
simulator = InductionFurnaceSimulator(capacity_kg=1500.0, rated_power_kw=750.0)
tou_engine = ToUTariffEngine()
cbam_ledger = CBAMLedger()
ml_engine = MeltPredictorML(data_dir="data")

# WebSocket connection manager
active_connections: list[WebSocket] = []

class ControlRequest(BaseModel):
    action: str  # "start_batch", "toggle_lid", "trigger_delay", "tap", "reset", "set_speed"
    batch_weight_kg: Optional[float] = 1500.0
    target_temp_c: Optional[float] = 1520.0
    speed: Optional[float] = 12.0

@app.get("/api/status")
def get_status() -> Dict[str, Any]:
    """Returns the consolidated digital twin status."""
    tariff_info = tou_engine.get_tariff_for_time()
    telemetry = simulator.tick(active_tariff_rate=tariff_info["rate_inr_kwh"])
    cbam_info = cbam_ledger.calculate_batch_carbon(
        energy_kwh=telemetry["cumulative_kwh"],
        output_tonnes=telemetry["batch_weight_tonnes"]
    )
    ml_forecast = ml_engine.predict_batch_profile(
        batch_weight_kg=telemetry["batch_weight_kg"],
        current_temp_c=telemetry["temperature_c"],
        target_temp_c=telemetry["target_temperature_c"],
        avg_power_kw=telemetry["active_power_kw"] if telemetry["active_power_kw"] > 100 else 700.0,
        lid_is_closed=telemetry["lid_is_closed"]
    )
    
    return {
        "telemetry": telemetry,
        "tariff": tariff_info,
        "cbam": cbam_info,
        "ml_forecast": ml_forecast
    }

@app.post("/api/control")
def execute_control(req: ControlRequest) -> Dict[str, Any]:
    """Executes operator and shop-floor actions on the digital twin."""
    if req.action == "start_batch":
        simulator.start_batch(weight_kg=req.batch_weight_kg, target_temp_c=req.target_temp_c)
    elif req.action == "toggle_lid":
        simulator.toggle_lid()
    elif req.action == "trigger_delay":
        simulator.trigger_holding_delay()
    elif req.action == "tap":
        simulator.tap_furnace()
    elif req.action == "reset":
        simulator.reset_to_idle()
    elif req.action == "set_speed" and req.speed:
        simulator.time_compression = max(1.0, min(50.0, req.speed))
    else:
        return {"status": "error", "message": f"Unknown action: {req.action}"}
        
    tariff_info = tou_engine.get_tariff_for_time()
    return {
        "status": "success",
        "action": req.action,
        "telemetry": simulator.get_telemetry(active_tariff_rate=tariff_info["rate_inr_kwh"])
    }

@app.get("/api/tou/schedule")
def get_tou_schedule():
    """Returns 24h tariff slabs and dynamic batch start recommendation."""
    schedule = tou_engine.get_24h_schedule()
    current_tariff = tou_engine.get_tariff_for_time()
    optimizer_rec = tou_engine.optimize_batch_start(
        batch_duration_mins=65.0,
        est_energy_kwh=930.0
    )
    return {
        "current_tariff": current_tariff,
        "schedule_24h": schedule,
        "optimization": optimizer_rec
    }

@app.get("/api/cbam/report")
def get_cbam_report():
    """Returns EU CBAM audit metrics and carbon ledger."""
    telemetry = simulator.get_telemetry()
    return cbam_ledger.calculate_batch_carbon(
        energy_kwh=telemetry["cumulative_kwh"],
        output_tonnes=telemetry["batch_weight_tonnes"]
    )

@app.get("/api/analytics/kolhapur")
def get_kolhapur_analytics():
    """Benchmarking data based on UNIDO-BEE Kolhapur MSME Foundry Cluster case studies."""
    return {
        "cluster_name": "Kolhapur MSME Foundry Cluster, Maharashtra",
        "total_units": 300,
        "annual_castings_tonnes": 600000,
        "cluster_annual_energy_toe": 166910,
        "sec_benchmarks": {
            "unoptimized_typical": 850.0,  # kWh/t
            "kolhapur_average": 770.0,     # kWh/t
            "bee_target_igbt": 625.0,      # kWh/t
            "global_best_in_class": 580.0  # kWh/t
        },
        "documented_bee_interventions": [
            {
                "measure": "Furnace Lid Automation Mechanism",
                "investment_inr": 560000,
                "annual_savings_kwh": 208380,
                "payback_years": 0.4,
                "impact": "Eliminates ~32.7 kWh/batch radiation loss"
            },
            {
                "measure": "IGBT Induction Power Supply Upgrade",
                "investment_inr": 2300000,
                "annual_savings_inr": 3600000,
                "payback_years": 0.7,
                "impact": "Drops SEC from 850 to 625 kWh/t (26% net reduction)"
            },
            {
                "measure": "ToU Batch Schedule & Holding Time Elimination",
                "investment_inr": 0,
                "annual_savings_inr": 1850000,
                "payback_years": 0.0,
                "impact": "Saves 120-150 kWh per idle hour; shifts melts to night discount"
            }
        ]
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """Streams live telemetry at 1 Hz to connected 3D digital twins and dashboards."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Advance simulation tick
            tariff_info = tou_engine.get_tariff_for_time()
            telemetry = simulator.tick(active_tariff_rate=tariff_info["rate_inr_kwh"])
            cbam_info = cbam_ledger.calculate_batch_carbon(
                energy_kwh=telemetry["cumulative_kwh"],
                output_tonnes=telemetry["batch_weight_tonnes"]
            )
            ml_forecast = ml_engine.predict_batch_profile(
                batch_weight_kg=telemetry["batch_weight_kg"],
                current_temp_c=telemetry["temperature_c"],
                target_temp_c=telemetry["target_temperature_c"],
                avg_power_kw=telemetry["active_power_kw"] if telemetry["active_power_kw"] > 100 else 700.0,
                lid_is_closed=telemetry["lid_is_closed"]
            )
            
            payload = {
                "telemetry": telemetry,
                "tariff": tariff_info,
                "cbam": cbam_info,
                "ml_forecast": ml_forecast
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
    except Exception as e:
        if websocket in active_connections:
            active_connections.remove(websocket)

# Mount frontend build if dist folder exists
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
