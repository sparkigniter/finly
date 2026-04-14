import { 
  LayoutDashboard, Globe, User, RefreshCw, LogOut, 
  TrendingUp, AlertTriangle, Zap, CheckCircle2, Activity 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

import { StatsHero } from './StatsHero';
import { StockCard } from './StockCard';
import { StockFilters } from './StockFilters';
import { ConnectTab } from './ConnectTab';
import logo from '../assets/logo.png';

/* ── New Component: Portfolio Insights ── */
/* ── Updated Component: Portfolio Insights ── */
const PortfolioInsights = ({ insights }) => {
    if (!insights) return null;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 animate-in slide-in-from-bottom-4 duration-700 items-start">
            {/* Health Score */}
            <div className="bg-slate-900 rounded-3xl p-6 text-white flex flex-col justify-between shadow-xl relative overflow-hidden h-full min-h-[180px]">
                <div className="relative z-10">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Portfolio Health</span>
                        <Activity className="text-emerald-400" size={20} />
                    </div>
                    <div className="text-5xl font-black mb-2">
                        {insights.portfolio_health_score}
                        <span className="text-xl text-slate-500 ml-1">/100</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-relaxed max-w-[200px]">
                        Overall status based on diversification and risk-adjusted returns.
                    </p>
                </div>
                <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 blur-3xl rounded-full" />
            </div>

            {/* Assessment & Strategy - ADDED items-start HERE */}
            <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200 p-6 shadow-sm grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
                <div>
                    <h4 className="flex items-center gap-2 text-[10px] font-black text-rose-600 uppercase mb-4 tracking-widest">
                        <AlertTriangle size={14} /> Risk Assessment
                    </h4>
                    <ul className="space-y-3">
                        {insights.risk_assessment?.map((item, i) => (
                            <li key={i} className="text-[11px] text-slate-600 flex items-start gap-2 leading-snug">
                                <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mt-1.5 shrink-0" />
                                {item.trim()}
                            </li>
                        ))}
                    </ul>
                </div>
                {/* Removed border-l to keep the design clean when items don't align perfectly in height */}
                <div className="border-t md:border-t-0 md:border-l border-slate-100 pt-6 md:pt-0 md:pl-8">
                    <h4 className="flex items-center gap-2 text-[10px] font-black text-blue-600 uppercase mb-4 tracking-widest">
                        <Zap size={14} /> Strategic Actions
                    </h4>
                    <ul className="space-y-3">
                        {insights.strategic_actions?.map((item, i) => (
                            <li key={i} className="text-[11px] text-slate-600 flex items-start gap-2 leading-snug">
                                <CheckCircle2 size={13} className="text-emerald-500 mt-0.5 shrink-0" />
                                {item.trim()}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};
export default PortfolioInsights;