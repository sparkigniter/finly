import React from 'react';

export const StatsHero = ({ summary }) => {
  if (!summary) return null;

  const isPositive = summary.total_returns >= 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Total Investment</p>
        <h2 className="text-3xl font-black text-slate-900 mt-1">
          ₹{summary.total_investment.toLocaleString('en-IN')}
        </h2>
      </div>

      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Net Returns</p>
        <div className="flex items-baseline gap-2 mt-1">
          <h2 className={`text-3xl font-black ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
            ₹{summary.total_returns.toLocaleString('en-IN')}
          </h2>
          <span className={`text-sm font-bold ${isPositive ? 'text-emerald-500' : 'text-rose-500'}`}>
            ({(summary.overall_performance_pct).toFixed(2)}%)
          </span>
        </div>
      </div>

      <div className="bg-slate-900 p-6 rounded-2xl shadow-lg text-white">
        <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Diversification</p>
        <h2 className="text-3xl font-black mt-1">{summary.diversification_score}/10</h2>
        <div className="w-full bg-slate-700 h-1.5 rounded-full mt-3 overflow-hidden">
          <div 
            className="bg-blue-400 h-full transition-all duration-500" 
            style={{ width: `${(summary.diversification_score || 0) * 10}%` }}
          />
        </div>
      </div>
    </div>
  );
};