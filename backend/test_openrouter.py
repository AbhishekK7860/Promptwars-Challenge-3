import asyncio
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.abspath("."))

from app.services.gemini_service import generate_insights_gemini, GeminiUnavailableError
from app.core.config import get_settings
from dotenv import load_dotenv

load_dotenv()

async def test_openrouter():
    settings = get_settings()
    print(f"USE_OPENROUTER: {settings.USE_OPENROUTER}")
    print(f"USE_GEMINI: {settings.USE_GEMINI}")
    print(f"OPENROUTER_API_KEY: {settings.OPENROUTER_API_KEY[:5]}...")
    
    ranked = [{"category": "transport", "kg": 3000, "percentage": 40}]
    breakdown = {"transport_km_car_petrol": 10000}
    
    try:
        insights = await generate_insights_gemini(
            ranked_categories=ranked,
            breakdown=breakdown,
            total_kg=5000
        )
        print("Success!")
        for insight in insights:
            print(f"- {insight.category}: {insight.action} (Save {insight.estimated_saving_kg}kg)")
    except Exception as e:
        print(f"Failed: {type(e).__name__} - {e}")
        import httpx
        if isinstance(e.__cause__, httpx.HTTPStatusError):
            print("Response:", e.__cause__.response.text)

if __name__ == "__main__":
    asyncio.run(test_openrouter())
