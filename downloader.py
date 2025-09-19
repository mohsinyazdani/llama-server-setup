"""
Download Module
Handles downloading of LLama server releases and files
"""
import requests
import os


def get_latest_release(github_api_url):
    print("Fetching latest release information...")
    
    try:
        response = requests.get(github_api_url, timeout=15)
        response.raise_for_status()
        release = response.json()
        
        print(f"Found release: {release['tag_name']}")
        print(f"Published: {release['published_at'][:10]}")
        return release

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch release info: {e}")
        return None


def find_matching_asset(release, pattern):
    print(f"Looking for asset matching: {pattern}")
    
    matching_assets = []
    for asset in release['assets']:
        if pattern in asset['name'].lower():
            matching_assets.append(asset)
    
    if not matching_assets:
        print(f"No assets found matching '{pattern}'")
        print("\nAvailable assets:")
        for asset in release['assets']:
            if asset['name'].endswith('.zip'):
                size_mb = asset['size'] / (1024 * 1024)
                print(f"   {asset['name']} ({size_mb:.1f} MB)")
        return None

    asset = matching_assets[0]
    size_mb = asset['size'] / (1024 * 1024)
    print(f"Found: {asset['name']} ({size_mb:.1f} MB)")
    return asset


def download_with_progress(url, filename):
    print(f"Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        bar_length = 30
                        filled_length = int(bar_length * downloaded // total_size)
                        bar = '█' * filled_length + '-' * (bar_length - filled_length)
                        print(f"\r[{bar}] {percent:.1f}%", end="", flush=True)

        print(f"\nDownloaded successfully!")
        return True

    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False
