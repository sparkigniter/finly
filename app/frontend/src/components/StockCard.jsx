import React, { useState } from 'react';

export const StockCard = ({ stock }) => {
  const [isOpen, setIsOpen] = useState(false);

  const recStyles = {
    BUY: "bg-emerald-50 text-emerald-700 border-emerald-200",
    HOLD: "bg-amber-50 text-amber-700 border-amber-200",
    SELL: "bg-rose-50 text-rose-700 border-rose-200",
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden mb-4 transition-all hover:border-blue-200">
      <div 
        className="p-5 flex items-center justify-between cursor-pointer hover:bg-slate-50/50"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-slate-100 rounded-xl flex items-center justify-center font-bold text-slate-500 text-xl">
            {stock.ticker[0]}
          </div>
          <div>
            <h3 className="font-bold text-slate-900 text-lg">{stock.ticker}</h3>
            <p className="text-[10px] text-slate-400 uppercase font-black tracking-widest">{stock.sector}</p>
          </div>
        </div>

        <div className="flex items-center gap-8">
          <div className="hidden md:block text-right">
            <p className="text-[10px] text-slate-400 uppercase font-bold">Performance</p>
            <p className={`font-bold ${stock.performance_pct >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
              {(stock.performance_pct * 100).toFixed(2)}%
            </p>
          </div>
          <span className={`px-4 py-1.5 rounded-full text-[11px] font-black border ${recStyles[stock.recommendation] || 'bg-slate-100'}`}>
            {stock.recommendation}
          </span>
        </div>
      </div>

      {isOpen && (
        <div className="p-6 bg-slate-50 border-t border-slate-100 space-y-6 animate-in slide-in-from-top-2 duration-300">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
              <h4 className="text-[10px] font-black text-slate-400 uppercase mb-3 tracking-widest">Technical Outlook</h4>
              <p className="text-sm text-slate-600 leading-relaxed italic">"{stock.technical_view}"</p>
            </div>
            
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
              <h4 className="text-[10px] font-black text-slate-400 uppercase mb-3 tracking-widest">Fundamental Summary</h4>
              <p className="text-sm text-slate-600 leading-relaxed">"{stock.fundamental_summary}"</p>
            </div>
          </div>

          <div className="bg-blue-50 p-5 rounded-xl border border-blue-100">
            <h4 className="text-[10px] font-black text-blue-500 uppercase mb-3 tracking-widest">AI Market Intelligence</h4>
            <p className="text-sm text-slate-700 leading-relaxed">{stock.latest_news}</p>
          </div>
        </div>
      )}
    </div>
  );
};