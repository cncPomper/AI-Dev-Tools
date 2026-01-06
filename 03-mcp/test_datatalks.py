import requests

def download_web_content(url: str) -> str:
    """Download the content of any web page as markdown using Jina reader."""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error downloading content: {str(e)}"

def count_word_occurrences(text: str, word: str) -> int:
    """Count how many times a word appears in a given text (case-insensitive)."""
    return text.lower().count(word.lower())

# Step 1: Download content from datatalks.club
url = "https://datatalks.club/"
print(f"Downloading content from {url}...")
content = download_web_content(url)

if content.startswith("Error"):
    print(content)
else:
    # Step 2: Count occurrences of "data"
    word = "data"
    count = count_word_occurrences(content, word)
    
    print(f"\n✅ Successfully downloaded content from {url}")
    print(f"Total characters: {len(content)}")
    print(f"\n📊 Word count result:")
    print(f"The word '{word}' appears {count} times on the page.")
    print(f"\nFirst 1000 characters of content:")
    print(content[:1000])