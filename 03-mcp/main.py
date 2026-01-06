from fastmcp import FastMCP # type: ignore
import requests # type: ignore

mcp = FastMCP("AI Dev Tools 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def download_web_content(url: str) -> str:
    """Download the content of any web page as markdown using Jina reader.
    
    Args:
        url: The URL of the web page to download
        
    Returns:
        The content of the web page in markdown format
    """
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error downloading content: {str(e)}"

@mcp.tool
def count_word_occurrences(text: str, word: str) -> int:
    """Count how many times a word appears in a given text (case-insensitive).
    
    Args:
        text: The text to search in
        word: The word to count
        
    Returns:
        The number of times the word appears in the text
    """
    return text.lower().count(word.lower())

if __name__ == "__main__":
    mcp.run()