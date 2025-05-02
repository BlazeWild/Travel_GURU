import os

from exa_py import Exa
from langchain_core.tools import tool

exa = Exa(apikey=os.getenv("EXA_API_KEY"))

@tool
def search_and_contents(query: str):
    """Search for webpages based on the query and retrieve their contents"""
    #this combines two AOU endpoints: search and contents retrieval
    return exa.search_web_contents(query,
                                   use_autoprompt=True,
                                   num_results=5,
                                   text=True,
                                   highlights=True,
                                   )
    
@tool
def find_similar_and_contents(url:str):
    """Search for webpages similr to the given url and retrieve their contents
    The url passed in should be a URL returned from 'search_and_contents'
    """
    #this combined two API endpoints: find_similar and contents retrieval
    return exa.find_similar_web_contents(url,
                                         num_results=5, 
                                         text=True,
                                         highlights=True,
            )


tools = [search_and_contents, find_similar_and_contents]
