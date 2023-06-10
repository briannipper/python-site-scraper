import os
import json
import sys
from types import SimpleNamespace
from urllib.parse import urlparse
import requests

settings_loc = input("Enter settings file: ")

if not os.path.exists(settings_loc):
    sys.exit(f"Settings file not found: {settings_loc}")
else:
    with open(settings_loc, "r") as settings_file:
        settings = json.loads(settings_file.read(), object_hook=lambda d: SimpleNamespace(**d))
        settings_file.close()

if not settings.protocol and settings.domain:
    sys.exit(f"Malformed JSON: {settings}")
else:
    url = f"{settings.protocol}://{settings.domain}"

try:
    urlparse(url)
except:
    sys.exit(f"Failed to parse URL: {url}")
else:
    print(f"Successfully parsed URL: {url}")
    r = requests.get(url)
    url_content = r.content

if url_content and settings.target_folder:
    if not os.path.exists(settings.target_folder):
        os.makedirs(settings.target_folder)
    with open(os.path.join(settings.target_folder, "index.html"), "wb") as write_file:
        write_file.write(url_content)
        write_file.close()
