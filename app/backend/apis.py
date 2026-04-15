@app.get("/broker/kite/callback")
async def kite_callback(request_token: str, user_id: str, client_type: str = "web"):
    """API to handle Kite Connect callback.
    
    Args:
        request_token: OAuth request token from Kite
        user_id: User ID for callback
        client_type: "mobile" for deep linking, "web" for JSON response
    """
    try:
        kite = Container.get().get_kite_client.get_client()
        data = kite.generate_session(request_token,
                                     api_secret=os.getenv("KITE_API_SECRET"))
        kite.set_access_token(data["access_token"])
        broker_service = Container.get().get_broker_service_provider
        broker_service.set_access_token(data["access_token"])
        holdings = broker_service.get_holdings()
        
        portfolio_service = PortfolioService(holdings, True)
        portfolio_data = {
            "portfolio": {
                "summary": portfolio_service.get_summary(),
                "top_holdings": portfolio_service.get_top_holdings(),
                "diversification_score": portfolio_service.get_diversification_score(),
                "worst_performing_stocks": portfolio_service.get_worst_performer(),
                "best_performing_stocks": portfolio_service.get_best_performer(),
                "stocks": portfolio_service.get_stock_breakdown(),
            }
        }
        store_portfolio_analysis(portfolio_data, user_id)
        
        request_id = uuid.uuid4().hex
        portfolio_analysis_queue_data = {
            "user_id": user_id,
            "request_id": request_id,
            "pushed_at": datetime.now(
                timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "portfolio": {
                "summary": portfolio_service.get_summary(),
                "top_holdings": portfolio_service.get_top_holdings(),
                "diversification_score": portfolio_service.get_diversification_score(),
                "worst_performing_stocks": portfolio_service.get_worst_performer(),
                "best_performing_stocks": portfolio_service.get_best_performer(),
                "sector_allocation": portfolio_service.get_sector_allocation(),
            },
        }
        Container.get().get_portfolio_analysis_queue.push(
            json.dumps(portfolio_analysis_queue_data)
        )
        
        if client_type.lower() == "mobile":
            return RedirectResponse(
                url=f"finly://broker-sync?request_token={request_token}&status=success"
            )
        else:
            return {
                "status": "success",
                "message": "Kite Connect login successful and portfolio analysis started.",
                "request_id": request_id,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process callback")
