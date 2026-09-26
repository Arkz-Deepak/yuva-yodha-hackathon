import React, { useState, useEffect, useRef } from 'react';
import { 
  Zap, 
  Activity, 
  Thermometer, 
  Clock, 
  IndianRupee, 
  Leaf, 
  ShieldCheck, 
  Layers, 
  Radio, 
  Gauge, 
  Info,
  Building2,
  RefreshCw
} from 'lucide-react';

import Furnace3D from './components/Furnace3D';
import SECGauge from './components/SECGauge';
import HoldingGuardAlert from './components/HoldingGuardAlert';
import ToUScheduler from './components/ToUScheduler';
import CBAMLedgerCard from './components/CBAMLedgerCard';
import ControlPanel from './components/ControlPanel';

export default function App() {
  const [data, setData] = useState(null);
  const [touSchedule, setTouSchedule] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [speed, setSpeed] = useState(12);
  const wsRef = useRef(null);

  // Initial REST fetch for fallback & tariff schedule
  useEffect(() => {
    fetch('/api/status')
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => console.log('REST fetch fallback error:', err));

    fetch('/api/tou/schedule')
      .then(res => res.json())
      .then(json => setTouSchedule(json))
      .catch(err => console.log('Tariff fetch error:', err));
  }, []);

  // WebSocket real-time telemetry stream
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/ws/telemetry`;

    function connectWs() {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        console.log('[EcoCast WebSocket] Connected to real-time telemetry stream.');
      };

      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          setData(payload);
        } catch (e) {
          console.error('Error parsing WS message', e);
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
        // Reconnect after 2 seconds
        setTimeout(connectWs, 2000);
      };

      ws.onerror = (err) => {
        console.error('[EcoCast WebSocket] Error:', err);
        ws.close();
      };
    }

    connectWs();

    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  // Control action handler
  const handleAction = async (action) => {
    try {
      const res = await fetch('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action })
      });
      const result = await res.json();
      console.log('Action response:', result);
      // Refresh status immediately
      const statusRes = await fetch('/api/status');
      const statusJson = await statusRes.json();
      setData(statusJson);
    } catch (err) {
      console.error('Action failed:', err);
    }
  };

  const handleSpeedChange = async (newSpeed) => {
    setSpeed(newSpeed);
    try {
      await fetch('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'set_speed', speed: newSpeed })
      });
    } catch (e) {
      console.error(e);
    }
  };

  const telemetry = data?.telemetry || {
    batch_id: 1042,
    state: "IDLE",
    temperature_c: 32,
    target_temperature_c: 1520,
    active_power_kw: 0,
    reactive_power_kvar: 0,
    power_factor: 0.96,
    current_a: 0,
    voltage_v: 1200,
    coil_water_in_c: 28,
    coil_water_out_c: 32,
    lid_is_closed: true,
    radiation_loss_kw: 0,
    tilt_angle_deg: 0,
    cumulative_kwh: 0,
    sec_kwh_per_tonne: 0,
    holding_minutes: 0,
    holding_energy_kwh: 0,
    holding_cost_inr: 0,
    holding_burn_rate_inr_per_min: 0,
    batch_weight_tonnes: 1.5
  };

  const tariff = data?.tariff;
  const cbam = data?.cbam;
  const mlForecast = data?.ml_forecast;

  return (
    <div className="min-h-screen pb-12">
      {/* Top Industrial Header */}
      <header className="sticky top-0 z-50 bg-[#0a0e14]/90 backdrop-blur-md border-b border-slate-800 px-4 lg:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          {/* Logo & Brand */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#2da643] to-[#3dcd58] flex items-center justify-center shadow-[0_0_20px_rgba(61,205,88,0.4)]">
              <Zap className="w-6 h-6 text-black font-extrabold" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-extrabold tracking-tight text-white flex items-center gap-1.5">
                  EcoCast <span className="text-[#3dcd58]">AI</span>
                </h1>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#3dcd58]/15 text-[#3dcd58] border border-[#3dcd58]/30">
                  SCHNEIDER ELECTRIC YUVA YODHA 2026
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Decision-Support Digital Twin for MSME Induction Furnaces • Kolhapur Foundry Cluster Benchmark
              </p>
            </div>
          </div>

          {/* Right Header Status */}
          <div className="flex items-center gap-4 text-xs font-mono">
            {/* Live Telemetry Pill */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800">
              <span className={`w-2.5 h-2.5 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className={isConnected ? 'text-emerald-400 font-semibold' : 'text-rose-400'}>
                {isConnected ? 'MQTT / TELEMETRY LIVE' : 'CONNECTING GATEWAY...'}
              </span>
            </div>

            {/* Batch ID Tag */}
            <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
              <Layers className="w-3.5 h-3.5 text-slate-400" />
              <span>Batch #{telemetry.batch_id}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 lg:px-8 mt-5 space-y-5">
        {/* Holding Loss Alarm Banner (The core decision leak) */}
        <HoldingGuardAlert
          isHolding={telemetry.is_holding_alert}
          holdingMinutes={telemetry.holding_minutes}
          holdingKwh={telemetry.holding_energy_kwh}
          holdingCostInr={telemetry.holding_cost_inr}
          burnRateInrPerMin={telemetry.holding_burn_rate_inr_per_min}
          onResolveAction={handleAction}
        />

        {/* 2-Column Main Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          {/* Left Column: 3D Twin & Shopfloor Controls (7 Cols) */}
          <div className="lg:col-span-7 space-y-4">
            {/* 3D Induction Furnace Twin */}
            <Furnace3D
              temperature={telemetry.temperature_c}
              targetTemp={telemetry.target_temperature_c}
              state={telemetry.state}
              lidIsClosed={telemetry.lid_is_closed}
              tiltAngle={telemetry.tilt_angle_deg}
              powerKw={telemetry.active_power_kw}
              radiationLossKw={telemetry.radiation_loss_kw}
            />

            {/* Live Electrical & Physical Telemetry Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              <div className="glass-panel p-3">
                <span className="text-[10px] uppercase font-mono text-slate-400 flex items-center gap-1">
                  <Zap className="w-3 h-3 text-emerald-400" /> Active Power
                </span>
                <div className="text-xl font-bold font-mono text-white mt-1">
                  {telemetry.active_power_kw.toFixed(1)} <span className="text-xs text-slate-400 font-normal">kW</span>
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">Rated: 750 kW</div>
              </div>

              <div className="glass-panel p-3">
                <span className="text-[10px] uppercase font-mono text-slate-400 flex items-center gap-1">
                  <Thermometer className="w-3 h-3 text-amber-400" /> Pyrometer Temp
                </span>
                <div className="text-xl font-bold font-mono text-amber-400 mt-1">
                  {telemetry.temperature_c.toFixed(0)} <span className="text-xs text-slate-400 font-normal">°C</span>
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">Target: 1520°C</div>
              </div>

              <div className="glass-panel p-3">
                <span className="text-[10px] uppercase font-mono text-slate-400 flex items-center gap-1">
                  <Activity className="w-3 h-3 text-sky-400" /> Cumulative Energy
                </span>
                <div className="text-xl font-bold font-mono text-sky-400 mt-1">
                  {telemetry.cumulative_kwh.toFixed(1)} <span className="text-xs text-slate-400 font-normal">kWh</span>
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">Batch 1.5 MT</div>
              </div>

              <div className="glass-panel p-3">
                <span className="text-[10px] uppercase font-mono text-slate-400 flex items-center gap-1">
                  <Gauge className="w-3 h-3 text-purple-400" /> Power Factor
                </span>
                <div className="text-xl font-bold font-mono text-purple-400 mt-1">
                  {telemetry.power_factor.toFixed(3)}
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">Coil: {telemetry.coil_water_out_c.toFixed(1)}°C</div>
              </div>
            </div>

            {/* Shopfloor Control & Simulation Panel */}
            <ControlPanel
              state={telemetry.state}
              lidIsClosed={telemetry.lid_is_closed}
              onAction={handleAction}
              mlForecast={mlForecast}
              speed={speed}
              onSpeedChange={handleSpeedChange}
            />
          </div>

          {/* Right Column: Decision Intelligence & Analytics (5 Cols) */}
          <div className="lg:col-span-5 space-y-4 flex flex-col">
            {/* SEC Benchmark Gauge */}
            <SECGauge
              secValue={telemetry.sec_kwh_per_tonne}
              beeBenchmark={625.0}
              batchTonnes={telemetry.batch_weight_tonnes}
            />

            {/* Time of Use Tariff Optimizer */}
            <ToUScheduler
              tariffData={tariff}
              touSchedule={touSchedule}
            />

            {/* EU CBAM Carbon & Export Ledger */}
            <CBAMLedgerCard
              cbamData={cbam}
            />
          </div>
        </div>

        {/* Bottom Kolhapur Cluster & Schneider Impact Footer */}
        <section className="glass-panel p-5 mt-6 border-slate-800/80 bg-gradient-to-r from-slate-900/90 to-[#0e1624]">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400">
                <Building2 className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  Kolhapur MSME Foundry Cluster Impact Reference
                </h4>
                <p className="text-xs text-slate-400 max-w-2xl mt-0.5">
                  Based on BEE-UNIDO case studies across Kolhapur’s 300 foundries. Demonstrates that 9–45% energy cost reductions are achievable through production-aware decision intelligence without multi-crore Capex.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 text-xs font-mono">
              <div className="text-right">
                <span className="text-slate-400 block text-[10px]">POTENTIAL CLUSTER SAVINGS</span>
                <span className="text-emerald-400 font-bold text-sm">₹14.0 Crore / year</span>
              </div>
              <div className="h-8 w-px bg-slate-800" />
              <div className="text-right">
                <span className="text-slate-400 block text-[10px]">ANNUAL AVOIDED CO₂</span>
                <span className="text-sky-400 font-bold text-sm">15,500 Tonnes</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
