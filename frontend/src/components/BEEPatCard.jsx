import React from 'react';
import { Award, TrendingUp, IndianRupee, CheckCircle2 } from 'lucide-react';

export default function BEEPatCard({ patData }) {
  const pat = patData || {
    actual_sec_kwh_per_t: 625.0,
    bee_pat_baseline_sec: 850.0,
    bee_pat_target_sec: 625.0,
    escerts_earned_per_batch: 0.193,
    escert_value_inr_per_batch: 415.0,
    projected_annual_escerts: 322.0,
    projected_annual_revenue_inr: 692300,
    iex_escert_market_price_inr: 2150.0,
    compliance_status: "PAT COMPLIANT"
  };

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
              <Award className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-200">BEE PAT Scheme Compliance</h3>
              <p className="text-xs text-slate-400">Perform, Achieve and Trade (Energy Conservation Act)</p>
            </div>
          </div>
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold font-mono bg-sky-950 border border-sky-600 text-sky-400">
            {pat.compliance_status}
          </span>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
            <span className="text-[10px] uppercase font-mono text-slate-400">ESCerts Earned / Heat</span>
            <div className="text-xl font-bold font-mono text-white mt-0.5">
              {pat.escerts_earned_per_batch?.toFixed(3)} <span className="text-xs text-slate-400 font-normal">ESCerts</span>
            </div>
            <span className="text-[11px] text-slate-500">1 ESCert = 1 Mtoe Saved</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
            <span className="text-[10px] uppercase font-mono text-slate-400">IEX Market Value</span>
            <div className="text-xl font-bold font-mono text-sky-400 mt-0.5">
              ₹{pat.escert_value_inr_per_batch?.toFixed(0)} <span className="text-xs text-slate-400 font-normal">/ heat</span>
            </div>
            <span className="text-[11px] text-slate-500">IEX Price: ₹{pat.iex_escert_market_price_inr}</span>
          </div>
        </div>
      </div>

      {/* Annual Revenue Projection */}
      <div className="mt-4 p-3 rounded-lg bg-sky-950/30 border border-sky-800/40">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5 text-sky-300">
            <TrendingUp className="w-4 h-4 text-sky-400" />
            <span>Annual Trading Revenue:</span>
          </div>
          <span className="font-mono font-bold text-sky-400">
            + ₹{(pat.projected_annual_revenue_inr / 100000).toFixed(2)} Lakhs / year
          </span>
        </div>
        <p className="text-[11px] text-slate-400 mt-1">
          Trading surplus ESCerts on the Indian Energy Exchange turns energy efficiency into a direct balance-sheet asset.
        </p>
      </div>
    </div>
  );
}
