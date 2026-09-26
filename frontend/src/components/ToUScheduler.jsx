import React from 'react';
import { Calendar, Clock, ArrowUpRight, TrendingUp } from 'lucide-react';

export default function ToUScheduler({ tariffData, touSchedule }) {
  const currentTariff = tariffData || {
    zone: "Normal Day",
    rate_inr_kwh: 8.50,
    status_color: "#3b82f6",
    description: "Standard operational tariff slab."
  };

  const optimization = touSchedule?.optimization || {
    recommendation: "Start immediately. Current tariff is favorable.",
    best_option: {
      offset_minutes: 0,
      potential_savings_inr: 0,
      start_time: "Now"
    }
  };

  const schedule24h = touSchedule?.schedule_24h || [];

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Time-of-Use (ToU) Tariff Optimizer</h3>
              <p className="text-xs text-slate-400">MSEDCL HT-Industrial Tariff Engine</p>
            </div>
          </div>
          <div 
            className="px-2.5 py-1 rounded-full text-xs font-semibold font-mono border"
            style={{ 
              borderColor: `${currentTariff.status_color}60`, 
              backgroundColor: `${currentTariff.status_color}20`,
              color: currentTariff.status_color 
            }}
          >
            ₹{currentTariff.rate_inr_kwh?.toFixed(2)} / kWh
          </div>
        </div>

        {/* 24-Hour Timeline Strip */}
        <div className="mt-4">
          <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1.5 font-mono">
            <span>24-Hour Tariff Schedule</span>
            <span className="text-emerald-400">Night Rebate (22-06h: -₹1.50)</span>
          </div>

          <div className="grid grid-cols-24 gap-0.5 h-6 rounded bg-slate-900 p-0.5 border border-slate-800">
            {schedule24h.length > 0 ? (
              schedule24h.map((slot) => {
                const isNight = slot.hour >= 22 || slot.hour < 6;
                const isPeak = slot.hour >= 18 && slot.hour < 22;
                const isNow = new Date().getHours() === slot.hour;

                return (
                  <div 
                    key={slot.hour}
                    className={`h-full rounded-sm relative group cursor-pointer transition ${
                      isPeak ? 'bg-rose-500/70' :
                      isNight ? 'bg-emerald-500/70' : 'bg-sky-500/50'
                    } ${isNow ? 'ring-2 ring-white scale-110 z-10' : ''}`}
                    title={`${slot.label}: ${slot.zone} (₹${slot.rate.toFixed(2)})`}
                  >
                    {isNow && (
                      <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-white rounded-full" />
                    )}
                  </div>
                );
              })
            ) : (
              <div className="col-span-24 text-center text-[10px] text-slate-500 self-center">
                Loading tariff grid...
              </div>
            )}
          </div>

          <div className="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
            <span>00:00 (Night)</span>
            <span>06:00 (Day)</span>
            <span>18:00 (Peak Surcharge)</span>
            <span>22:00</span>
          </div>
        </div>
      </div>

      {/* Decision-Support Recommendation Box */}
      <div className="mt-4 p-3 rounded-lg bg-slate-900/90 border border-slate-800">
        <div className="flex items-start gap-2.5">
          <div className="p-1 rounded bg-amber-500/20 text-amber-400 mt-0.5">
            <TrendingUp className="w-4 h-4" />
          </div>
          <div className="flex-1">
            <h5 className="text-xs font-semibold text-slate-200">Optimal Start Recommendation</h5>
            <p className="text-xs text-slate-300 mt-0.5 leading-relaxed">
              {optimization.recommendation}
            </p>
          </div>
        </div>

        {optimization.best_option?.potential_savings_inr > 0 && (
          <div className="mt-2 pt-2 border-t border-slate-800 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Projected Batch Saving:</span>
            <span className="text-emerald-400 font-bold">
              + ₹{optimization.best_option.potential_savings_inr.toFixed(0)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
