import React, { useState } from 'react';
import { Globe, FileText, RefreshCw, CheckCircle2 } from 'lucide-react';
import { FileUpload } from './FileUpload';

export const ConnectTab = ({ isSyncing, setIsSyncing, refreshData, token, API_URL }) => {
    const [syncStatus, setSyncStatus] = useState(null);

    const handleBrokerLogin = async () => {
        setIsSyncing(true);
        try {
            const response = await fetch(`${API_URL}/broker/kite/login`, {
                headers: { "Authorization": `Bearer ${token}` },
            });
            const { login_url } = await response.json();
            window.location.href = login_url;
        } catch (err) {
            console.error("Sync Failed:", err);
            setIsSyncing(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center mb-10">
                <h2 className="text-3xl font-black text-slate-900">Data Sources</h2>
                <p className="text-slate-500 mt-2">Update your portfolio via broker sync or manual upload.</p>
            </div>

            {/* Zerodha Sync Card */}
            <div className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm transition-all hover:shadow-md">
                <div className="flex flex-col sm:flex-row items-center gap-6">
                    <div className="w-16 h-16 bg-blue-50 rounded-3xl flex items-center justify-center text-blue-600">
                        <Globe size={32} />
                    </div>
                    <div className="flex-1 text-center sm:text-left">
                        <h3 className="text-xl font-bold text-slate-900">Zerodha Kite</h3>
                        <p className="text-slate-500 text-sm">Automatically import holdings and P&L data.</p>
                    </div>
                    <button 
                        onClick={handleBrokerLogin}
                        disabled={isSyncing}
                        className="w-full sm:w-auto px-8 py-3 bg-slate-900 text-white rounded-2xl font-bold text-sm hover:bg-slate-800 transition-all active:scale-95 disabled:opacity-50"
                    >
                        {isSyncing ? <RefreshCw className="animate-spin mx-auto" size={20}/> : "Connect Broker"}
                    </button>
                </div>
            </div>

            {/* Manual Upload Card */}
            <div className="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm transition-all hover:shadow-md">
                <div className="flex flex-col sm:flex-row items-center gap-6">
                    <div className="w-16 h-16 bg-orange-50 rounded-3xl flex items-center justify-center text-orange-600">
                        <FileText size={32} />
                    </div>
                    <div className="flex-1 text-center sm:text-left">
                        <h3 className="text-xl font-bold text-slate-900">Excel Export</h3>
                        <p className="text-slate-500 text-sm">Upload your Zerodha or Groww XLSX files.</p>
                    </div>
                    <FileUpload onUploadSuccess={refreshData} />
                </div>
            </div>

            {syncStatus === 'success' && (
                <div className="flex items-center gap-2 justify-center text-green-600 font-bold animate-bounce">
                    <CheckCircle2 size={18} /> Portfolio Updated Successfully
                </div>
            )}
        </div>
    );
};

export default ConnectTab;  