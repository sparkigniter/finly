import React, { useState } from 'react';
import { 
  ChevronDown, ChevronUp, Activity, TrendingUp, Wallet,
  Target, AlertTriangle, Lightbulb, Zap
} from 'lucide-react';

export const StockCard = ({ stock }) => {
    const [expanded, setExpanded] = useState(false);

    if (!stock) return <div className="w-full h-32 bg-slate-50 animate-pulse rounded-2xl mb-4" />;

    const symbol = stock.tradingsymbol || "Unknown";
    const sector = (stock.sector === "null" || !stock.sector) ? "Diversified" : stock.sector;
    const pnl = stock.pnl ?? 0;
    const roi = stock.roi ?? 0;
    const isPositive = pnl >= 0;
    const recommendation = stock.recommendation || "Neutral";
    
    // New JSON Insight Mapping
    const insight = stock.insight || {};
    const risks = insight.risks || [];
    const opportunities = insight.opportunities || [];
    const aiAction = insight.action || "Continue monitoring";

    return (
        <div className={`bg-white rounded-3xl border transition-all duration-300 mb-4 overflow-hidden ${expanded ? 'shadow-xl border-slate-300' : 'shadow-sm border-slate-100 hover:border-slate-300'}`}>
            
            {/* MAIN HEADER */}
            <div className="p-5 md:p-6 cursor-pointer" onClick={() => setExpanded(!expanded)}>
                <div className="flex justify-between items-start mb-6">
                    <div className="flex items-center gap-4">
                        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-black text-white text-xs shadow-inner transition-colors ${isPositive ? 'bg-slate-900' : 'bg-rose-900'}`}>
                            {symbol.substring(0, 2).toUpperCase()}
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <h3 className="font-black text-slate-900 tracking-tight text-base">{symbol}</h3>
                                <span className="text-[8px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded font-black uppercase tracking-widest">
                                    {stock.market_cap}
                                </span>
                            </div>
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block mt-0.5">
                                {sector}
                            </span>
                        </div>
                    </div>
                    
                    <div className="flex flex-col items-end">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter border shadow-sm ${
                            recommendation === 'BUY' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 
                            recommendation === 'SELL' ? 'bg-rose-50 text-rose-600 border-rose-100' : 
                            'bg-amber-50 text-amber-600 border-amber-100'
                        }`}>
                            <Zap size={10} className="mr-1 fill-current" />
                            {recommendation}
                        </span>
                        <div className="mt-2 text-[10px] font-bold text-slate-400">P/E: {stock.pe_ratio?.toFixed(2) || '--'}</div>
                    </div>
                </div>

                {/* KPI GRID */}
                <div className="grid grid-cols-2 md:grid-cols-2 gap-6 pt-5 border-t border-slate-50">
                    <div className="space-y-1">
                        <span className="text-[9px] font-black text-slate-400 uppercase flex items-center gap-1">
                            <TrendingUp size={10} /> Total Returns
                        </span>
                        <div className={`text-xl font-black tracking-tighter ${isPositive ? 'text-emerald-600' : 'text-rose-600'}`}>
                            ₹{pnl.toLocaleString('en-IN')}
                            <span className="text-[10px] ml-1.5 opacity-80 font-bold">{isPositive ? '↑' : '↓'} {Math.abs(roi)}%</span>
                        </div>
                    </div>
                    
                    <div className="space-y-1">
                        <span className="text-[9px] font-black text-slate-400 uppercase flex items-center gap-1">
                            <Wallet size={10} /> Value
                        </span>
                        <div className="text-xl font-black text-slate-900 tracking-tighter">
                            ₹{stock.current_value?.toLocaleString('en-IN')}
                        </div>
                    </div>
                </div>
                <div className="grid gap-6 pt-5 border-t border-slate-50">
                    <div className="space-y-1">
                        <span className="text-[9px] font-black text-slate-400 uppercase flex items-center gap-1">
                            <Activity size={10} /> AI Rec
                        </span>
                        <div className="text-[11px] font-bold text-orange-600 uppercase mt-1.5 flex items-center gap-1">
                            <Target size={12} /> {aiAction?.trim()}
                        </div>
                    </div>
                </div>
            </div>

            {/* EXPANDED AI SECTION */}
            {expanded && (
                <div className="px-5 md:px-6 pb-6 animate-in slide-in-from-top-2 duration-300">
                    <div className="bg-slate-50 rounded-2xl p-5 border border-slate-200/60 relative overflow-hidden">
                        <div className="relative z-10">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="p-1.5 bg-blue-600 rounded-lg">
                                    <Lightbulb size={14} className="text-white" />
                                </div>
                                <h4 className="text-[10px] font-black text-slate-800 uppercase tracking-widest">Deep Strategy Analysis</h4>
                            </div>
                            
                            <p className="text-[12px] text-slate-600 leading-relaxed mb-6 font-medium italic border-l-2 border-blue-200 pl-4">
                                "{insight.reason}"
                            </p>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="bg-white p-4 rounded-xl border border-rose-100 shadow-sm">
                                    <h5 className="text-[9px] font-black text-rose-500 uppercase mb-3 flex items-center gap-1.5">
                                        <AlertTriangle size={12}/> Identified Risks
                                    </h5>
                                    <ul className="space-y-2">
                                        {risks.map((r, i) => (
                                            <li key={i} className="text-[11px] text-slate-500 flex items-start gap-2 leading-tight">
                                                <span className="text-rose-400 font-bold">•</span> {r}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                                <div className="bg-white p-4 rounded-xl border border-emerald-100 shadow-sm">
                                    <h5 className="text-[9px] font-black text-emerald-500 uppercase mb-3 flex items-center gap-1.5">
                                        <TrendingUp size={12}/> Growth Opportunities
                                    </h5>
                                    <ul className="space-y-2">
                                        {opportunities.map((o, i) => (
                                            <li key={i} className="text-[11px] text-slate-500 flex items-start gap-2 leading-tight">
                                                <span className="text-emerald-400 font-bold">•</span> {o}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
            
            <button 
                onClick={() => setExpanded(!expanded)}
                className="w-full py-3 bg-white text-[10px] font-black text-slate-400 flex items-center justify-center gap-2 hover:text-slate-900 hover:bg-slate-50 transition-all uppercase tracking-widest border-t border-slate-100"
            >
                {expanded ? "Collapse Analysis" : "Analyze Performance"}
                {expanded ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
            </button>
        </div>
    );
};
export default StockCard;