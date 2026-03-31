import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { StatsHero } from './StatsHero';
import { StockCard } from './StockCard';
import { FileUpload } from './FileUpload';
import {StockFilters} from './StockFilters';
import logo from '../assets/logo.png';
import '../App.css';

export const Dashboard = () => {
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


    if (loading) return (
        <div className="flex items-center justify-center min-h-screen font-medium text-gray-500">
            Initializing Finly Engine...
        </div>
    );

    return (
        <div className="max-w-5xl mx-auto py-12 px-4">
            <header className="mb-12 flex flex-col gap-6">
                <div className="flex justify-between items-center">
                    <img src={logo} alt="Finly Logo" className="h-10 w-auto" />
                    <FileUpload onUploadSuccess={refreshData} />
                </div>
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
            </header>

            {data && (
                <>
                    <StatsHero summary={data.portfolio_summary} />
                    <div className="space-y-4 mt-10">
                        {filteredStocks.map((stock, idx) => <StockCard key={idx} stock={stock} />)}
                    </div>
                </>
            )}
        </div>
    );
};
