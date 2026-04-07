import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Capacitor } from '@capacitor/core';

/**
 * DeepLinkHandler - Standalone Navigation Component
 * This component listens for custom URI schemes (finly://) and 
 * routes the user to the appropriate internal page.
 */
export const DeepLinkHandler = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Senior DevOps Note: Only initialize native listeners if running on a native platform
        // This prevents Vite/Rolldown errors during web-only development.
        if (!Capacitor.isNativePlatform()) {
            return;
        }

        // Dynamically import to further isolate native code from web bundler if needed
        // but a standard import usually works once the package is installed.
        const initNativeListeners = async () => {
            const { App } = await import('@capacitor/app');

            // 1. Handle app launches from a deep link (Cold Start)
            App.getLaunchUrl().then((launchUrl) => {
                if (launchUrl?.url) {
                    handleUrl(launchUrl.url);
                }
            });

            // 2. Handle app wake-ups from background (Warm Start)
            const listener = await App.addListener('appUrlOpen', (event) => {
                handleUrl(event.url);
            });

            return listener;
        };

        let nativeListener;
        initNativeListeners().then(l => nativeListener = l);

        /**
         * URL Parser and Router
         * Supports: finly://broker-sync?request_token=...&status=success
         */
        const handleUrl = (urlString) => {
            try {
                const url = new URL(urlString);
                const path = url.host || url.pathname.replace(/^\/\//, ''); 
                
                if (path === 'broker-sync') {
                    const requestToken = url.searchParams.get('request_token');
                    const status = url.searchParams.get('status');

                    if (status === 'success' && requestToken) {
                        const userId = url.searchParams.get('user_id') || 'me';
                        navigate(`/broker-callback?request_token=${requestToken}&user_id=${userId}`);
                    }
                }
            } catch (err) {
                console.error("Deep Link: Critical parsing failure", err);
            }
        };

        return () => {
            if (nativeListener) {
                nativeListener.remove();
            }
        };
    }, [navigate]);

    return null;
};

export default DeepLinkHandler;