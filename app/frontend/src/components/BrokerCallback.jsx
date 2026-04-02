import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { RefreshCw, CheckCircle2, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const BrokerCallback = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { token } = useAuth();
    const [status, setStatus] = useState('syncing'); // 'syncing', 'success', 'error'
    
    const API_URL = import.meta.env.VITE_API_URL;

    useEffect(() => {
        const syncBroker = async () => {
            const requestToken = searchParams.get("request_token");
            const userId = searchParams.get("user_id");

            if (!requestToken || !userId) {
                setStatus('error');
                return;
            }

            try {
                // Call your FastAPI backend to exchange tokens and save to Redis
                const response = await fetch(`${API_URL}/broker/kite/callback?request_token=${requestToken}&user_id=${userId}`, {
                    method: "GET",
                    headers: { "Authorization": `Bearer ${token}` }
                });

                if (response.ok) {
                    setStatus('success');
                    // Wait 2 seconds so user sees the success state, then go to dashboard
                    setTimeout(() => navigate("/dashboard"), 2000);
                } else {
                    setStatus('error');
                }
            } catch (err) {
                console.error("Sync failed:", err);
                setStatus('error');
            }
        };

        syncBroker();
    }, [searchParams, API_URL, token, navigate]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
            <div className="bg-white p-8 rounded-2xl shadow-xl max-w-sm w-full text-center">
                {status === 'syncing' && (
                    <>
                        <RefreshCw className="animate-spin mx-auto text-orange-500 mb-4" size={48} />
                        <h2 className="text-2xl font-bold text-gray-800">Syncing Zerodha</h2>
                        <p className="text-gray-500 mt-2">Connecting your portfolio to Finly Engine...</p>
                    </>
                )}

                {status === 'success' && (
                    <>
                        <CheckCircle2 className="mx-auto text-green-500 mb-4" size={48} />
                        <h2 className="text-2xl font-bold text-gray-800">Connection Successful</h2>
                        <p className="text-gray-500 mt-2">Your holdings are now synced. Redirecting...</p>
                    </>
                )}

                {status === 'error' && (
                    <>
                        <AlertCircle className="mx-auto text-red-500 mb-4" size={48} />
                        <h2 className="text-2xl font-bold text-gray-800">Sync Failed</h2>
                        <p className="text-gray-500 mt-2">We couldn't link your account. Please try again.</p>
                        <button 
                            onClick={() => navigate("/dashboard")}
                            className="mt-6 px-4 py-2 bg-gray-800 text-white rounded-lg"
                        >
                            Back to Dashboard
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default BrokerCallback;