import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Activity, BarChart3, Newspaper, TrendingUp, TrendingDown } from 'lucide-react';

export const StockCard = ({ stock }) => {
    const [expanded, setExpanded] = useState(false);
    const isPos = stock.performance_pct >= 0;

    return (
        <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm transition-all active:bg-slate-50">
            <div className="p-5" onClick={() => setExpanded(!expanded)}>
                <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center font-black text-slate-700 border border-slate-100">
                            {stock.ticker?.substring(0, 2)}
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-900 leading-none">{stock.ticker}</h3>
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                                {stock.sector === "null" ? "Diversified" : stock.sector}
                            </span>
                        </div>
                    </div>
                    <div className="text-right">
                        <div className={`flex items-center justify-end gap-1 font-black ${isPos ? 'text-green-600' : 'text-red-600'}`}>
                            {isPos ? <TrendingUp size={14}/> : <TrendingDown size={14}/>}
                            {isPos ? '+' : ''}{stock.performance_pct}%
                        </div>
                        <span className="text-[9px] font-black px-2 py-0.5 rounded-md bg-slate-100 text-slate-500 uppercase">
                            {stock.recommendation}
                        </span>
                    </div>
                </div>

                {!expanded && (
                    <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed italic">
                        "{stock.technical_view}"
                    </p>
                )}
            </div>

            {expanded && (
                <div className="px-5 pb-6 space-y-5 animate-in slide-in-from-top-2 duration-300">
                    <div className="grid grid-cols-2 gap-3">
                        <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                            <p className="text-[9px] font-bold text-slate-400 uppercase">Gain/Loss</p>
                            <p className="text-sm font-black text-slate-800">₹{stock.total_gain_loss?.toLocaleString()}</p>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                            <p className="text-[9px] font-bold text-slate-400 uppercase">Div. Yield</p>
                            <p className="text-sm font-black text-slate-800">{stock.dividend_yield}%</p>
                        </div>
                    </div>

                    <div className="space-y-4 pt-2">
                        <div className="group">
                            <h4 className="flex items-center gap-2 text-[10px] font-black text-orange-600 uppercase mb-2">
                                <Activity size={12}/> Technical Analysis
                            </h4>
                            <p className="text-xs text-slate-600 leading-relaxed bg-orange-50/30 p-3 rounded-xl border border-orange-100/20">
                                {stock.technical_view}
                            </p>
                        </div>

                        <div className="group">
                            <h4 className="flex items-center gap-2 text-[10px] font-black text-blue-600 uppercase mb-2">
                                <BarChart3 size={12}/> Fundamentals
                            </h4>
                            <p className="text-xs text-slate-600 leading-relaxed bg-blue-50/30 p-3 rounded-xl border border-blue-100/20">
                                {stock.fundamental_summary}
                            </p>
                        </div>
                    </div>
                </div>
            )}
            
            <button 
                onClick={() => setExpanded(!expanded)}
                className="w-full py-4 text-[10px] font-black text-slate-300 border-t border-slate-50 flex items-center justify-center gap-2 tracking-tighter"
            >
                {expanded ? "COLLAPSE" : "TAP FOR FULL AI ANALYSIS"}
                {expanded ? <ChevronUp size={12}/> : <ChevronDown size={12}/>}
            </button>
        </div>
    );
};