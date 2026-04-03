export const StatsHero = ({ summary }) => {
    return (
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 lg:gap-6">
            <div className="p-5 bg-white rounded-3xl border border-slate-100 shadow-sm">
                <p className="text-[10px] font-bold text-slate-400 uppercase">Investment</p>
                <h2 className="text-xl font-black text-slate-900 mt-1">₹{summary.total_investment?.toLocaleString()}</h2>
            </div>
            <div className="p-5 bg-white rounded-3xl border border-slate-100 shadow-sm">
                <p className="text-[10px] font-bold text-slate-400 uppercase">Returns</p>
                <h2 className="text-xl font-black text-green-600 mt-1">₹{summary.total_returns?.toLocaleString()}</h2>
            </div>
            <div className="p-5 bg-slate-900 rounded-3xl shadow-lg col-span-2 lg:col-span-1 flex justify-between items-center">
                <div>
                    <p className="text-[10px] font-bold text-slate-500 uppercase">Overall Performance</p>
                    <h2 className="text-xl font-black text-white mt-1">{summary.overall_performance_pct}%</h2>
                </div>
                <div className="w-10 h-10 bg-orange-500 rounded-xl flex items-center justify-center text-white font-black text-xs">
                    {summary.diversification_score || 0}
                </div>
            </div>
        </div>
    );
};

export default StatsHero;