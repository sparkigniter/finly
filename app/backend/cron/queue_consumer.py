import sys
import asyncio
from dotenv import load_dotenv
from app.backend.queues.protfolio_analyse import ProtfolioAnalyseQueue
from app.backend.services.container import container
load_dotenv()

async def run_batch(queue_name: str):
    """Handles the routing of different queue jobs."""
    match queue_name:
        case ProtfolioAnalyseQueue.JOB_NAME:
            # We 'await' here because consume() is an async function
            await container.protfolio_analysis_queue.consume()
        case _:
            print(f"Unknown queue: {queue_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.backend.cron.queue_consumer <queue_name>")
        sys.exit(1)
    
    target_queue = sys.argv[1]
    
    # Start the engine ONCE for the entire batch
    asyncio.run(run_batch(target_queue))