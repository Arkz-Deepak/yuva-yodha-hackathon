# EcoCast AI: Decision-Support Digital Twin for MSME Induction Furnaces

> **Schneider Electric Yuva Yodha Energy Tech Hackathon 2026**  
> **Track:** Challenge 4 — Smart Manufacturing: Industrial Energy & Process Efficiency  
> **Benchmark Context:** Kolhapur MSME Foundry Cluster, Maharashtra, India  

---

## 🚀 Executive Summary

In India's MSME foundry clusters (such as Kolhapur, with 300+ units producing 600,000 tonnes of automotive castings annually), electricity costs represent **30% to 50% of total manufacturing costs**, with medium-frequency induction melting furnaces consuming over **70% of that energy**. 

While equipment-level upgrades (like IGBT conversions) deliver value, Bureau of Energy Efficiency (BEE) and UNIDO audits reveal that **9% to 45% of equipment-specific energy losses stem from decision-level inefficiencies**:
1. **Unsynchronized Melting & Molten Holding Waste:** Furnaces reach tapping temperature (1520°C) too early and idle for 20–60 minutes awaiting cranes or molds, burning **120–150 kWh every idle hour** in radiation and standby losses.
2. **Time-of-Use (ToU) Blindness:** Operators melt during expensive evening peak surcharge hours (+₹1.50/unit) instead of scheduling heavy melting during off-peak night discount windows (-₹1.50/unit).
3. **Open Crucible Radiation:** Operating without insulated covers leaks **~32.7 kWh per batch** in thermal radiation.
4. **EU CBAM Border Tax Exposure:** With the European Union's Carbon Border Adjustment Mechanism (CBAM) active in 2026, Indian exporters emitting ~2.5 tCO₂/t face **₹7,450 to ₹16,200/tonne in cross-border import penalties**, threatening the 30% of castings Kolhapur exports.

**EcoCast AI** is an edge-native, lightweight decision-support digital twin engineered specifically for MSME foundries. It delivers production-aware intelligence on top of standard energy meters without requiring multi-crore SCADA overhauls.

---

## 🛠️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                           ECOCAST DIGITAL TWIN ARCHITECTURE                       |
+-----------------------------------------------------------------------------------+

 [ Industrial Sensor Ingestion ]
      - Schneider EasyLogic / EM6400 Energy Meter Telemetry (Active kW, kVAR, PF, V, I)
      - Non-contact Pyrometer Bath Temp (°C), Coil Cooling Water (°C), Bath Weight (kg)
      - Modbus-TCP / MQTT Event Streaming Gateway
                     |
                     v
 [ FastAPI Edge Intelligence Gateway (Python 3.13) ]
      |-- 1. Thermodynamic & Physics Simulator: Coreless induction furnace modeling
      |-- 2. SEC Engine: Specific Energy Consumption (kWh/tonne) vs BEE Benchmark
      |-- 3. ToU Tariff Engine: Dynamic MSEDCL tariff optimization & batch start scheduler
      |-- 4. Holding Guard: Real-time ₹/min monetary leak and CO2 penalty tracker
      |-- 5. Machine Learning Predictor: Scikit-learn melt duration & power ramp models
      |-- 6. EU CBAM Carbon Ledger: Export compliance & carbon intensity tracking
                     |
                     v (WebSocket @ 1 Hz & REST API)
 [ Modern Operator HMI & 3D Digital Twin (React + Three.js + Tailwind CSS) ]
      |-- Three.js 3D Twin: Interactive crucible with dynamic heat shader & hydraulic tilt
      |-- Holding Guard Alarm: High-urgency warning with live monetary loss ticker
      |-- SEC Target Gauge: Instantaneous kWh/t vs 625 kWh/t BEE star standard
      |-- 24h ToU Timeline: Shift melt recommendation for off-peak power discounts
      |-- CBAM Carbon Card: Embodied tCO2/t and export tariff protection calculator
