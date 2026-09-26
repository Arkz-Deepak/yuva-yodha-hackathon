"""
EcoCast AI - Enterprise MSME Gateway & Digital Twin Orchestrator
Schneider Electric Yuva Yodha Energy Tech Hackathon 2026
Challenge 4: Smart Manufacturing - Industrial Energy & Process Efficiency
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel

from backend.simulator import InductionFurnaceSimulator
from backend.tou_optimizer import ToUTariffEngine
from backend.cbam_ledger import CBAMLedger
from backend.ml_engine import MeltPredictorML
from backend.bee_pat import BEEPatSchemeEngine
from backend.certificate_generator import CertificateGenerator
from backend.modbus_driver import SchneiderModbusDriver
from backend.heat_history import HeatHistoryManager

app = FastAPI(
    title="EcoCast AI - Schneider EcoStruxure Edge MSME Gateway",
    description="Factory-ready decision-support digital twin for induction furnaces (Kolhapur Cluster Benchmark)",
    version="2.0.0"
)

# Enable CORS for Vite dev and production
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
pat_engine = BEEPatSchemeEngine()
cert_generator = CertificateGenerator(export_dir="exports")
modbus_driver = SchneiderModbusDriver()
heat_history = HeatHistoryManager(data_file="data/heats_ledger.json")

# WebSocket connection manager
active_connections: list[WebSocket] = []

class ControlRequest(BaseModel):
    action: str  # "start_batch", "toggle_lid", "trigger_delay", "tap", "reset", "set_speed"
    batch_weight_kg: Optional[float] = 1500.0
    target_temp_c: Optional[float] = 1520.0
    speed: Optional[float] = 12.0

class ModbusConfigRequest(BaseModel):
    mode: str = "SIMULATION"  # "SIMULATION" or "LIVE_MODBUS"
    host: str = "127.0.0.1"
    port: int = 502
    slave_id: int = 1
    meter_model: str = "Schneider Electric EasyLogic™ PM5350"

@app.get("/api/status")
def get_status() -> Dict[str, Any]:
    """Returns the consolidated digital twin and edge gateway status."""
    tariff_info = tou_engine.get_tariff_for_time()
    
    # If in live Modbus mode, check if physical telemetry is available
    if modbus_driver.mode == "LIVE_MODBUS" and modbus_driver.is_connected:
        live_hw = modbus_driver.read_telemetry()
        if live_hw:
            simulator.active_power_kw = live_hw["active_power_kw"]
            simulator.reactive_power_kvar = live_hw["reactive_power_kvar"]
            simulator.power_factor = live_hw["power_factor"]
            
    telemetry = simulator.tick(active_tariff_rate=tariff_info["rate_inr_kwh"])
    
    cbam_info = cbam_ledger.calculate_batch_carbon(
        energy_kwh=telemetry["cumulative_kwh"],
        output_tonnes=telemetry["batch_weight_tonnes"]
    )
    pat_info = pat_engine.evaluate_batch_pat_compliance(
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
    
    # If batch is tapping or complete, sync with heat history
    if telemetry["state"] in ["TAPPING", "HOLDING"] and telemetry["cumulative_kwh"] > 500:
        heat_history.add_or_update_heat({
            "heat_id": telemetry["batch_id"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weighbridge_tonnes": telemetry["batch_weight_tonnes"],
            "metered_kwh": telemetry["cumulative_kwh"],
            "sec_kwh_per_t": telemetry["sec_kwh_per_tonne"],
            "holding_minutes": telemetry["holding_minutes"],
            "holding_cost_inr": telemetry["holding_cost_inr"],
            "scope2_intensity_tco2": cbam_info["scope2_emissions_tonnes"] / telemetry["batch_weight_tonnes"],
            "total_intensity_tco2": cbam_info["carbon_intensity_tco2_per_t"],
            "cbam_status": cbam_info["export_readiness_status"],
            "cbam_savings_inr": cbam_info["cbam_savings_vs_unoptimized_inr_per_t"],
            "escerts_earned": pat_info["escerts_earned_per_batch"],
            "gateway_id": "SE-ECO-EDGE-4102",
            "status": "COMPLETED" if telemetry["state"] == "TAPPING" else "ACTIVE"
        })

    return {
        "telemetry": telemetry,
        "tariff": tariff_info,
        "cbam": cbam_info,
        "pat": pat_info,
        "ml_forecast": ml_forecast,
        "modbus": modbus_driver.get_status()
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
        # Record completed heat
        tariff_info = tou_engine.get_tariff_for_time()
        telem = simulator.get_telemetry(active_tariff_rate=tariff_info["rate_inr_kwh"])
        cbam_info = cbam_ledger.calculate_batch_carbon(telem["cumulative_kwh"], telem["batch_weight_tonnes"])
        pat_info = pat_engine.evaluate_batch_pat_compliance(telem["cumulative_kwh"], telem["batch_weight_tonnes"])
        heat_history.add_or_update_heat({
            "heat_id": telem["batch_id"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weighbridge_tonnes": telem["batch_weight_tonnes"],
            "metered_kwh": telem["cumulative_kwh"],
            "sec_kwh_per_t": telem["sec_kwh_per_tonne"],
            "holding_minutes": telem["holding_minutes"],
            "holding_cost_inr": telem["holding_cost_inr"],
            "scope2_intensity_tco2": cbam_info["scope2_emissions_tonnes"] / telem["batch_weight_tonnes"],
            "total_intensity_tco2": cbam_info["carbon_intensity_tco2_per_t"],
            "cbam_status": cbam_info["export_readiness_status"],
            "cbam_savings_inr": cbam_info["cbam_savings_vs_unoptimized_inr_per_t"],
            "escerts_earned": pat_info["escerts_earned_per_batch"],
            "gateway_id": "SE-ECO-EDGE-4102",
            "status": "COMPLETED"
        })
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

@app.get("/api/pat/metrics")
def get_pat_metrics():
    """Returns BEE PAT Scheme compliance and ESCerts metrics."""
    telemetry = simulator.get_telemetry()
    return pat_engine.evaluate_batch_pat_compliance(
        energy_kwh=telemetry["cumulative_kwh"],
        output_tonnes=telemetry["batch_weight_tonnes"]
    )

@app.get("/api/heats")
def get_heat_records():
    """Returns all logged heats for regulatory audit."""
    return heat_history.get_all_heats()

@app.get("/api/certificate/pdf/{heat_id}")
def download_certificate_pdf(heat_id: int):
    """Generates and downloads the official digitally stamped PDF audit certificate."""
    heat = heat_history.get_heat_by_id(heat_id)
    if not heat:
        # Fallback to current heat
        telem = simulator.get_telemetry()
        heat = {
            "heat_id": heat_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weighbridge_tonnes": telem["batch_weight_tonnes"],
            "metered_kwh": max(900.0, telem["cumulative_kwh"]),
            "facility_name": "Kolhapur Foundry Cluster Unit #14 (MIDC Shiroli)",
            "meter_model": modbus_driver.meter_model,
            "gateway_id": "SE-ECO-EDGE-4102"
        }
    
    pdf_bytes = cert_generator.generate_pdf(heat)
    filename = f"CBAM_BEE_Audit_Certificate_HEAT_{heat_id}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.get("/api/certificate/csv")
def download_audit_csv():
    """Exports full regulatory heat ledger as CSV for customs or BEE verification."""
    heats = heat_history.get_all_heats()
    csv_str = cert_generator.generate_csv_audit_log(heats)
    filename = f"Kolhapur_CBAM_BEE_Audit_Ledger_{datetime.now().strftime('%Y%m%d')}.csv"
    
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.get("/api/modbus/status")
def get_modbus_status():
    """Returns hardware Modbus-TCP driver status."""
    return modbus_driver.get_status()

@app.post("/api/modbus/config")
def configure_modbus(req: ModbusConfigRequest):
    """Configures industrial Modbus-TCP gateway parameters."""
    res = modbus_driver.configure(
        host=req.host,
        port=req.port,
        slave_id=req.slave_id,
        meter_model=req.meter_model,
        mode=req.mode
    )
    return res

@app.get("/api/analytics/kolhapur")
def get_kolhapur_analytics():
    """Benchmarking data based on UNIDO-BEE Kolhapur MSME Foundry Cluster case studies."""
    return {
        "cluster_name": "Kolhapur MSME Foundry Cluster, Maharashtra",
        "total_units": 300,
        "annual_castings_tonnes": 600000,
        "cluster_annual_energy_toe": 166910,
        "sec_benchmarks": {
            "unoptimized_typical": 850.0,
            "kolhapur_average": 770.0,
            "bee_target_igbt": 625.0,
            "global_best_in_class": 580.0
        },
        "schneider_hardware_compatibility": [
            "EasyLogic™ PM5350 / PM5110 / PM1200 Power & Energy Meters",
            "PowerLogic™ ION9000 / PM8000 Advanced Power Quality Meters",
            "EcoStruxure™ Edge Box (Magelis / Harmony iPC) Industrial Edge",
            "Altivar™ Process ATV600 / ATV900 Variable Speed Drives",
            "TeSys™ Island Smart Motor Management"
        ]
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """Streams live telemetry at 1 Hz to connected 3D digital twins and dashboards."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            tariff_info = tou_engine.get_tariff_for_time()
            
            # Modbus check
            if modbus_driver.mode == "LIVE_MODBUS" and modbus_driver.is_connected:
                live_hw = modbus_driver.read_telemetry()
                if live_hw:
                    simulator.active_power_kw = live_hw["active_power_kw"]
                    simulator.reactive_power_kvar = live_hw["reactive_power_kvar"]
                    simulator.power_factor = live_hw["power_factor"]

            telemetry = simulator.tick(active_tariff_rate=tariff_info["rate_inr_kwh"])
            cbam_info = cbam_ledger.calculate_batch_carbon(
                energy_kwh=telemetry["cumulative_kwh"],
                output_tonnes=telemetry["batch_weight_tonnes"]
            )
            pat_info = pat_engine.evaluate_batch_pat_compliance(
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
                "pat": pat_info,
                "ml_forecast": ml_forecast,
                "modbus": modbus_driver.get_status()
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
    except Exception:
        if websocket in active_connections:
            active_connections.remove(websocket)

# Mount frontend build if dist folder exists
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
