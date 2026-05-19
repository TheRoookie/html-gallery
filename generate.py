import os
import json
from datetime import datetime

ROOT = "."
OUTPUT = "projects.json"

IGNORE = {
    ".git",
    "assets",
    "__pycache__"
}

IMAGE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif"
]

projects = []

def find_thumbnail(folder):
    for file in os.listdir(folder):
        lower = file.lower()

        if "thumb" in lower or "preview" in lower:
            return os.path.join(folder, file).replace("\\", "/")

    for file in os.listdir(folder):
        ext = os.path.splitext(file)[1].lower()

        if ext in IMAGE_EXTENSIONS:
            return os.path.join(folder, file).replace("\\", "/")

    return None

def read_readme(folder):
    readme_path = os.path.join(folder, "README.md")

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            lines = content.splitlines()

            title = None
            description = ""

            for line in lines:
                line = line.strip()

                if line.startswith("# ") and not title:
                    title = line.replace("# ", "").strip()

                elif line and not line.startswith("#"):
                    description = line
                    break

            return {
                "title": title,
                "description": description
            }

    return {
        "title": None,
        "description": ""
    }

def get_category(path):
    parts = path.split("/")

    if len(parts) > 1:
        return parts[0]

    return "General"

def scan(directory):
    for root, dirs, files in os.walk(directory):

        dirs[:] = [d for d in dirs if d not in IGNORE]

        if "index.html" in files:

            rel_path = os.path.relpath(root, ROOT).replace("\\", "/")

            if rel_path == ".":
                continue

            readme = read_readme(root)

            thumbnail = find_thumbnail(root)

            stat = os.stat(root)

            last_updated = datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d")

            name = readme["title"] or os.path.basename(root)

            tags = [
                part.lower()
                for part in rel_path.split("/")
            ]

            projects.append({
                "name": name,
                "path": f"./{rel_path}/",
                "folder": rel_path,
                "category": get_category(rel_path),
                "description": readme["description"],
                "thumbnail": thumbnail,
                "tags": tags,
                "lastUpdated": last_updated
            })

scan(ROOT)

projects.sort(key=lambda x: x["name"].lower())

projects.sort(
    key=lambda x: x["lastUpdated"],
    reverse=True
)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(projects, f, indent=2)

print(f"Generated {OUTPUT} with {len(projects)} projects")