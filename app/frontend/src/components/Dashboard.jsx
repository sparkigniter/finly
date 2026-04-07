import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, Globe, User, RefreshCw, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

import { StatsHero } from './StatsHero';
import { StockCard } from './StockCard';
import { StockFilters } from './StockFilters';
import { ConnectTab } from './ConnectTab';
import logo from '../assets/logo.png';

export const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('portfolio');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isSyncing, setIsSyncing] = useState(false);

    const [searchTerm, setSearchTerm] = useState("");
    const [filterType, setFilterType] = useState("All");
    const [sectorType, setSectorType] = useState("All");

    const navigate = useNavigate();
    const { token, logout } = useAuth();
    const API_URL = import.meta.env.VITE_API_URL;

    const handleLogout = useCallback(() => {
        logout();
        localStorage.removeItem('token');
        navigate('/login');
    }, [logout, navigate]);

    const refreshData = useCallback(async () => {
        if (!token) return;
        try {
            const response = await fetch(`${API_URL}/portfolio`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            if (response.status === 401) return handleLogout();

            const result = await response.json();
            setData(typeof result === "string" ? JSON.parse(result) : result);
        } catch (err) {
            console.error("Fetch Error:", err);
        } finally {
            setLoading(false);
        }
    }, [API_URL, token, handleLogout]);

    useEffect(() => { refreshData(); }, [refreshData]);

    const filteredStocks = useMemo(() => {
        if (!data?.individual_stocks) return [];
        return data.individual_stocks.filter((item) => {
            const matchesSearch = item?.ticker?.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesType = filterType === "All" || item?.recommendation?.toLowerCase() === filterType.toLowerCase();
            const matchesSector = sectorType === "All" || item?.sector?.toLowerCase() === sectorType.toLowerCase();
            return matchesSearch && matchesType && matchesSector;
        });
    }, [data, searchTerm, filterType, sectorType]);

    /* ── Loading State (Improved) ───────────────── */
    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50">
                <div className="p-4 bg-white rounded-2xl shadow-md">
                    <RefreshCw className="animate-spin text-orange-500" size={28} />
                </div>
                <p className="text-slate-500 mt-4 font-medium tracking-wide">
                    Analyzing your portfolio...
                </p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white pb-24 md:pb-10">

            {/* ── Top Nav (Refined) ───────────────── */}
            <nav className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 border-b border-slate-200">
                <div className="max-w-[1400px] mx-auto px-6 py-4 flex justify-between items-center">

                    {/* Logo */}
                    <img src={logo} alt="Finly" className="h-10 object-contain" />

                    {/* Tabs */}
                    <div className="hidden md:flex bg-slate-100 p-1 rounded-xl">
                        {['portfolio', 'connect'].map(tab => (
                            <button
                                key={tab}
                                onClick={() => setActiveTab(tab)}
                                className={`px-6 py-2 rounded-lg text-sm font-semibold transition-all ${
                                    activeTab === tab
                                        ? "bg-white shadow text-slate-900"
                                        : "text-slate-500 hover:text-slate-700"
                                }`}
                            >
                                {tab === 'portfolio' ? 'Portfolio' : 'Sync Sources'}
                            </button>
                        ))}
                    </div>

                    {/* Right */}
                    <div className="flex items-center gap-4">
                        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-orange-50 rounded-lg border border-orange-100">
                            <div className="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-bold">
                                VG
                            </div>
                            <span className="text-xs font-semibold text-orange-700">
                                Vicky G.
                            </span>
                        </div>

                        <button
                            onClick={handleLogout}
                            className="p-2 rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 transition"
                        >
                            <LogOut size={18} />
                        </button>
                    </div>
                </div>
            </nav>

            {/* ── Main ───────────────── */}
            <main className="max-w-[1400px] mx-auto px-4 md:px-6 py-8">

                {activeTab === 'portfolio' ? (
                    <div className="space-y-8 animate-in fade-in duration-500">

                        {/* Hero */}
                        {data?.portfolio_summary && (
                            <StatsHero summary={data.portfolio_summary} />
                        )}

                        {/* Filters */}
                        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
                            <StockFilters
                                searchTerm={searchTerm}
                                setSearchTerm={setSearchTerm}
                                filterType={filterType}
                                setFilterType={setFilterType}
                                sectorType={sectorType}
                                setSectorType={setSectorType}
                                uniqueSectors={[
                                    ...new Set(data?.individual_stocks?.map(s => s.sector))
                                ].filter(Boolean)}
                            />
                        </div>

                        {/* Stocks */}
                        {filteredStocks.length > 0 ? (
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {filteredStocks.map((stock, i) => (
                                    <div
                                        key={stock.ticker || i}
                                        className="transition-transform hover:-translate-y-1"
                                    >
                                        <StockCard stock={stock} />
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
                                <p className="text-slate-500 font-medium">
                                    No stocks match your filters
                                </p>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="animate-in fade-in duration-500">
                        <ConnectTab
                            isSyncing={isSyncing}
                            setIsSyncing={setIsSyncing}
                            refreshData={refreshData}
                            token={token}
                            API_URL={API_URL}
                        />
                    </div>
                )}
            </main>

            {/* ── Mobile Nav (Improved) ───────────────── */}
            <div className="md:hidden fixed bottom-4 left-4 right-4 bg-white/90 backdrop-blur-xl border border-slate-200 rounded-2xl shadow-lg flex justify-around py-3 z-50">

                <NavItem icon={<LayoutDashboard size={20} />} label="Portfolio" active={activeTab === 'portfolio'} onClick={() => setActiveTab('portfolio')} />

                <NavItem icon={<Globe size={20} />} label="Sync" active={activeTab === 'connect'} onClick={() => setActiveTab('connect')} />

                <NavItem icon={<User size={20} />} label="Logout" onClick={handleLogout} />
            </div>
        </div>
    );
};

/* ── Reusable Mobile Nav Item ───────────────── */
const NavItem = ({ icon, label, active, onClick }) => (
    <button
        onClick={onClick}
        className={`flex flex-col items-center text-xs font-semibold ${
            active ? "text-orange-500" : "text-slate-400"
        }`}
    >
        {icon}
        <span className="mt-1">{label}</span>
    </button>
);

export default Dashboard;