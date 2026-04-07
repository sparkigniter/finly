import React from 'react';

export const StatsHero = ({ summary }) => {
    const stats = {
        invested: summary?.total_investment || 0,
        returns: summary?.total_returns || 0,
        perf: summary?.overall_performance_pct || 0,
        health: summary?.diversification_score || 0,
        risk: summary?.risk_profile || "Moderate"
    };

    const isPositive = stats.returns >= 0;
    const healthWidth = `${Math.min(Math.max(stats.health * 10, 8), 100)}%`;

    return (
        <div className="w-full px-2 mb-8 space-y-5">

            {/* ── Top Financial Cards ───────────────── */}
            <div className="grid grid-cols-2 gap-4">
                {/* Invested */}
                <div className="p-5 rounded-3xl bg-white/80 backdrop-blur-xl border border-slate-200 shadow-sm hover:shadow-md transition">
                    <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                        Capital Deployed
                    </p>
                    <p className="text-2xl font-bold text-slate-900 mt-1">
                        ₹{stats.invested.toLocaleString('en-IN')}
                    </p>
                </div>

                {/* Returns */}
                <div className="p-5 rounded-3xl bg-white/80 backdrop-blur-xl border border-slate-200 shadow-sm hover:shadow-md transition">
                    <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                        Net Earnings
                    </p>
                    <p className={`text-2xl font-bold mt-1 ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
                        {isPositive ? '+' : ''}₹{stats.returns.toLocaleString('en-IN')}
                    </p>
                </div>
            </div>

            {/* ── Main Portfolio Card ───────────────── */}
            <div className="relative p-6 rounded-[28px] bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white shadow-xl overflow-hidden">

                {/* Glow accents */}
                <div className="absolute -top-10 -right-10 w-40 h-40 bg-orange-500/20 blur-[80px]" />
                <div className="absolute bottom-0 left-0 w-32 h-32 bg-emerald-500/10 blur-[60px]" />

                {/* Header */}
                <div className="flex justify-between items-start mb-6">
                    <div>
                        <p className="text-xs text-slate-400 tracking-widest uppercase">
                            Portfolio Health
                        </p>

                        <div className="flex items-end gap-2 mt-2">
                            <h2 className="text-4xl font-extrabold">
                                {stats.health}
                                <span className="text-lg text-slate-500">/10</span>
                            </h2>

                            <span className="text-xs px-2 py-1 rounded-lg bg-white/10 border border-white/10 text-slate-300">
                                {stats.risk} Risk
                            </span>
                        </div>
                    </div>

                    {/* Growth */}
                    <div className="text-right">
                        <p className="text-xs text-slate-400 uppercase tracking-wider">
                            Growth
                        </p>
                        <p className={`text-2xl font-bold ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {isPositive ? '▲' : '▼'} {stats.perf}%
                        </p>
                    </div>
                </div>

                {/* Progress */}
                <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                        <span className="text-slate-400">
                            Diversification Strength
                        </span>
                        <span className="text-orange-400 font-semibold">
                            {stats.health >= 7 ? 'Excellent' : stats.health >= 4 ? 'Moderate' : 'Low'}
                        </span>
                    </div>

                    <div className="h-3 w-full bg-white/10 rounded-full overflow-hidden">
                        <div
                            className="h-full rounded-full bg-gradient-to-r from-orange-500 via-amber-400 to-yellow-300 transition-all duration-700 ease-out shadow-md"
                            style={{ width: healthWidth }}
                        />
                    </div>
                </div>

                {/* Insight */}
                <div className="mt-5 text-xs text-slate-400 leading-relaxed border-t border-white/10 pt-4">
                    <span className="italic">
                        Your portfolio is heavily exposed to{" "}
                        <span className="text-white font-medium">
                            {summary?.top_sector || 'Equities'}
                        </span>. Consider diversification to improve stability.
                    </span>
                </div>
            </div>
        </div>
    );
};

export default StatsHero;