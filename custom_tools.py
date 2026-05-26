from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool("search_tool")
def search_tool(query: str) -> str:
    """Search the web for information on a given topic."""
    from logger import log_progress
    log_progress(f"DEBUG: search_tool called with query: {query}")
    print(f"DEBUG: search_tool called with query: {query}")
    try:
        runner = DuckDuckGoSearchRun()
        result = runner.run(query)
        log_progress(f"DEBUG: search_tool returned {len(result)} characters")
        print(f"DEBUG: search_tool returned {len(result)} characters")
        return result
    except Exception as e:
        log_progress(f"DEBUG: search_tool error: {e}")
        print(f"DEBUG: search_tool error: {e}")
        return f"Error searching: {e}"
