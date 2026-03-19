import React, { useState, useEffect, useCallback } from 'react';
import { StatsHero } from './components/StatsHero';
import { StockCard } from './components/StockCard';
import { FileUpload } from './components/FileUpload';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = "http://localhost:8000/portfolio/1";

  // 1. Define the refresh logic using useCallback for better performance
  const refreshData = useCallback(async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Failed to sync data");
      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error("Refresh failed:", err);
    }
  }, []);

  // 2. Run the initial fetch on load
  useEffect(() => {
    refreshData().finally(() => setLoading(false));
  }, [refreshData]);

  if (loading) return <div className="text-center p-20">Loading Finly...</div>;

  return (
    <div className="min-h-screen bg-[#F8FAFC] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <header className="mb-12">
          <h1 className="text-5xl font-black text-slate-900 tracking-tighter">FINLY.</h1>
        </header>

        {/* 3. Pass the function as a prop to FileUpload */}
        <FileUpload onUploadSuccess={refreshData} />

        {data && (
          <>
            <StatsHero summary={data.portfolio_summary} />
            <div className="space-y-3 mt-10">
              {data.individual_stocks.map((stock, idx) => (
                <StockCard key={idx} stock={stock} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;