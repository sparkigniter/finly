import React, { useState, useEffect } from 'react';
import { StatsHero } from './components/StatsHero';
import { StockCard } from './components/StockCard';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Using your local API endpoint
  const API_URL = "http://0.0.0.0:8000/portfolio/1";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Failed to reach backend server");
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-slate-400 font-bold animate-pulse uppercase tracking-widest text-xs">Syncing with Finly Engine...</p>
      </div>
    </div>
  );

  if (error) return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-6">
      <div className="bg-white p-8 rounded-3xl shadow-xl border border-rose-100 text-center max-w-md">
        <div className="text-4xl mb-4">🔌</div>
        <h2 className="text-xl font-black text-slate-900 mb-2">Backend Connection Failed</h2>
        <p className="text-slate-500 text-sm mb-6">Make sure your Python server is running on port 8000 and CORS is enabled.</p>
        <button 
          onClick={() => window.location.reload()}
          className="bg-slate-900 text-white px-6 py-2 rounded-full text-xs font-bold hover:bg-slate-800 transition-colors"
        >
          Try Again
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F8FAFC] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-12 flex justify-between items-end">
          <div>
            <h1 className="text-5xl font-black text-slate-900 tracking-tighter">FINLY<span className="text-blue-600">.</span></h1>
            <p className="text-slate-400 text-xs font-bold uppercase tracking-[0.3em] mt-1">Intelligence Dashboard</p>
          </div>
          <div className="hidden md:block text-right">
            <span className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-50 text-emerald-600 rounded-full text-[10px] font-black border border-emerald-100">
              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
              LIVE DATA
            </span>
          </div>
        </header>

        <StatsHero summary={data?.portfolio_summary} />

        <div className="mt-12">
          <div className="flex justify-between items-center mb-6 px-2">
            <h3 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Holdings Analysis</h3>
            <p className="text-[10px] text-slate-400 font-medium italic">Showing {data?.individual_stocks?.length} Assets</p>
          </div>
          
          <div className="space-y-3">
            {data?.individual_stocks?.map((stock, idx) => (
              <StockCard key={idx} stock={stock} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;