```

---

## 👥 Team & Responsibilities

| Team Member | Details & Affiliation | Core Focus & Responsibilities |
| :--- | :--- | :--- |
| **Deepak R** | **Team Lead**<br/>Indian Institute of Petroleum and Energy (IIPE) | **Full-Stack Architecture & 3D Digital Twin:** Engineered the FastAPI edge gateway, real-time WebSocket telemetry pipeline, Three.js 3D crucible twin, operator HMI dashboard, Modbus-TCP hardware driver, and end-to-end simulation mechanics. |
| **Saranya Dutta** | **Team Member**<br/>Email: `saranyadutta@iipe.ac.in`<br/>Indian Institute of Petroleum and Energy (IIPE) | **Chemical Process & Energy Modeling:** Validated thermodynamic melt energy balance, induction furnace phase change calculations, Specific Energy Consumption (SEC) benchmarks, EU CBAM carbon ledger modeling, and BEE PAT scheme compliance. |

---

## 📊 Quantified Impact & Payback

* **Energy Cost Reduction:** **12% to 18%** net electricity bill savings by eliminating idle molten holding time and shifting heavy melting to off-peak tariff slabs.
* **Annual Savings per MSME Unit:** **₹30 Lakhs to ₹45 Lakhs** per year (for a typical 2,500 T/year foundry with a ₹2.5 Crore annual power bill).
* **Decarbonization:** Avoids **350–500 tonnes of CO₂** per unit per year.
* **Simple Payback Period:** **Under 6 months** (zero major hardware CapEx required).
* **Schneider Electric Ecosystem Fit:** Extends Schneider’s *EcoStruxure Power & Process* philosophy to India's 5,000+ MSME manufacturing plants, driving hardware adoption for Schneider energy meters, drives, and smart relays.

---

## ⚡ Quickstart

### 1. Launch with One Click (Windows)
Double-click `run.bat` or run in terminal:
```powershell
.\run.bat
```

### 2. Manual Launch
```powershell
# Install backend dependencies (if needed)
pip install -r requirements.txt

# Start backend server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open your browser to: **[http://localhost:8000](http://localhost:8000)**

---

## 📁 Repository Structure

```
yuva-yodha-hackathon/
├── backend/
│   ├── main.py              # FastAPI server & WebSocket streaming orchestrator
│   ├── simulator.py         # Induction furnace physics & telemetry simulator
│   ├── sec_engine.py        # Specific Energy Consumption calculation engine
│   ├── tou_optimizer.py     # MSEDCL Time-of-Use tariff scheduler & recommender
│   ├── cbam_ledger.py       # EU CBAM export compliance & carbon penalty ledger
│   └── ml_engine.py         # Scikit-learn predictive energy & duration regressors
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Furnace3D.jsx         # Three.js 3D induction furnace digital twin
│   │   │   ├── SECGauge.jsx          # SEC benchmark gauge vs BEE 625 kWh/t
│   │   │   ├── HoldingGuardAlert.jsx # Molten holding loss warning & ticker
│   │   │   ├── ToUScheduler.jsx      # 24h ToU tariff scheduler & smart shift
│   │   │   ├── CBAMLedgerCard.jsx    # CBAM carbon intensity & export protection
│   │   │   └── ControlPanel.jsx      # Operator controls & simulation speed
│   │   ├── App.jsx                   # Main operator dashboard container
│   │   └── index.css                 # Dark industrial theme & animations
│   ├── dist/                         # Compiled production build served by FastAPI
│   └── vite.config.js                # Vite configuration with proxy to backend
├── data/
│   ├── Steel_industry_data.csv       # UCI Machine Learning Steel Industry dataset
│   └── Energy_dataset.csv            # Industrial telemetry & power factor dataset
├── docs/
│   └── kolhapur_foundry_research.pdf # Research essay on Kolhapur MSME cluster
├── run.bat                           # Single-click Windows launcher
└── README.md
```
