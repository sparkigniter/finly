import React from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  ShieldCheck, 
  PieChart, 
  Target,
  Layers,
  ChevronRight
} from 'lucide-react';

export const StatsHero = ({ summary, otherdata }) => {
    const stats = {
        invested: summary?.total_investment || 0,
        currentValue: summary?.total_current_value || 0,
        pnl: summary?.total_pnl || 0,
        roi: summary?.overall_roi_pct || 0,
        winRate: summary?.win_rate || 0,
        holdings: summary?.holdings_count || 0,
        gainers: summary?.gainers_count || 0,
        diversification: otherdata?.diversification_score || 0,
        risk: otherdata?.risk_profile || "Balanced"
    };

    const isPositive = stats.pnl >= 0;

    return (
        <div className="w-full px-4 sm:px-6 lg:px-8 py-6 max-w-7xl mx-auto space-y-6">
            
            {/* ── MAIN + SIDE GRID ───────────────── */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* ── MAIN CARD ───────────────── */}
                <div className="lg:col-span-2 relative p-6 sm:p-8 rounded-[2rem] bg-slate-900 text-white shadow-xl overflow-hidden border border-white/5">
                    
                    <div className="absolute top-0 right-0 w-40 h-40 bg-emerald-500/20 blur-[80px] rounded-full" />

                    <div className="relative z-10">
                        <div className="flex justify-between items-center mb-6">
                            <span className="text-xs sm:text-sm font-bold tracking-widest text-slate-400 uppercase">
                                Portfolio Value
                            </span>

                            <div className="px-3 py-1 rounded-full bg-white/10 border border-white/10 flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                                <span className="text-xs font-bold uppercase text-slate-200">
                                    {stats.risk}
                                </span>
                            </div>
                        </div>

                        <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight" style={{color:"white", textAlign:"start"}}>
                            ₹{stats.currentValue.toLocaleString('en-IN')}
                        </h2>

                        <div className={`flex items-center gap-2 mt-2 text-sm sm:text-base font-bold ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {isPositive ? <TrendingUp size={16}/> : <TrendingDown size={16}/>}
                            <span>
                                {isPositive ? '+' : ''}₹{Math.abs(stats.pnl).toLocaleString('en-IN')}
                            </span>
                            <span className="opacity-60 text-xs sm:text-sm">
                                ({stats.roi}%)
                            </span>
                        </div>

                        <div className="flex items-center justify-between pt-6 mt-6 border-t border-white/10">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center">
                                    <ShieldCheck size={16} className="text-slate-400" />
                                </div>
                                <div>
                                    <p className="text-xs font-bold text-slate-500 uppercase">Invested</p>
                                    <p className="text-sm sm:text-base font-bold text-white">
                                        ₹{stats.invested.toLocaleString('en-IN')}
                                    </p>
                                </div>
                            </div>
                            <ChevronRight size={18} className="text-slate-600" />
                        </div>
                    </div>
                </div>

                {/* ── SIDE STATS ───────────────── */}
                <div className="grid grid-cols-2 lg:grid-cols-1 gap-4">
                    
                    {/* Diversification */}
                    <div className="bg-white p-4 rounded-3xl border border-slate-100 shadow-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <div className="p-2 bg-indigo-50 rounded-lg">
                                <Layers size={16} className="text-indigo-600" />
                            </div>
                            <span className="text-xs font-black text-slate-400 uppercase">
                                Diversification
                            </span>
                        </div>

                        <div className="flex items-baseline gap-1">
                            <span className="text-xl font-black text-slate-900">
                                {stats.diversification}
                            </span>
                            <span className="text-xs text-slate-400">%</span>
                        </div>

                        <div className="mt-2 h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                            <div 
                                className="h-full bg-indigo-500 rounded-full" 
                                style={{ width: `${stats.diversification}%` }}
                            />
                        </div>
                    </div>

                    {/* Win Rate */}
                    <div className="bg-white p-4 rounded-3xl border border-slate-100 shadow-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <div className="p-2 bg-amber-50 rounded-lg">
                                <Target size={16} className="text-amber-600" />
                            </div>
                            <span className="text-xs font-black text-slate-400 uppercase">
                                Gain %
                            </span>
                        </div>

                        <div className="flex items-baseline gap-1">
                            <span className="text-xl font-black text-slate-900">
                                {stats.winRate}
                            </span>
                            <span className="text-xs text-slate-400">%</span>
                        </div>

                        <div className="mt-2 h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                            <div 
                                className="h-full bg-amber-500 rounded-full" 
                                style={{ width: `${stats.winRate}%` }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* ── INSIGHT BAR ───────────────── */}
            <div className="bg-slate-50 rounded-2xl p-4 flex items-center gap-4 border border-slate-100">
                <div className="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-200">
                    <PieChart size={20} className="text-white" />
                </div>

                <div className="flex-1">
                    <p className="text-sm text-slate-600">
                        <span className="font-bold text-slate-900">
                            {stats.holdings} Assets Managed
                        </span>. 
                        Your top performers are driving{" "}
                        <span className="text-emerald-600 font-bold">
                            {stats.roi}% growth
                        </span>.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default StatsHero;