import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


TARGET = "https://techsavanna.co.ke"
OUTPUT_FOLDER = "./clonedsite"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def download_file(url, folder):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status() 
        
        # Get a valid filename (with fallback if missing)
        filename = os.path.basename(urlparse(url).path)
        if not filename or filename == "/":
            filename = "index.html"  # Default filename for directories

        file_path = os.path.join(folder, filename)

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return filename
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

def clone_website(url, output_folder):
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve website.")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Download CSS, JS, and images
    for tag in soup.find_all(["link", "script", "img"]):
        attr = "href" if tag.name == "link" else "src"
        if tag.has_attr(attr):
            file_url = urljoin(url, tag[attr])
            filename = download_file(file_url, output_folder)
            if filename:
                tag[attr] = os.path.basename(filename)  # Rewrite link

    # Save the modified HTML
    with open(os.path.join(output_folder, "index.html"), "w", encoding="utf-8") as file:
        file.write(str(soup))

    print(f"Website cloned successfully to {output_folder}")

# Run the cloning function
clone_website(TARGET, OUTPUT_FOLDER)

