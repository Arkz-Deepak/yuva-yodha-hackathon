import React, { useState } from 'react';
import { Play, RotateCcw, AlertOctagon, Flame, FastForward, Cpu, Sparkles, CheckCircle2 } from 'lucide-react';

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
  const isTapping = state === "TAPPING";
  const isIdle = state === "IDLE";

  const [clickedBtn, setClickedBtn] = useState(null);

  const handleBtnClick = (action) => {
    setClickedBtn(action);
    setTimeout(() => setClickedBtn(null), 350);
    if (onAction) onAction(action);
  };

  return (
    <div className="glass-panel p-5 space-y-4">
      {/* Title & Speed Multiplier */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <span>⚡ Interactive Shopfloor Controls</span>
          </h3>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1.5 bg-slate-900/90 px-2.5 py-1 rounded-lg border border-slate-800 text-xs font-mono">
          <FastForward className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-slate-400 mr-1 text-[11px]">Demo Speed:</span>
          {[1, 5, 12, 25].map((s) => (
            <button
              key={s}
              type="button"
              onClick={() => onSpeedChange(s)}
              className={`px-2 py-0.5 rounded text-[11px] font-bold cursor-pointer transition-all duration-150 active:scale-90 ${
                speed === s 
                  ? 'bg-emerald-500 text-black shadow-[0_0_10px_rgba(16,185,129,0.5)] scale-105' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Primary Action Buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
        {/* 1. Start / Restart Batch */}
        <button
          type="button"
          onClick={() => handleBtnClick('start_batch')}
          className={`relative px-3 py-3 rounded-xl font-bold text-xs flex flex-col items-center justify-center gap-1 transition-all duration-150 cursor-pointer shadow-lg active:scale-95 ${
            clickedBtn === 'start_batch' ? 'ring-2 ring-white scale-95' : ''
          } ${
            isMelting
              ? 'bg-emerald-950/80 border border-emerald-500/80 text-emerald-300 shadow-emerald-950/50'
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-950/50 hover:shadow-emerald-600/30'
          }`}
        >
          <div className="flex items-center gap-1.5">
            <Play className="w-4 h-4 fill-current" />
            <span>{isMelting ? 'Ramping Heat' : isIdle ? 'Start Batch' : 'New Heat'}</span>
          </div>
          <span className="text-[10px] font-normal opacity-80">1.5 MT Ingot</span>
        </button>

        {/* 2. Toggle Lid Button */}
        <button
          type="button"
          onClick={() => handleBtnClick('toggle_lid')}
          className={`relative px-3 py-3 rounded-xl font-bold text-xs flex flex-col items-center justify-center gap-1 border transition-all duration-150 cursor-pointer shadow-lg active:scale-95 ${
            clickedBtn === 'toggle_lid' ? 'ring-2 ring-white scale-95' : ''
          } ${
            lidIsClosed
              ? 'bg-slate-800 border-slate-700 text-slate-200 hover:bg-slate-700 hover:border-slate-600'
              : 'bg-rose-950/90 border-rose-500 text-rose-200 hover:bg-rose-900 shadow-rose-950/60 animate-pulse'
          }`}
        >
          <div className="flex items-center gap-1.5">
            <span>{lidIsClosed ? '🛡️ Open Lid' : '⚠️ Close Lid'}</span>
          </div>
          <span className="text-[10px] font-normal opacity-80">
            {lidIsClosed ? 'Trap 32.7 kWh' : 'Radiation Leak!'}
          </span>
        </button>

        {/* 3. Simulate Ladle Delay / Holding */}
        <button
          type="button"
          onClick={() => handleBtnClick('trigger_delay')}
          className={`relative px-3 py-3 rounded-xl font-bold text-xs flex flex-col items-center justify-center gap-1 border transition-all duration-150 cursor-pointer shadow-lg active:scale-95 ${
            clickedBtn === 'trigger_delay' ? 'ring-2 ring-white scale-95' : ''
          } ${
            isHolding
              ? 'bg-amber-950 border-amber-500 text-amber-300 ring-2 ring-amber-500/50 animate-pulse'
              : 'bg-amber-950/60 border-amber-600/70 text-amber-300 hover:bg-amber-900/80 hover:border-amber-500'
          }`}
        >
          <div className="flex items-center gap-1.5">
            <AlertOctagon className="w-4 h-4 text-amber-400" />
            <span>Simulate Hold</span>
          </div>
          <span className="text-[10px] font-normal opacity-80">Trigger Delay</span>
        </button>

        {/* 4. Tap Metal */}
        <button
          type="button"
          onClick={() => handleBtnClick('tap')}
          className={`relative px-3 py-3 rounded-xl font-bold text-xs flex flex-col items-center justify-center gap-1 border border-orange-500/50 transition-all duration-150 cursor-pointer shadow-lg active:scale-95 ${
            clickedBtn === 'tap' ? 'ring-2 ring-white scale-95' : ''
          } ${
            isTapping
              ? 'bg-orange-700 text-white animate-pulse'
              : 'bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-500 hover:to-amber-500 text-white shadow-orange-950/60'
          }`}
        >
          <div className="flex items-center gap-1.5">
            <Flame className="w-4 h-4 fill-current" />
            <span>Tap Metal</span>
          </div>
          <span className="text-[10px] font-normal opacity-80">Pour to Ladle</span>
        </button>

        {/* 5. Reset to Idle */}
        <button
          type="button"
          onClick={() => handleBtnClick('reset')}
          className={`relative col-span-2 sm:col-span-1 px-3 py-3 rounded-xl font-bold text-xs flex flex-col items-center justify-center gap-1 border border-slate-700 bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white transition-all duration-150 cursor-pointer shadow-lg active:scale-95 ${
            clickedBtn === 'reset' ? 'ring-2 ring-white scale-95' : ''
          }`}
        >
          <div className="flex items-center gap-1.5">
            <RotateCcw className="w-4 h-4 text-slate-400" />
            <span>Reset Idle</span>
          </div>
          <span className="text-[10px] font-normal opacity-70">Cool Furnace</span>
        </button>
      </div>

      {/* ML Decision Support Banner */}
      {mlForecast && (
        <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
              <Cpu className="w-4 h-4" />
            </div>
            <div>
              <span className="font-bold text-white">AI Thermodynamic Trajectory</span>
              <div className="flex items-center gap-2 text-slate-400 text-[11px] mt-0.5">
                <span>Est. Duration: <strong className="text-emerald-400 font-mono">{mlForecast.predicted_duration_mins} min</strong></span>
                <span>•</span>
                <span>Predicted SEC: <strong className="text-emerald-400 font-mono">{mlForecast.predicted_sec_kwh_per_t} kWh/t</strong></span>
                <span>•</span>
                <span className="text-emerald-300 font-medium">BEE Class: {mlForecast.efficiency_rating}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto">
            <span className="text-slate-400 text-[11px]">Recommended Setpoint:</span>
            <span className="px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 font-mono font-bold border border-emerald-800 shadow-sm">
              720 kW Optimal Ramp
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
