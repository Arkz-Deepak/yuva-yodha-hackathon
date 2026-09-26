import React from 'react';
import { History, FileText, Download, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';

export default function HeatHistoryTable({ heats = [], onSelectHeat }) {
  return (
    <div className="glass-panel p-5 space-y-4">
      {/* Table Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-slate-200">Verified Heat Audit Ledger</h3>
            <p className="text-xs text-slate-400">Statutory Form CA-26 Historical Heat Records</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <a
            href="/api/certificate/csv"
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs flex items-center gap-1.5 transition border border-slate-700"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" /> Export CSV
          </a>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/90 text-slate-400 font-mono text-[11px] border-b border-slate-800">
            <tr>
              <th className="p-3">Heat ID</th>
              <th className="p-3">Timestamp</th>
              <th className="p-3">Net Tonnes</th>
              <th className="p-3">Energy (kWh)</th>
              <th className="p-3">SEC (kWh/t)</th>
              <th className="p-3">Hold Time</th>
              <th className="p-3">CBAM Status</th>
              <th className="p-3">ESCerts</th>
              <th className="p-3 text-right">Audit Certificate</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80 font-mono">
            {heats.length > 0 ? (
              heats.map((heat) => {
                const sec = heat.sec_kwh_per_t || (heat.metered_kwh / heat.weighbridge_tonnes);
                const isOptimal = sec <= 630;

                return (
                  <tr key={heat.heat_id} className="hover:bg-slate-800/40 transition">
                    <td className="p-3 font-bold text-white flex items-center gap-1.5">
                      <Layers className="w-3.5 h-3.5 text-emerald-400" />
                      HEAT-{heat.heat_id}
                    </td>
                    <td className="p-3 text-slate-400">{heat.timestamp}</td>
                    <td className="p-3 font-semibold text-slate-200">{Number(heat.weighbridge_tonnes).toFixed(3)} MT</td>
                    <td className="p-3 text-sky-400">{Number(heat.metered_kwh).toFixed(1)}</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded font-bold ${
                        isOptimal ? 'bg-emerald-950 text-emerald-400' : 'bg-amber-950 text-amber-400'
                      }`}>
                        {Number(sec).toFixed(1)}
                      </span>
                    </td>
                    <td className="p-3 text-slate-400">
                      {heat.holding_minutes > 0 ? (
                        <span className="text-amber-400">{Number(heat.holding_minutes).toFixed(1)} m</span>
                      ) : (
                        <span className="text-emerald-400">0.0 m</span>
                      )}
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-950/80 text-emerald-400 border border-emerald-800">
                        {heat.cbam_status || 'COMPLIANT'}
                      </span>
                    </td>
                    <td className="p-3 text-sky-400 font-bold">
                      {Number(heat.escerts_earned || 0).toFixed(3)}
                    </td>
                    <td className="p-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => onSelectHeat && onSelectHeat(heat)}
                          className="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-sans flex items-center gap-1 transition cursor-pointer"
                        >
                          <FileText className="w-3 h-3 text-emerald-400" /> View
                        </button>
                        <a
                          href={`/api/certificate/pdf/${heat.heat_id}`}
                          download
                          className="px-2 py-1 rounded bg-emerald-900/50 hover:bg-emerald-800 text-emerald-300 text-[11px] font-sans flex items-center gap-1 transition cursor-pointer border border-emerald-700/50"
                        >
                          <Download className="w-3 h-3" /> PDF
                        </a>
                      </div>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={9} className="p-4 text-center text-slate-500 font-sans">
                  No previous heats found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
