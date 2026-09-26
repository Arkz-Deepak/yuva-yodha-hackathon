import React, { useState } from 'react';
import { X, Server, CheckCircle2, AlertCircle, RefreshCw, Cpu, Activity } from 'lucide-react';

export default function ModbusConfigModal({ isOpen, onClose, modbusStatus, onSaveConfig }) {
  if (!isOpen) return null;

  const [mode, setMode] = useState(modbusStatus?.mode || "SIMULATION");
  const [host, setHost] = useState(modbusStatus?.host || "192.168.1.100");
  const [port, setPort] = useState(modbusStatus?.port || 502);
  const [slaveId, setSlaveId] = useState(modbusStatus?.slave_id || 1);
  const [meterModel, setMeterModel] = useState(modbusStatus?.meter_model || "Schneider Electric EasyLogic™ PM5350");
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setSaveMessage(null);
    try {
      const res = await fetch('/api/modbus/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode,
          host,
          port: parseInt(port),
          slave_id: parseInt(slaveId),
          meter_model: meterModel
        })
      });
      const data = await res.json();
      setIsSaving(false);
      setSaveMessage({ type: 'success', text: `Configuration updated: Mode is ${mode}` });
      if (onSaveConfig) onSaveConfig(data);
    } catch (err) {
      setIsSaving(false);
      setSaveMessage({ type: 'error', text: 'Failed to update Modbus configuration.' });
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-lg bg-[#0f172a] border border-slate-700 rounded-2xl shadow-2xl p-6 text-slate-100">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400">
            <Server className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Industrial Hardware Gateway</h3>
            <p className="text-xs text-slate-400">Modbus-TCP / RTU Schneider Electric Meter Ingestion</p>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="mt-5 space-y-4 text-xs">
          {/* Operating Mode Selector */}
          <div>
            <label className="text-slate-300 font-semibold block mb-1.5">Data Ingestion Mode</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setMode("SIMULATION")}
                className={`p-3 rounded-xl border text-left cursor-pointer transition ${
                  mode === "SIMULATION"
                    ? 'bg-emerald-950/60 border-emerald-500 text-emerald-300 ring-1 ring-emerald-500'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className="font-bold flex items-center gap-1.5">
                  <Cpu className="w-4 h-4" /> Physics Digital Twin
                </div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Synthetic induction thermodynamics & historical replay
                </div>
              </button>

              <button
                type="button"
                onClick={() => setMode("LIVE_MODBUS")}
                className={`p-3 rounded-xl border text-left cursor-pointer transition ${
                  mode === "LIVE_MODBUS"
                    ? 'bg-sky-950/60 border-sky-500 text-sky-300 ring-1 ring-sky-500'
                    : 'bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className="font-bold flex items-center gap-1.5">
                  <Activity className="w-4 h-4" /> Live Modbus-TCP
                </div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Real-time registers from Schneider PM/ION meters
                </div>
              </button>
            </div>
          </div>

          {/* Meter Model Selection */}
          <div>
            <label className="text-slate-300 font-semibold block mb-1">Energy Meter Model</label>
            <select
              value={meterModel}
              onChange={(e) => setMeterModel(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-white font-mono text-xs focus:border-emerald-500 outline-none"
            >
              <option value="Schneider Electric EasyLogic™ PM5350">Schneider Electric EasyLogic™ PM5350 (Class 0.5S)</option>
              <option value="Schneider Electric PowerLogic™ ION9000">Schneider Electric PowerLogic™ ION9000 (Revenue Grade)</option>
              <option value="Schneider Electric EasyLogic™ PM1200 / EM6400NG">Schneider Electric EasyLogic™ PM1200 / EM6400NG</option>
            </select>
          </div>

          {/* Gateway IP & Port */}
          <div className="grid grid-cols-3 gap-3">
            <div className="col-span-2">
              <label className="text-slate-300 font-semibold block mb-1">Modbus Gateway Host / IP</label>
              <input
                type="text"
                value={host}
                onChange={(e) => setHost(e.target.value)}
                placeholder="192.168.1.100"
                className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-white font-mono text-xs focus:border-emerald-500 outline-none"
              />
            </div>

            <div>
              <label className="text-slate-300 font-semibold block mb-1">Port</label>
              <input
                type="number"
                value={port}
                onChange={(e) => setPort(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-white font-mono text-xs focus:border-emerald-500 outline-none"
              />
            </div>
          </div>

          {/* Slave Unit ID */}
          <div>
            <label className="text-slate-300 font-semibold block mb-1">Modbus Slave / Unit ID</label>
            <input
              type="number"
              value={slaveId}
              onChange={(e) => setSlaveId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-white font-mono text-xs focus:border-emerald-500 outline-none"
            />
          </div>

          {/* Status Message */}
          {saveMessage && (
            <div className={`p-2.5 rounded-lg text-xs font-semibold ${
              saveMessage.type === 'success' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' : 'bg-rose-950 text-rose-300 border border-rose-800'
            }`}>
              {saveMessage.text}
            </div>
          )}

          {/* Submit */}
          <div className="pt-2 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 font-semibold text-xs hover:bg-slate-700 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 transition cursor-pointer shadow-lg shadow-emerald-950/50"
            >
              {isSaving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
              Save & Apply Settings
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
