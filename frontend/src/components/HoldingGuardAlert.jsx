import React from 'react';
import { AlertTriangle, Clock, Flame, IndianRupee, ShieldAlert } from 'lucide-react';

export default function HoldingGuardAlert({ 
  isHolding = false, 
  holdingMinutes = 0, 
  holdingKwh = 0, 
  holdingCostInr = 0, 
  burnRateInrPerMin = 0,
  onResolveAction
}) {
  if (!isHolding) {
    return (
      <div className="glass-panel p-4 flex items-center justify-between border-emerald-900/40 bg-emerald-950/20">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            🛡️
          </div>
          <div>
            <h4 className="text-sm font-semibold text-emerald-300">Holding Guard: Active Protection</h4>
            <p className="text-xs text-slate-400">Zero idle molten hold detected. Melting and pouring synchronized.</p>
          </div>
        </div>
        <span className="text-xs font-mono font-medium px-2.5 py-1 rounded bg-emerald-900/40 text-emerald-300 border border-emerald-700/50">
          Optimal Flow
        </span>
      </div>
    );
  }

  return (
    <div className="glass-panel p-5 border-rose-600 animate-pulse-red bg-rose-950/40">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Left: Alarm Status */}
        <div className="flex items-start gap-3">
          <div className="p-2.5 rounded-xl bg-rose-500/20 text-rose-400 animate-bounce">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500 text-white uppercase tracking-wider">
                CRITICAL INEFFICIENCY
              </span>
              <h4 className="text-base font-bold text-white">Unproductive Molten Holding State</h4>
            </div>
            <p className="text-xs text-rose-200 mt-1 max-w-xl">
              Metal is at 1520°C target temperature but idle awaiting ladle/mold crane. Radiation and electrical standby are actively burning operational cash!
            </p>
          </div>
        </div>

        {/* Right: Metrics Ticker */}
        <div className="grid grid-cols-3 gap-3 bg-black/40 p-3 rounded-lg border border-rose-900/60 font-mono">
          <div className="text-center">
            <div className="text-[10px] uppercase text-rose-300 flex items-center justify-center gap-1">
              <Clock className="w-3 h-3" /> Hold Time
            </div>
            <div className="text-lg font-bold text-white mt-0.5">{holdingMinutes.toFixed(1)} m</div>
          </div>
          <div className="text-center border-x border-rose-900/50 px-2">
            <div className="text-[10px] uppercase text-rose-300 flex items-center justify-center gap-1">
              <Flame className="w-3 h-3" /> Waste kWh
            </div>
            <div className="text-lg font-bold text-amber-400 mt-0.5">{holdingKwh.toFixed(1)}</div>
          </div>
          <div className="text-center">
            <div className="text-[10px] uppercase text-rose-300 flex items-center justify-center gap-1">
              <IndianRupee className="w-3 h-3" /> Loss (₹)
            </div>
            <div className="text-lg font-bold text-rose-400 mt-0.5">₹{holdingCostInr.toFixed(0)}</div>
          </div>
        </div>
      </div>

      {/* Burn Rate & Decision Action */}
      <div className="mt-3 pt-3 border-t border-rose-900/60 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div className="flex items-center gap-2 text-rose-300 font-mono">
          <span>🔥 Ongoing Burn Rate:</span>
          <span className="font-bold text-white bg-rose-900/60 px-2 py-0.5 rounded">
            ₹{burnRateInrPerMin.toFixed(1)} / min
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-300 text-xs">Action:</span>
          <button
            onClick={() => onResolveAction && onResolveAction('tap')}
            className="px-3 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition cursor-pointer shadow-lg"
          >
            Pour to Ladle Now
          </button>
        </div>
      </div>
    </div>
  );
}
