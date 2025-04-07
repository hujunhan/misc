import pandas as pd
import requests
import time
import re

# Load your existing file
df = pd.read_csv("/Users/hu/Downloads/vinyl_with_authors.csv")
df["Title"] = df["Title"].astype(str).str.strip()


# Define MusicBrainz search function
def search_musicbrainz(title_query):
    url = "https://musicbrainz.org/ws/2/release/"
    params = {
        "query": f'release:"{title_query}"',
        "fmt": "json",
    }
    headers = {"User-Agent": "VinylAlbumFixer/1.0 (your_email@example.com)"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        releases = data.get("releases", [])
        if releases:
            artist_credit = releases[0].get("artist-credit", [])
            if artist_credit:
                return artist_credit[0].get("name")
    except Exception as e:
        print(f"Error searching for '{title_query}': {e}")

    return None


# Clean the title for alternative searches
def clean_title(title):
    return re.sub(r"[^\w\s]", "", title)  # Remove punctuation


# Main processing loop
for idx, row in df.iterrows():
    if pd.notna(row["Author"]) and row["Author"].strip():
        continue  # Already filled, skip

    original_title = row["Title"]
    cleaned_title = clean_title(original_title)
    keywords = " ".join(original_title.split()[:3])  # First 3 words

    print(f"Searching for: {original_title}")

    author = (
        search_musicbrainz(original_title)
        or search_musicbrainz(cleaned_title)
        or search_musicbrainz(keywords)
    )

    if author:
        df.at[idx, "Author"] = author
        print(f"✓ Found: {original_title} → {author}")
    else:
        print(f"✗ Not found: {original_title}")

    time.sleep(1)  # Rate limit

# Save the result
df.to_csv("vinyl_with_authors_updated.csv", index=False)
print("🎉 Done! Saved as vinyl_with_authors_updated.csv")
