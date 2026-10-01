import React from 'react';
import { Globe, Leaf, FileCheck, Euro } from 'lucide-react';

export default function CBAMLedgerCard({ cbamData }) {
  const cbam = cbamData || {
    carbon_intensity_tco2_per_t: 2.15,
    eu_target_benchmark_tco2: 1.50,
    india_average_benchmark_tco2: 2.50,
    cbam_duty_liability_eur_per_t: 51.79,
    cbam_duty_liability_inr_per_t: 4842,
    cbam_savings_vs_unoptimized_inr_per_t: 1240,
    export_readiness_status: "MODERATE",
    ets_carbon_price_eur: 79.68
  };

  const isCompliant = cbam.export_readiness_status === "EXCELLENT";

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <Globe className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-200">EU CBAM Carbon & Export Ledger</h3>
              <p className="text-xs text-slate-400">Carbon Border Adjustment Mechanism Audit</p>
            </div>
          </div>
          <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold font-mono border ${
            isCompliant 
              ? 'bg-emerald-950/80 border-emerald-500 text-emerald-400' 
              : 'bg-amber-950/80 border-amber-500 text-amber-300'
          }`}>
            {cbam.export_readiness_status}
          </span>
        </div>

        {/* Carbon Intensity Comparison */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
            <span className="text-[10px] uppercase font-mono text-slate-400">Melt Carbon Intensity</span>
            <div className="text-xl font-bold font-mono text-white mt-0.5">
              {cbam.carbon_intensity_tco2_per_t?.toFixed(2)} <span className="text-xs font-normal text-slate-400">tCO₂/t</span>
            </div>
            <span className="text-[11px] text-slate-500">Target: ≤ 1.50 (EU Avg)</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
            <span className="text-[10px] uppercase font-mono text-slate-400">Export Carbon Tariff Risk</span>
            <div className="text-xl font-bold font-mono text-amber-400 mt-0.5">
              ₹{cbam.cbam_duty_liability_inr_per_t?.toFixed(0)} <span className="text-xs font-normal text-slate-400">/ tonne</span>
            </div>
            <span className="text-[11px] text-slate-500">Unmitigated Tariff Penalty</span>
          </div>
        </div>
      </div>

      {/* Export Shield Insight */}
      <div className="mt-4 p-3 rounded-lg bg-emerald-950/30 border border-emerald-800/40">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5 text-emerald-300">
            <Leaf className="w-4 h-4 text-emerald-400" />
            <span>EcoCast Tariff Protection:</span>
          </div>
          <span className="font-mono font-bold text-emerald-400">
            + ₹{cbam.cbam_savings_vs_unoptimized_inr_per_t?.toFixed(0)} / t saved
          </span>
        </div>
        <p className="text-[11px] text-slate-400 mt-1">
          Eliminating holding time & optimizing SEC safeguards Kolhapur exports against ₹7,450/t cross-border carbon duties.
        </p>
      </div>
    </div>
  );
}
