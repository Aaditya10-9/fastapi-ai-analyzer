from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup

app = FastAPI(title="AI Content Analyzer API")

class URLInput(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Analyzer API"}

@app.post("/scrape")
async def scrape_url(input: URLInput):
    """
    Scrapes a URL and extracts the title and text content.
    In production, this can be connected to an LLM API for summarization.
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(input.url, follow_redirects=True)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            
            # Extract paragraphs
            paragraphs = [p.get_text() for p in soup.find_all('p')[:5]]
            content = " ".join(paragraphs)[:500]  # Limit to 500 chars
            
            return {
                "status": "success",
                "title": title,
                "content_preview": content,
                "word_count": len(content.split())
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
