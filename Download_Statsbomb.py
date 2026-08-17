import os
import requests
import time
from requests.exceptions import ChunkedEncodingError

def download_with_retry(url, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except (ChunkedEncodingError, requests.exceptions.RequestException) as e:
            print(f"Retry {attempt + 1} failed: {e}")
            time.sleep(delay)
    print(f"Failed after {max_retries} attempts: {url}")
    return None

# Define the tournaments with their competition and season IDs
tournaments = {
    'euro2022': {'competition_id': 53, 'season_id': 106},
    'wwc2023': {'competition_id': 72, 'season_id': 107}
}

base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

for name, ids in tournaments.items():
    comp_id = ids['competition_id']
    season_id = ids['season_id']
    # Create subdirectories for this tournament
    os.makedirs(os.path.join('data', name, 'events'), exist_ok=True)
    os.makedirs(os.path.join('data', name, 'lineups'), exist_ok=True)
    os.makedirs(os.path.join('data', name, 'three-sixty'), exist_ok=True)
    # URL for the list of matches
    matches_url = f"{base_url}/matches/{comp_id}/{season_id}.json"
    try:
        resp = requests.get(matches_url)
        resp.raise_for_status()
        matches = resp.json()
    except Exception as e:
        print(f"Error fetching match list for {name}: {e}")
        continue

    for match in matches:
        match_id = match['match_id']
        # Download and save events data
        events_url = f"{base_url}/events/{match_id}.json"
        try:
            resp = requests.get(events_url)
            resp.raise_for_status()
            with open(os.path.join(name, 'events', f"{match_id}.json"), 'wb') as f:
                f.write(resp.content)
        except Exception as e:
            print(f"Failed to download events for match {match_id}: {e}")
        # Download and save lineups data
        lineups_url = f"{base_url}/lineups/{match_id}.json"
        try:
            resp = requests.get(lineups_url)
            resp.raise_for_status()
            with open(os.path.join(name, 'lineups', f"{match_id}.json"), 'wb') as f:
                f.write(resp.content)
        except Exception as e:
            print(f"Failed to download lineups for match {match_id}: {e}")
        # Download and save 360 data if available
        three_sixty_url = f"{base_url}/three-sixty/{match_id}.json"
        resp = download_with_retry(three_sixty_url)
        if resp and resp.status_code == 200:
            try:
                with open(os.path.join(name, 'three-sixty', f"{match_id}.json"), 'wb') as f:
                    f.write(resp.content)
            except Exception as e:
                print(f"Failed to save 360 data for match {match_id}: {e}")

