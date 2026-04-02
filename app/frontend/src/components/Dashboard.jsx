import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { StatsHero } from './StatsHero';
import { StockCard } from './StockCard';
import { FileUpload } from './FileUpload';
import { StockFilters } from './StockFilters';
import { useAuth } from '../context/AuthContext';
import { Globe, RefreshCw, LogOut, User, LayoutDashboard } from 'lucide-react';
import logo from '../assets/logo.png';

export const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isSyncing, setIsSyncing] = useState(false);
    const [syncStatus, setSyncStatus] = useState(null);
    
    const [searchTerm, setSearchTerm] = useState("");
    const [filterType, setFilterType] = useState("All");
    const [sectorType, setSectorType] = useState("All");

    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();
    const { token, logout } = useAuth(); 
    const API_URL = import.meta.env.VITE_API_URL;

    const handleLogout = useCallback(() => {
        logout();
        localStorage.removeItem('token');
        navigate('/login');
    }, [logout, navigate]);

    const refreshData = useCallback(async () => {
        try {
            const response = await fetch(`${API_URL}/portfolio`, {
                headers: { "Authorization": `Bearer ${token}` },
            });
            
            if (response.status === 401) return handleLogout();
            if (!response.ok) throw new Error("Failed to fetch");
            
            let result = await response.json();
            if(typeof result === "string") {
                result = JSON.parse(result);
            }
            setData(result);
        } catch (err) {
            console.error("Data Fetch Error:", err);
        }
    }, [API_URL, token, handleLogout]);

    const handleBrokerLogin = async () => {
        setIsSyncing(true);
        try {
            const response = await fetch(`${API_URL}/broker/kite/login`, {
                headers: { "Authorization": `Bearer ${token}` },
            });
            const { login_url } = await response.json();
            window.location.href = login_url;
        } catch (err) {
            console.error("Broker Init Failed:", err);
            setIsSyncing(false);
        }
    };

    const triggerAnalysis = async () => {
        setIsSyncing(true);
        try {
            await fetch(`${API_URL}/analyze-portfolio`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${token}` },
            });
            setSyncStatus('success');
            setTimeout(() => setSyncStatus(null), 5000);
            refreshData();
        } finally {
            setIsSyncing(false);
        }
    };

    useEffect(() => {
        if (searchParams.get("sync") === "success") {
            setSearchParams({}); 
            triggerAnalysis();
        }
        refreshData().finally(() => setLoading(false));
    }, [searchParams, refreshData]);

    const filteredStocks = useMemo(() => {
        console.log(typeof(data))
        if (!data?.individual_stocks) return [];
        console.log((data.individual_stocks));
        return data.individual_stocks.filter((item) => {
            const matchesSearch = item?.ticker?.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesType = filterType === "All" || item?.recommendation?.toLowerCase() === filterType.toLowerCase();
            const matchesSector = sectorType === "All" || (item?.sector !== "null" && item?.sector?.toLowerCase() === sectorType.toLowerCase());
            return matchesSearch && matchesType && matchesSector;
        });
    }, [data, searchTerm, filterType, sectorType]);


    if (loading) return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-slate-50">
            <RefreshCw className="animate-spin text-orange-500 mb-4" size={32} />
            <p className="text-slate-500 font-medium tracking-wide">Syncing Finly Portfolio...</p>
        </div>
    );

    return (
        <div className="min-h-screen bg-[#F8FAFC]">
            {/* Top Navigation */}
            <nav className="bg-white border-b border-slate-100 sticky top-0 z-50">
                <div className="max-w-[1400px] mx-auto px-6 py-4 flex items-center justify-between">
                    <img src={logo} alt="Finly Logo" className="h-10 w-auto object-contain" />
                    <div className="flex items-center gap-6">
                        <div className="flex items-center gap-3 px-4 py-2 bg-slate-50 rounded-xl border border-slate-100">
                            <div className="w-8 h-8 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center font-bold text-xs">VG</div>
                            <span className="text-sm font-semibold text-slate-700 hidden sm:block">Vicky Goudar</span>
                        </div>
                        <button onClick={handleLogout} className="text-slate-400 hover:text-red-500 transition-colors p-2">
                            <LogOut size={20}/>
                        </button>
                    </div>
                </div>
            </nav>

            <main className="max-w-[1400px] mx-auto py-10 px-6">
                <header className="mb-10 p-8 bg-white rounded-[2rem] border border-slate-100 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                    <div>
                        <div className="flex items-center gap-2 text-orange-500 font-bold text-xs uppercase tracking-widest mb-2">
                            <LayoutDashboard size={14} /> Intelligence Dashboard
                        </div>
                        <h1 className="text-4xl font-black text-slate-900 tracking-tight">Finly - Portfolio Analysis</h1>
                        <p className="text-slate-500 mt-2 text-lg">AI-driven analysis for your Indian equity markets.</p>
                    </div>
                    
                    <div className="flex items-center gap-3 p-2 bg-slate-50 rounded-2xl border border-slate-100">
                        <button 
                            onClick={handleBrokerLogin}
                            disabled={isSyncing}
                            className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm transition-all shadow-lg active:scale-95 ${
                                syncStatus === 'success' ? "bg-green-600 text-white" : "bg-orange-500 text-white hover:bg-orange-600 shadow-orange-200"
                            }`}
                        >
                            {isSyncing ? <RefreshCw className="animate-spin" size={18}/> : <Globe size={18}/>}
                            {syncStatus === 'success' ? "Connected" : "Sync Zerodha"}
                        </button>
                        <div className="w-[1px] h-8 bg-slate-200 mx-2" />
                        <FileUpload onUploadSuccess={refreshData} />
                    </div>
                </header>

                {data?.portfolio_summary && <StatsHero summary={data.portfolio_summary} />}
                
                <section className="mt-12">
                    <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm mb-8">
                        <StockFilters 
                            searchTerm={searchTerm} setSearchTerm={setSearchTerm}
                            filterType={filterType} setFilterType={setFilterType}
                            sectorType={sectorType} setSectorType={setSectorType}
                            uniqueSectors={[...new Set(data?.individual_stocks?.map(s => s.sector))].filter(s => s && s !== "null")}
                        />
                    </div>
                    {console.log("Filtered Stocks:", filteredStocks)}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {filteredStocks.map((stock, i) => (
                            <StockCard key={stock.ticker || i} stock={stock} />
                        ))}
                    </div>
                </section>
            </main>
        </div>
    );
};  

export default Dashboard;