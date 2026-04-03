import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, Globe, User, RefreshCw, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

// Components
import { StatsHero } from './StatsHero';
import { StockCard } from './StockCard';
import { StockFilters } from './StockFilters';
import { ConnectTab } from './ConnectTab';
import logo from '../assets/logo.png';

export const Dashboard = () => {
    const [activeTab, setActiveTab] = useState('portfolio'); // 'portfolio' | 'connect'
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
                headers: { "Authorization": `Bearer ${token}` },
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
            const matchesSector = sectorType === "All" || (item?.sector && item?.sector?.toLowerCase() === sectorType.toLowerCase());
            return matchesSearch && matchesType && matchesSector;
        });
    }, [data, searchTerm, filterType, sectorType]);

    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50">
            <RefreshCw className="animate-spin text-orange-500 mb-4" size={32} />
            <p className="text-slate-500 font-medium">Loading Finly Analysis...</p>
        </div>
    );

    return (
        <div className="min-h-screen bg-[#F8FAFC] pb-24 md:pb-10">
            {/* Desktop Top Nav */}
            <nav className="bg-white border-b border-slate-100 sticky top-0 z-50 px-6 py-4">
                <div className="max-w-[1400px] mx-auto flex items-center justify-between">
                    <img src={logo} alt="Finly" className="h-8 md:h-10 w-auto object-contain" />
                    
                    {/* Desktop Tab Switcher */}
                    <div className="hidden md:flex bg-slate-100 p-1 rounded-xl">
                        <button 
                            onClick={() => setActiveTab('portfolio')}
                            className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'portfolio' ? "bg-white shadow-sm text-slate-900" : "text-slate-500"}`}
                        >
                            Portfolio
                        </button>
                        <button 
                            onClick={() => setActiveTab('connect')}
                            className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${activeTab === 'connect' ? "bg-white shadow-sm text-slate-900" : "text-slate-500"}`}
                        >
                            Sync Sources
                        </button>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-orange-50 rounded-lg border border-orange-100">
                            <div className="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center text-[10px] font-bold">VG</div>
                            <span className="text-xs font-bold text-orange-700">Vicky G.</span>
                        </div>
                        <button onClick={handleLogout} className="text-slate-400 hover:text-red-500 transition-colors">
                            <LogOut size={20}/>
                        </button>
                    </div>
                </div>
            </nav>

            <main className="max-w-[1400px] mx-auto py-8 px-4 md:px-6">
                {activeTab === 'portfolio' ? (
                    <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
                        <header className="mb-8">
                            <h1 className="text-3xl font-black text-slate-900 tracking-tight">Portfolio Intelligence</h1>
                            <p className="text-slate-500">Real-time analysis of your equity holdings.</p>
                        </header>

                        {data?.portfolio_summary && <StatsHero summary={data.portfolio_summary} />}
                        
                        <section className="mt-10">
                            <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm mb-6">
                                <StockFilters 
                                    searchTerm={searchTerm} setSearchTerm={setSearchTerm}
                                    filterType={filterType} setFilterType={setFilterType}
                                    sectorType={sectorType} setSectorType={setSectorType}
                                    uniqueSectors={[...new Set(data?.individual_stocks?.map(s => s.sector))].filter(s => s && s !== "null")}
                                />
                            </div>
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {filteredStocks.map((stock, i) => (
                                    <StockCard key={stock.ticker || i} stock={stock} />
                                ))}
                            </div>
                        </section>
                    </div>
                ) : (
                    <ConnectTab 
                        isSyncing={isSyncing} 
                        setIsSyncing={setIsSyncing} 
                        refreshData={refreshData} 
                        token={token} 
                        API_URL={API_URL} 
                    />
                )}
            </main>

            {/* Mobile Bottom Navigation */}
            <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-md border-t border-slate-100 flex justify-around py-4 z-50">
                <button onClick={() => setActiveTab('portfolio')} className={`flex flex-col items-center gap-1 ${activeTab === 'portfolio' ? "text-orange-500" : "text-slate-400"}`}>
                    <LayoutDashboard size={22} />
                    <span className="text-[10px] font-bold uppercase tracking-tighter">Portfolio</span>
                </button>
                <button onClick={() => setActiveTab('connect')} className={`flex flex-col items-center gap-1 ${activeTab === 'connect' ? "text-orange-500" : "text-slate-400"}`}>
                    <Globe size={22} />
                    <span className="text-[10px] font-bold uppercase tracking-tighter">Sync Data</span>
                </button>
                <button onClick={handleLogout} className="flex flex-col items-center gap-1 text-slate-400">
                    <User size={22} />
                    <span className="text-[10px] font-bold uppercase tracking-tighter">Profile</span>
                </button>
            </div>
        </div>
    );
};

export default Dashboard;