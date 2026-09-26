import React from 'react';
import { Play, Pause, RotateCcw, AlertOctagon, Flame, FastForward, Cpu } from 'lucide-react';

export default function ControlPanel({ 
  state = "IDLE", 
  lidIsClosed = true, 
  onAction,
  mlForecast,
  speed = 12,
  onSpeedChange
}) {
  const isMelting = state === "MELTING" || state === "CHARGING" || state === "REFINING" || state === "SUPERHEATING";
  const isHolding = state === "HOLDING";

  return (
    <div className="glass-panel p-5 space-y-4">
      {/* Title & Speed Multiplier */}
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <span>⚡ Shopfloor Control & Simulation</span>
        </h3>

        {/* Speed Selector */}
        <div className="flex items-center gap-1 bg-slate-900 px-2 py-1 rounded-lg border border-slate-800 text-xs font-mono">
          <FastForward className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400 mr-1">Speed:</span>
          {[1, 5, 12, 25].map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-1.5 py-0.5 rounded text-[11px] font-bold cursor-pointer transition ${
                speed === s 
                  ? 'bg-emerald-500 text-black' 
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Primary Action Buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
        {/* Start Batch Button */}
        <button
          onClick={() => onAction('start_batch')}
          disabled={isMelting}
          className={`px-3 py-2.5 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 transition cursor-pointer shadow-lg ${
            isMelting
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-950/50'
          }`}
        >
          <Play className="w-4 h-4" /> Start Melt Batch
        </button>

        {/* Toggle Lid Button */}
        <button
          onClick={() => onAction('toggle_lid')}
          className={`px-3 py-2.5 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 border transition cursor-pointer ${
            lidIsClosed
              ? 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
              : 'bg-rose-950/80 border-rose-600 text-rose-300 hover:bg-rose-900 animate-pulse'
          }`}
        >
          <span>{lidIsClosed ? '🛡️ Open Lid' : '⚠️ Close Lid'}</span>
        </button>

        {/* Simulate Delay / Holding */}
        <button
          onClick={() => onAction('trigger_delay')}
          disabled={isHolding || state === "IDLE"}
          className={`px-3 py-2.5 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 border transition cursor-pointer ${
            isHolding || state === "IDLE"
              ? 'bg-slate-800/50 border-slate-800 text-slate-600 cursor-not-allowed'
              : 'bg-amber-950/60 border-amber-600/70 text-amber-300 hover:bg-amber-900'
          }`}
        >
          <AlertOctagon className="w-4 h-4 text-amber-400" /> Simulate Ladle Delay
        </button>

        {/* Tap Metal */}
        <button
          onClick={() => onAction('tap')}
          disabled={state === "IDLE" || state === "TAPPING"}
          className={`px-3 py-2.5 rounded-lg font-semibold text-xs flex items-center justify-center gap-1.5 transition cursor-pointer ${
            state === "IDLE" || state === "TAPPING"
              ? 'bg-slate-800/50 text-slate-600 cursor-not-allowed'
              : 'bg-orange-600 hover:bg-orange-500 text-white shadow-lg'
          }`}
        >
          <Flame className="w-4 h-4" /> Tap Metal
        </button>
      </div>

      {/* ML Decision Support Banner */}
      {mlForecast && (
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <Cpu className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold text-white">AI Melt Trajectory:</span>
            <span className="text-slate-400">
              Est. Duration: <strong className="text-emerald-400 font-mono">{mlForecast.predicted_duration_mins} min</strong>
            </span>
            <span>•</span>
            <span className="text-slate-400">
              Predicted SEC: <strong className="text-emerald-400 font-mono">{mlForecast.predicted_sec_kwh_per_t} kWh/t</strong>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400 text-[11px]">Recommended Power Setpoint:</span>
            <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono font-bold border border-emerald-800">
              720 kW Ramp
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
