import requests # type: ignore

def download_web_content(url: str) -> str:
    """Download the content of any web page as markdown using Jina reader."""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error downloading content: {str(e)}"

# Test the download_web_content function
url = "https://github.com/alexeygrigorev/minsearch"
content = download_web_content(url)

print(f"URL: {url}")
print(f"Number of characters: {len(content)}")
print(f"\nFirst 500 characters of content:")
print(content[:500])