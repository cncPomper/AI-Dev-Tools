import os
import requests
import zipfile
from pathlib import Path
from minsearch import Index

def download_fastmcp_docs():
    """Download fastmcp documentation if not already downloaded."""
    zip_path = "fastmcp-main.zip"
    
    # Check if already downloaded
    if os.path.exists(zip_path):
        print(f"✓ {zip_path} already exists, skipping download")
        return zip_path
    
    print("Downloading fastmcp repository...")
    url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    
    print(f"✓ Downloaded {zip_path}")
    return zip_path

def extract_and_index_docs(zip_path):
    """Extract md and mdx files from zip and index them with minsearch."""
    documents = []
    
    print("Extracting and indexing documentation files...")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            # Only process .md and .mdx files
            if file_info.filename.endswith(('.md', '.mdx')):
                # Remove the first part of the path (fastmcp-main/)
                if '/' in file_info.filename:
                    clean_filename = '/'.join(file_info.filename.split('/')[1:])
                else:
                    clean_filename = file_info.filename
                
                # Skip if it's just a directory or empty filename
                if not clean_filename:
                    continue
                
                # Read the content
                content = zip_ref.read(file_info.filename).decode('utf-8')
                
                documents.append({
                    'filename': clean_filename,
                    'content': content
                })
                
                print(f"  ✓ Indexed: {clean_filename}")
    
    # Create minsearch index
    index = Index(
        text_fields=['content', 'filename'],
        keyword_fields=[]
    )
    
    # Index all documents
    index.fit(documents)
    
    print(f"\n✓ Indexed {len(documents)} documents")
    return index

def search(index, query, top_k=5):
    """Search function that retrieves top_k most relevant documents."""
    results = index.search(query, num_results=top_k)
    return results

def main():
    """Main function to test the implementation."""
    # Step 1: Download the zip file
    zip_path = download_fastmcp_docs()
    
    # Step 2: Extract and index documents
    index = extract_and_index_docs(zip_path)
    
    # Step 3: Test search with query "demo"
    print("\n" + "="*60)
    print("Testing search with query: 'demo'")
    print("="*60)
    
    results = search(index, "demo", top_k=5)
    
    print(f"\nTop 5 results for 'demo':\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['filename']}")
        print(f"   Preview: {doc['content'][:100].strip()}...")
        print()
    
    # Answer the question
    print("="*60)
    print(f"✓ First file returned: {results[0]['filename']}")
    print("="*60)

if __name__ == "__main__":
    main()