import React from 'react';

export const StockFilters = ({ 
    searchTerm, 
    setSearchTerm, 
    filterType, 
    setFilterType, 
    sectorType, 
    setSectorType, 
    uniqueSectors, 
    resetFilters 
}) => {
    return (
        <div className="flex flex-col md:flex-row gap-3 w-full">
            {/* Search Ticker */}
            <div className="flex-grow">
                <input
                    type="text"
                    placeholder="Search ticker (e.g. BEL, AAPL)..."
                    className="w-full px-4 py-2 rounded-lg border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none shadow-sm transition-all"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </div>

            {/* Status Dropdown */}
            <div className="flex gap-3">
                <select
                    value={filterType}
                    onChange={(e) => setFilterType(e.target.value)}
                    className="min-w-[140px] px-4 py-2 rounded-lg border border-gray-200 bg-white shadow-sm focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer"
                >
                    <option value="All">All Status</option>
                    <option value="buy">Buy</option>
                    <option value="hold">Hold</option>
                    <option value="sell">Sell</option>
                </select>
            </div>

            {/* Sector Dropdown */}
            <div className="flex gap-3">
                <select
                    value={sectorType}
                    onChange={(e) => setSectorType(e.target.value)}
                    className="min-w-[160px] px-4 py-2 rounded-lg border border-gray-200 bg-white shadow-sm focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer"
                >
                    <option value="All">All Sectors</option>
                    {uniqueSectors.map((sector, idx) => (
                        <option key={idx} value={sector}>{sector}</option>
                    ))}
                </select>
            </div>

            {/* Reset Button */}
            <button 
                className="px-4 py-2 border border-blue-600 text-blue-600 hover:bg-blue-50 font-medium rounded-lg transition-colors duration-200 whitespace-nowrap"
                onClick={resetFilters}
            >
                Reset All Filters
            </button>
        </div>
    );
};