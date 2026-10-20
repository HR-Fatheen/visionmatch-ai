import json
import time
from pathlib import Path

import requests

ROOT = Path("data/images")
ATTRIBUTION_FILE = Path("data/image_sources.json")

CATEGORIES = {
    "wildlife": ["red fox animal", "gray wolf animal", "tiger wildlife", "eagle bird", "deer animal",
                 "red panda animal", "lion wildlife", "penguin bird", "elephant wildlife", "owl bird"],
    "technology": ["computer laptop", "robot technology", "circuit board", "computer server",
                   "smartphone device", "3d printer", "drone technology", "keyboard computer",
                   "computer motherboard", "robot arm"],
    "food": ["pizza food", "hamburger food", "pasta dish", "sushi food", "fresh salad",
             "bread loaf", "pancakes food", "fruit bowl", "soup bowl", "chocolate cake"],
    "sports": ["football soccer ball", "basketball sport", "tennis racket", "cricket sport",
               "badminton racket", "swimming sport", "cycling sport", "baseball sport",
               "volleyball sport", "athletics running"],
}

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "VisionMatchAI/1.0 (educational capstone project)"}
sources = []
session = requests.Session()
session.headers.update(HEADERS)


def search_images(query):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": 640,
        "format": "json",
    }
    response = session.get(API, params=params, timeout=30)
    response.raise_for_status()
    pages = response.json().get("query", {}).get("pages", {})
    return list(pages.values())


for category, queries in CATEGORIES.items():
    folder = ROOT / category
    folder.mkdir(parents=True, exist_ok=True)
    count = len(list(folder.glob("*.jpg"))) + len(list(folder.glob("*.png")))

    for query in queries:
        if count >= 10:
            break

        try:
            pages = search_images(query)
        except Exception as exc:
            print(f"Search failed for {query}: {exc}")
            continue

        for page in pages:
            if count >= 10:
                break

            info_list = page.get("imageinfo", [])
            if not info_list:
                continue

            info = info_list[0]
            url = info.get("thumburl") or info.get("url", "")
            if not url.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png")):
                continue

            metadata = info.get("extmetadata", {})
            license_name = metadata.get("LicenseShortName", {}).get("value", "")
            if not license_name:
                continue

            filename = f"{category}_{count + 1:02d}.jpg"
            destination = folder / filename

            try:
                image_response = session.get(url, timeout=45)
                image_response.raise_for_status()

                content_type = image_response.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    continue

                if len(image_response.content) < 5000:
                    continue

                # Keep the correct extension for PNG files.
                if "png" in content_type.lower():
                    destination = destination.with_suffix(".png")

                destination.write_bytes(image_response.content)

                sources.append({
                    "filename": str(destination).replace("\\", "/"),
                    "category": category,
                    "query": query,
                    "title": page.get("title", ""),
                    "source_page": info.get("descriptionurl", ""),
                    "image_url": url,
                    "license": license_name,
                    "license_url": metadata.get("LicenseUrl", {}).get("value", ""),
                    "artist": metadata.get("Artist", {}).get("value", ""),
                    "credit": metadata.get("Credit", {}).get("value", ""),
                })

                count += 1
                print(f"Downloaded [{category}] {destination.name}")
                time.sleep(0.2)

            except Exception as exc:
                print(f"Download failed for {page.get('title')}: {exc}")

    print(f"{category}: {count} images")

ATTRIBUTION_FILE.parent.mkdir(parents=True, exist_ok=True)
ATTRIBUTION_FILE.write_text(
    json.dumps(sources, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(f"\nDownloaded {len(sources)} images total.")
print(f"Source/licensing metadata saved to {ATTRIBUTION_FILE}.")
