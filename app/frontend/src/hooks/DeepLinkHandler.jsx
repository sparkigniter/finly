import { useEffect } from 'react';
import { App } from '@capacitor/app';
import { useNavigate } from 'react-router-dom';

/**
 * DeepLinkHandler - Standalone Navigation Component
 * This component listens for custom URI schemes (finly://) and 
 * routes the user to the appropriate internal page.
 * * Usage: Place this inside your <BrowserRouter> in App.jsx
 */
export const DeepLinkHandler = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // 1. Handle app launches from a deep link (Cold Start)
        // If the app was closed and opened via a link, this catches the initial URL.
        App.getLaunchUrl().then((launchUrl) => {
            if (launchUrl?.url) {
                handleUrl(launchUrl.url);
            }
        });

        // 2. Handle app wake-ups from background (Warm Start)
        // If the app was already open in the background, this listener fires.
        const listener = App.addListener('appUrlOpen', (event) => {
            handleUrl(event.url);
        });

        /**
         * URL Parser and Router
         * Supports: finly://broker-sync?request_token=...&status=success
         */
        const handleUrl = (urlString) => {
            try {
                const url = new URL(urlString);
                
                // Parse the path (supports finly://path or finly://host/path variations)
                const path = url.host || url.pathname.replace(/^\/\//, ''); 
                
                if (path === 'broker-sync') {
                    const requestToken = url.searchParams.get('request_token');
                    const status = url.searchParams.get('status');

                    if (status === 'success' && requestToken) {
                        const userId = url.searchParams.get('user_id') || 'me';
                        
                        // Execute navigation to the callback processing page
                        navigate(`/broker-callback?request_token=${requestToken}&user_id=${userId}`);
                    } else {
                        console.warn("Deep Link: Received non-success status or missing token", status);
                    }
                }
            } catch (err) {
                console.error("Deep Link: Critical parsing failure", err);
            }
        };

        return () => {
            // Clean up listener on unmount to prevent multiple route triggers
            listener.remove();
        };
    }, [navigate]);

    // This component handles logic only and renders nothing to the UI
    return null;
};

export default DeepLinkHandler;