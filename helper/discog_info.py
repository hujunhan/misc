import pandas as pd
import requests
import time
import time


def rate_limited_get(url, params=None):
    while True:
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)

            # Retry on server error or empty body
            if r.status_code >= 500 or not r.text.strip():
                print(
                    f"⚠️ Server error or empty response from {url}. Retrying in 10s..."
                )
                time.sleep(10)
                continue

            remaining = int(r.headers.get("X-Discogs-Ratelimit-Remaining", 60))
            used = int(r.headers.get("X-Discogs-Ratelimit-Used", 0))

            if remaining <= 1:
                print(
                    f"⚠️ Rate limit nearly exceeded. Used: {used}, Remaining: {remaining}. Waiting 60s..."
                )
                time.sleep(60)

            return r
        except Exception as e:
            print(f"🌐 Connection error: {e}. Retrying in 10s...")
            time.sleep(10)


DISCOGS_TOKEN = "uMpfmDzvqDkMHorXPAjGzcsXVeWVlVbQUGVmkUtr"
HEADERS = {"User-Agent": "VinylScorer/4.0"}

# Load your vinyl list
df = pd.read_csv("vinyl_with_discogs_scores.csv")

# Ensure columns exist
for col in [
    "Rating",
    "Rating Count",
    "Community Have",
    "Community Want",
    "Year",
    "Genres",
]:
    if col not in df.columns:
        df[col] = None


def fetch_release_info(resource_url):
    try:
        r = rate_limited_get(resource_url)
        if r.status_code != 200:
            print(f"⚠️ HTTP {r.status_code} for {resource_url}")
            print("Response content preview:", r.text[:200])
            return {}

        try:
            data = r.json()
        except ValueError:
            print(f"❌ Invalid JSON from {resource_url}")
            print("Response content preview:", r.text[:200])
            return {}

        rating_info = data.get("community", {}).get("rating", {})
        return {
            "rating": rating_info.get("average"),
            "rating_count": rating_info.get("count"),
            "have": data.get("community", {}).get("have"),
            "want": data.get("community", {}).get("want"),
            "year": data.get("year"),
            "genres": ", ".join(data.get("genres", [])) if "genres" in data else None,
        }

    except Exception as e:
        print(f"Exception while fetching release info: {e}")
        return {}


def search_best_release(title, artist=None):
    url = "https://api.discogs.com/database/search"
    params = {
        "token": DISCOGS_TOKEN,
        "type": "release",
        "release_title": title,
        "per_page": 5,
    }
    if artist:
        params["artist"] = artist

    try:
        r = rate_limited_get(url, params)

        data = r.json()
        results = data.get("results", [])
        if not results:
            return None

        # Find the release with the highest rating count
        best_info = None
        best_count = -1
        for result in results:
            resource_url = result.get("resource_url")
            if not resource_url:
                continue
            info = fetch_release_info(resource_url)
            if (
                info
                and info["rating_count"] is not None
                and info["rating_count"] > best_count
            ):
                best_info = info
                best_count = info["rating_count"]
        return best_info
    except Exception as e:
        print(f"Search failed for '{title}' by '{artist}': {e}")
        return None


# Process the list
for idx, row in df.iterrows():
    if pd.notna(row["Rating"]):
        continue  # Already has data

    title = row["Title"]
    artist = row["Author"]
    print(f"Searching for: {title} by {artist}")

    info = search_best_release(title, artist)
    if not info:
        info = search_best_release(title)

    if info:
        df.at[idx, "Rating"] = info.get("rating")
        df.at[idx, "Rating Count"] = info.get("rating_count")
        df.at[idx, "Community Have"] = info.get("have")
        df.at[idx, "Community Want"] = info.get("want")
        df.at[idx, "Year"] = info.get("year")
        df.at[idx, "Genres"] = info.get("genres")
        print(
            f"✓ Best match → Rating: {info['rating']} (Count: {info['rating_count']})"
        )
        # After updating df.at[...] for each album
        df.to_csv("vinyl_with_discogs_scores_final.csv", index=False)

    else:
        print(f"✗ No release found for: {title}")

    time.sleep(1.2)  # Rate limit

# Save results
df.to_csv("vinyl_with_discogs_scores_final.csv", index=False)
print("🎉 Done! Saved as vinyl_with_discogs_scores_final.csv")
