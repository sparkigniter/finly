import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Activity, BarChart3, Newspaper, TrendingUp, TrendingDown } from 'lucide-react';

export const StockCard = ({ stock }) => {
    const [expanded, setExpanded] = useState(false);
    const isPositive = stock.performance_pct >= 0;

    return (
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-slate-200/50 transition-all duration-500 overflow-hidden group">
            <div className="p-6 cursor-pointer" onClick={() => setExpanded(!expanded)}>
                <div className="flex justify-between items-start">
                    <div className="flex gap-4">
                        <div className="w-14 h-14 rounded-2xl bg-slate-50 flex items-center justify-center font-black text-slate-800 text-xl border border-slate-100 group-hover:bg-orange-50 group-hover:text-orange-600 transition-colors">
                            {stock.ticker?.substring(0, 2)}
                        </div>
                        <div>
                            <h3 className="text-xl font-black text-slate-900">{stock.ticker}</h3>
                            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                {stock.sector === "null" ? "Diversified" : stock.sector}
                            </p>
                        </div>
                    </div>
                    <div className="text-right">
                        <div className={`flex items-center justify-end gap-1 font-black text-lg ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                            {isPositive ? <TrendingUp size={18}/> : <TrendingDown size={18}/>}
                            {isPositive ? '+' : ''}{stock.performance_pct}%
                        </div>
                        <span className={`inline-block mt-2 px-3 py-1 rounded-lg text-[10px] font-black border tracking-tighter ${
                            stock.recommendation === 'HOLD' ? 'bg-orange-50 text-orange-600 border-orange-100' : 'bg-green-50 text-green-600 border-green-100'
                        }`}>
                            AI RECOMMENDATION: {stock.recommendation}
                        </span>
                    </div>
                </div>
            </div>

            {expanded && (
                <div className="px-6 pb-8 space-y-6 animate-in fade-in slide-in-from-top-4 duration-300">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                            <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Total Gain/Loss</p>
                            <p className="text-lg font-black text-slate-800">₹{stock.total_gain_loss?.toLocaleString()}</p>
                        </div>
                        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                            <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">Div. Yield</p>
                            <p className="text-lg font-black text-slate-800">{stock.dividend_yield}%</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="p-4 bg-orange-50/30 rounded-2xl border border-orange-100/50">
                            <h4 className="flex items-center gap-2 text-xs font-black text-orange-700 uppercase mb-2">
                                <Activity size={14}/> Technical View
                            </h4>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium">{stock.technical_view}</p>
                        </div>

                        <div className="p-4 bg-blue-50/30 rounded-2xl border border-blue-100/50">
                            <h4 className="flex items-center gap-2 text-xs font-black text-blue-700 uppercase mb-2">
                                <BarChart3 size={14}/> Fundamental Summary
                            </h4>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium">{stock.fundamental_summary}</p>
                        </div>

                        <div className="p-4 bg-indigo-50/30 rounded-2xl border border-indigo-100/50">
                            <h4 className="flex items-center gap-2 text-xs font-black text-indigo-700 uppercase mb-2">
                                <Newspaper size={14}/> Intelligence & News
                            </h4>
                            <p className="text-sm text-slate-600 leading-relaxed font-medium italic">{stock.latest_news}</p>
                        </div>
                    </div>
                </div>
            )}

            <div className="px-6 py-3 bg-slate-50/50 border-t border-slate-100 flex justify-center">
                <button onClick={() => setExpanded(!expanded)} className="text-[10px] font-black text-slate-400 hover:text-orange-500 uppercase tracking-widest flex items-center gap-2">
                    {expanded ? "Collapse Insight" : "Expand Full AI Analysis"}
                    {expanded ? <ChevronUp size={14}/> : <ChevronDown size={14}/>}
                </button>
            </div>
        </div>
    );
};

export default StockCard;