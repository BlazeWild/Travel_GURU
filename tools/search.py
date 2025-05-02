# search.py
import os
import asyncio
from typing import Tuple, List
from exa_py import Exa
from langchain.docstore.document import Document
from langchain.document_loaders.recursive_url_loader import FireCrawlLoader

EXA_API_KEY = os.getenv("EXA_API_KEY")
FIRECRAWL_TIMEOUT = 30
MAX_RETRIES = 3

exa = Exa(api_key=EXA_API_KEY)

def format_search_results(search_results):
    if not search_results:
        return "No results found."
    markdown_results = "### Search Results\n"
    for idx, result in enumerate(search_results.results, 1):
        title = result.title if hasattr(result, 'title') and result.title else "No title"
        url = result.url
        date = result.published_date if hasattr(result, 'published_date') else "No date"
        markdown_results += f"**{idx}.** [{title}]({url}) ({date})\n"
        summary = getattr(result, 'summary', 'No summary available.')
        markdown_results += f"Summary: {summary}\n"
    return markdown_results

async def search_web(query: str, num_results: int = 5) -> Tuple[str, List]:
    try:
        search_results = exa.search_web_contents(
            query,
            summary={"query": "Main points and key takeaways"},
            num_results=num_results
        )
        formatted = format_search_results(search_results)
        return formatted, search_results.results
    except Exception as e:
        return f"Search error: {str(e)}", []

async def get_web_content(url: str) -> List[Document]:
    for attempt in range(MAX_RETRIES):
        try:
            loader = FireCrawlLoader(url=url, mode="scrape")
            documents = await asyncio.wait_for(loader.aload(), timeout=FIRECRAWL_TIMEOUT)
            if documents:
                return documents
            await asyncio.sleep(1)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(1)
            else:
                return [Document(page_content=f"Failed to fetch from {url}: {str(e)}", metadata={"source": url})]
    return []