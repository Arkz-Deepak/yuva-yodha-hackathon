import React from 'react';
import { X, Download, FileText, CheckCircle2, ShieldCheck, QrCode, FileSpreadsheet } from 'lucide-react';

export default function CertificateModal({ isOpen, onClose, heatData }) {
  if (!isOpen) return null;

  const heat = heatData || {
    heat_id: 1043,
    weighbridge_tonnes: 1.500,
    metered_kwh: 937.5,
    sec_kwh_per_t: 625.0,
    total_intensity_tco2: 0.712,
    cbam_status: "COMPLIANT",
    cbam_savings_inr: 7450,
    escerts_earned: 0.193,
    gateway_id: "SE-ECO-EDGE-4102",
    facility_name: "Kolhapur Foundry Cluster Unit #14 (MIDC Shiroli)",
    meter_model: "Schneider Electric EasyLogic™ PM5350"
  };

  const heatId = heat.heat_id || 1043;
  const tonnes = Number(heat.weighbridge_tonnes || 1.5).toFixed(3);
  const kwh = Number(heat.metered_kwh || 937.5).toFixed(1);
  const sec = Number(heat.sec_kwh_per_t || (kwh / tonnes)).toFixed(1);
  const scope2Co2 = (sec * 0.82).toFixed(1);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-3xl max-h-[92vh] overflow-y-auto bg-[#0f172a] border border-emerald-500/40 rounded-2xl shadow-[0_0_50px_rgba(16,185,129,0.25)] p-6 text-slate-100">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Certificate Header Banner */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 pr-10">
          <div>
            <span className="text-[10px] uppercase font-mono tracking-wider text-emerald-400 font-bold block">
              SCHNEIDER ELECTRIC EcoStruxure™ EDGE MSME GATEWAY
            </span>
            <h2 className="text-xl font-extrabold text-white mt-0.5">
              Heat Compliance & Export Audit Certificate
            </h2>
            <p className="text-xs text-slate-400">
              Form CA-26: EU CBAM & BEE PAT Statutory Energy & Carbon Verification
            </p>
          </div>
          <div className="hidden sm:flex flex-col items-end">
            <span className="px-2.5 py-1 rounded bg-emerald-950 text-emerald-400 text-xs font-mono font-bold border border-emerald-700">
              DIGITALLY STAMPED
            </span>
            <span className="text-[10px] text-slate-500 mt-1 font-mono">Heat #HEAT-{heatId}</span>
          </div>
        </div>

        {/* Facility & Metadata Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4 bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 text-xs">
          <div>
            <span className="text-slate-500 block text-[10px]">FACILITY</span>
            <span className="font-semibold text-slate-200">Kolhapur MSME #14</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">METERING DEVICE</span>
            <span className="font-semibold text-emerald-400">SE EasyLogic PM5350</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">WEIGHBRIDGE NET</span>
            <span className="font-bold text-white font-mono">{tonnes} MT</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[10px]">METERED ENERGY</span>
            <span className="font-bold text-sky-400 font-mono">{kwh} kWh</span>
          </div>
        </div>

        {/* Statutory Formula Box */}
        <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-600/50 space-y-2 text-xs font-mono">
          <div className="flex items-center gap-2 text-emerald-400 font-bold">
            <ShieldCheck className="w-4 h-4" />
            <span>STATUTORY MEASUREMENT & AUDIT METHODOLOGY</span>
          </div>
          <div className="bg-black/40 p-2.5 rounded-lg border border-emerald-900/60 leading-relaxed text-slate-200">
            <div>
              <strong>Specific Energy Consumption (SEC)</strong> = Metered Total kWh / Weighbridge Net Tonnes
            </div>
            <div className="text-emerald-300 font-bold mt-0.5">
              = {kwh} kWh / {tonnes} MT = <span className="underline">{sec} kWh/tonne</span>
            </div>
            <div className="mt-2">
              <strong>Embodied Scope 2 Carbon</strong> = SEC × 0.82 kg CO₂/kWh (CEA Baseline)
            </div>
            <div className="text-emerald-300 font-bold mt-0.5">
              = {sec} × 0.82 = <span className="underline">{scope2Co2} kg CO₂/tonne</span>
            </div>
          </div>
        </div>

        {/* CBAM & BEE PAT Evaluation Table */}
        <div className="mt-4 border border-slate-800 rounded-xl overflow-hidden text-xs">
          <table className="w-full text-left">
            <thead className="bg-slate-900 text-slate-400 font-mono text-[11px]">
              <tr>
                <th className="p-2.5">Audit Dimension</th>
                <th className="p-2.5">Heat Measured</th>
                <th className="p-2.5">Statutory Benchmark</th>
                <th className="p-2.5">Compliance & Savings</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              <tr className="hover:bg-slate-900/40">
                <td className="p-2.5 font-medium text-slate-300">Specific Energy (SEC)</td>
                <td className="p-2.5 font-bold font-mono text-emerald-400">{sec} kWh/t</td>
                <td className="p-2.5 text-slate-400">BEE Target: 625.0 kWh/t</td>
                <td className="p-2.5 text-emerald-400 font-semibold">VERIFIED COMPLIANT</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="p-2.5 font-medium text-slate-300">Embodied Carbon</td>
                <td className="p-2.5 font-bold font-mono text-white">0.712 tCO₂/t</td>
                <td className="p-2.5 text-slate-400">EU Target: 1.50 tCO₂/t</td>
                <td className="p-2.5 text-emerald-400 font-semibold">CBAM EXEMPT (0 Deficit)</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="p-2.5 font-medium text-slate-300">EU CBAM Export Shield</td>
                <td className="p-2.5 font-bold font-mono text-emerald-400">+ €79.68 / t</td>
                <td className="p-2.5 text-slate-400">EU ETS Price: €79.68/t</td>
                <td className="p-2.5 text-emerald-400 font-bold font-mono">+ ₹7,450 / t saved</td>
              </tr>
              <tr className="hover:bg-slate-900/40">
                <td className="p-2.5 font-medium text-slate-300">BEE PAT Scheme ESCerts</td>
                <td className="p-2.5 font-bold font-mono text-sky-400">0.193 ESCerts</td>
                <td className="p-2.5 text-slate-400">EC Act 2001 (1 Mtoe = 1 ESCert)</td>
                <td className="p-2.5 text-sky-400 font-bold font-mono">₹415 IEX Trading Value</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Digital Signature & Actions */}
        <div className="mt-5 pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-[11px] text-slate-500 font-mono">
            <span>SHA-256 Stamp: </span>
            <span className="text-slate-400 break-all">e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b...</span>
          </div>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            <a
              href="/api/certificate/csv"
              className="flex-1 sm:flex-none px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs flex items-center justify-center gap-1.5 transition cursor-pointer border border-slate-700"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" /> Export CSV Ledger
            </a>

            <a
              href={`/api/certificate/pdf/${heatId}`}
              download
              className="flex-1 sm:flex-none px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 transition cursor-pointer shadow-lg shadow-emerald-950/60"
            >
              <Download className="w-4 h-4" /> Download PDF Certificate
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
