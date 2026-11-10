#print("sameer is a millionaire and one of the worlds best entrepreneurs")

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    search the web for recent and relavable information about the query and return title, url and snippet of the top 3 results
    """
    results = tavily_client.search(query=query, max_results=3)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\n URL: {r['url']}\n Snippet: {r['content'][:3000]}\n "
        )
    return "\n---\n".join(out)


#print(web_search.invoke("latest news about AI advancements in 2027"))

@tool
def Scrape_url(url: str)-> str:
    """ Scrape and return clean text content from agiven URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=16, headers={"user-agent": "Moxilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]
    except Exception as e:
        return f"could not scrape URL: {str(e)}"

#print( Scrape_url.invoke("https://ai2027-tracker.com/changelog"))
