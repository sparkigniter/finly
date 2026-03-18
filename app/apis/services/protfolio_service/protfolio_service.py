import json
from app.ai.google_vertex.workflows.finadvisory_orchestrator import FinAdvisorOrchestrator

class ProtfolioService: 

    async def analyse(self, data: dict):
        try:  
            batch_size = 30
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                print(f"Processing batch: {batch}")
                await FinAdvisorOrchestrator.analyze_portfolio(
                    user_id="test",
                    file_content=json.dumps(batch))

                return {
                    "status": "success",
                }
        except Exception as e:
            raise e
