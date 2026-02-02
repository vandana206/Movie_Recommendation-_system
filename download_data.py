import requests
import os

def download_file(url, filename):
    print(f"Downloading {filename}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")

if __name__ == "__main__":
    movies_url = "https://raw.githubusercontent.com/vamshi121/TMDB-5000-Movie-Dataset/main/tmdb_5000_movies.csv"
    extract_path = "tmdb_5000_movies.csv"
    
    if not os.path.exists(extract_path):
        download_file(movies_url, extract_path)
    else:
        print(f"{extract_path} already exists.")
