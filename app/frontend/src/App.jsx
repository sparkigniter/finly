import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { StatsHero } from './components/StatsHero';
import { StockCard } from './components/StockCard';
import { FileUpload } from './components/FileUpload';
import { StockFilters } from './components/StockFilters';
import logo from './assets/logo.png';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("All");
  const [sectorType, setSectorType] = useState("All");

  const API_URL = "http://localhost:8000/portfolio/1";

  const refreshData = useCallback(async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Failed to fetch");
      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error("Refresh failed:", err);
    }
  }, []);

  useEffect(() => {
    refreshData().finally(() => setLoading(false));
  }, [refreshData]);

  // 1. Get Unique Sectors from the raw data
  const uniqueSectors = useMemo(() => {
    if (!data?.individual_stocks) return [];
    const sectors = data.individual_stocks
      .map(item => item.sector)
      .filter(Boolean);
    return [...new Set(sectors)].sort();
  }, [data]);

  // 2. Combined Filter Logic (Search + Status + Sector)
  const filteredStocks = useMemo(() => {
    if (!data?.individual_stocks) return [];

    return data.individual_stocks.filter((item) => {
      const ticker = item?.ticker?.toLowerCase() || "";
      const recommendation = item?.recommendation?.toLowerCase() || "";
      const sector = item?.sector?.toLowerCase() || "";
      const search = searchTerm.toLowerCase();

      const matchesSearch = ticker.includes(search);
      const matchesType = filterType === "All" || recommendation === filterType.toLowerCase();
      const matchesSector = sectorType === "All" || sector === sectorType.toLowerCase();

      return matchesSearch && matchesType && matchesSector;
    });
  }, [data, searchTerm, filterType, sectorType]);

  const resetFilters = () => {
    setSearchTerm("");
    setFilterType("All");
    setSectorType("All");
  }

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen font-medium text-gray-500">
      Initializing Finly Engine...
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F8FAFC] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">

        <header className="mb-12 flex flex-col gap-6">

          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <img src={logo} alt="Finly Logo" className="h-10 w-auto object-contain header-logo" />
            <div className="w-full md:w-auto">
              <FileUpload onUploadSuccess={refreshData} />
            </div>
          </div>
        </header>
        <div className="py-12 px-4 sm:px-6 lg:px-8">
          {/* Stock Filters */}
          <StockFilters 
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            filterType={filterType}
            setFilterType={setFilterType}
            sectorType={sectorType}
            setSectorType={setSectorType}
            uniqueSectors={uniqueSectors}
            resetFilters={() => {
                setSearchTerm("");
                setFilterType("All");
                setSectorType("All");
            }}
          />
        </div>

        {/* MAIN CONTENT AREA */}
        {data ? (
          <>
            {/* Global Portfolio Stats */}
            <StatsHero summary={data.portfolio_summary} />

            {/* Section Header */}
            <div className="flex justify-between items-center mt-12 mb-6">
              <h3 className="text-xl font-bold text-gray-800">Portfolio Breakdown</h3>
              <div className="text-sm font-semibold text-blue-600 bg-blue-50 px-4 py-1.5 rounded-full border border-blue-100">
                {filteredStocks.length} {filteredStocks.length === 1 ? 'Asset' : 'Assets'} Found
              </div>
            </div>

            {/* Stock List Container */}
            <div className="space-y-4 w-full">
              {filteredStocks.length > 0 ? (
                filteredStocks.map((stock, idx) => (
                  <StockCard key={idx} stock={stock} />
                ))
              ) : (
                <div className="text-center py-24 bg-white rounded-2xl border-2 border-dashed border-gray-200 text-gray-400 w-full">
                  <p className="text-lg">No matches found for your current filters.</p>
                  <button
                    onClick={() => { setSearchTerm(""); setFilterType("All"); setSectorType("All"); }}
                    className="mt-4 text-blue-500 font-medium hover:underline"
                  >
                    Reset all filters
                  </button>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="text-center py-20 bg-white rounded-2xl shadow-sm border border-gray-100">
            <p className="text-gray-500">Upload your Zerodha export to see AI-driven insights.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;