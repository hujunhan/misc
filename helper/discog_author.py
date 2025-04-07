import pandas as pd
import requests
import time

# Your personal Discogs token here
DISCOGS_TOKEN = "uMpfmDzvqDkMHorXPAjGzcsXVeWVlVbQUGVmkUtr"

# Load your CSV
df = pd.read_csv("/Users/hu/Downloads/vinyl_with_authors_updated.csv")
df["Title"] = df["Title"].astype(str).str.strip()


# Discogs search function
def search_discogs(title):
    url = "https://api.discogs.com/database/search"
    params = {"q": title, "type": "release", "token": DISCOGS_TOKEN}
    headers = {"User-Agent": "VinylAuthorFinder/1.0"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        results = data.get("results", [])
        if results:
            return results[0].get("title")  # Usually formatted like "Artist - Album"
    except Exception as e:
        print(f"Error searching Discogs for {title}: {e}")
    return None


# Extract artist name from result like "Artist - Album Title"
def extract_artist(discogs_title):
    if discogs_title and " - " in discogs_title:
        return discogs_title.split(" - ")[0].strip()
    return None


# Process missing authors
for idx, row in df.iterrows():
    if pd.notna(row["Author"]) and row["Author"].strip():
        continue

    title = row["Title"]
    print(f"Searching Discogs for: {title}")
    discogs_result = search_discogs(title)
    artist = extract_artist(discogs_result)

    if artist:
        df.at[idx, "Author"] = artist
        print(f"✓ Found: {title} → {artist}")
    else:
        print(f"✗ Not found: {title}")

    time.sleep(1)  # Stay under rate limits

# Save the result
df.to_csv("vinyl_with_authors_discogs.csv", index=False)
print("🎉 Done! Saved as vinyl_with_authors_discogs.csv")
