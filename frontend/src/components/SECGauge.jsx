import React from 'react';
import { Zap, Award, TrendingDown } from 'lucide-react';

export default function SECGauge({ secValue = 0, beeBenchmark = 625, batchTonnes = 1.5 }) {
  // SEC ranges from 400 to 1000 kWh/t
  const minVal = 450;
  const maxVal = 950;
  const clampedVal = Math.max(minVal, Math.min(maxVal, secValue || minVal));
  const percentage = ((clampedVal - minVal) / (maxVal - minVal)) * 100;
  
  // Calculate potential savings vs unoptimized Kolhapur baseline (780 kWh/t)
  const baselineSec = 780;
  const deltaVsBaseline = baselineSec - (secValue > 0 ? secValue : baselineSec);
  const costSavingsInr = deltaVsBaseline > 0 ? deltaVsBaseline * batchTonnes * 8.50 : 0;

  // Status color
  let statusColor = '#3dcd58'; // Green
  let statusLabel = 'Optimal (BEE Class)';
  if (secValue > 720 && secValue <= 800) {
    statusColor = '#f59e0b'; // Amber
    statusLabel = 'Average MSME';
  } else if (secValue > 800) {
    statusColor = '#ef4444'; // Red
    statusLabel = 'High Inefficiency';
  }

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-200">Specific Energy Consumption</h3>
            <p className="text-xs text-slate-400">Core Benchmark Metric (SEC)</p>
          </div>
        </div>
        <span className="text-xs font-mono px-2 py-0.5 rounded border border-slate-700 text-slate-300">
          Target: {beeBenchmark} kWh/t
        </span>
      </div>

      {/* Main Metric Display */}
      <div className="my-4 text-center">
        <div className="flex items-baseline justify-center gap-1.5">
          <span className="text-4xl font-extrabold font-mono tracking-tight" style={{ color: statusColor }}>
            {secValue > 0 ? secValue.toFixed(1) : '---'}
          </span>
          <span className="text-sm font-medium text-slate-400">kWh / Tonne</span>
        </div>
        <span 
          className="inline-block mt-1 px-2.5 py-0.5 text-xs font-semibold rounded-full"
          style={{ backgroundColor: `${statusColor}20`, color: statusColor }}
        >
          {secValue > 0 ? statusLabel : 'Awaiting Melt Cycle'}
        </span>
      </div>

      {/* Progress Arc / Linear Bar */}
      <div className="space-y-2">
        <div className="relative w-full h-3 bg-slate-800 rounded-full overflow-hidden">
          {/* Target marker */}
          <div 
            className="absolute top-0 bottom-0 w-1 bg-white z-10 shadow-[0_0_8px_white]"
            style={{ left: `${((beeBenchmark - minVal) / (maxVal - minVal)) * 100}%` }}
            title={`BEE Star Standard: ${beeBenchmark} kWh/t`}
          />
          {/* Filled Bar */}
          <div 
            className="h-full rounded-full transition-all duration-500"
            style={{ 
              width: `${percentage}%`,
              backgroundColor: statusColor 
            }}
          />
        </div>

        {/* Labels below bar */}
        <div className="flex justify-between text-[11px] text-slate-400 font-mono">
          <span>500 (Best)</span>
          <span className="text-emerald-400 font-bold">⭐ 625 (BEE Target)</span>
          <span>780 (Kolhapur Avg)</span>
          <span>950</span>
        </div>
      </div>

      {/* Kolhapur Savings Insight */}
      <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
        <div className="flex items-center gap-1.5 text-slate-300">
          <TrendingDown className="w-4 h-4 text-emerald-400" />
          <span>Batch Cost Savings:</span>
        </div>
        <span className="font-mono font-bold text-emerald-400">
          {costSavingsInr > 0 ? `+ ₹${costSavingsInr.toFixed(0)} saved` : 'Standard Baseline'}
        </span>
      </div>
    </div>
  );
}
