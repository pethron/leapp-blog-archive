# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Archive a whole Hashnode blog as Markdown, with images downloaded locally.

Reads the blog sitemap, then for each post saves
  posts/<YYYY-MM-DD>-<slug>/index.md   (front matter + original Markdown)
  posts/<YYYY-MM-DD>-<slug>/images/    (cover + inline images)
and regenerates the index in README.md.

Usage: uv run scripts/archive.py [--force] [--host blog.leapp.cloud]
"""

import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "posts"
sys.stdout.reconfigure(encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (blog-archive)"}
IMG_RE = re.compile(r'!\[([^\]]*)\]\((https?://[^\s)]+)(?:\s+[^)]*)?\)')
SKIP = ("/series/", "/tag/", "/archive", "/recommendations", "/newsletter", "/members")
INDEX_START, INDEX_END = "<!-- index:start -->", "<!-- index:end -->"


def get(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def post_urls(host: str) -> list[str]:
    xml = get(f"https://{host}/sitemap.xml").decode("utf-8")
    urls = re.findall(r"<loc>(.*?)</loc>", xml)
    return [u for u in urls if urlparse(u).path.strip("/") and not any(s in u for s in SKIP)]


def metadata(url: str) -> dict:
    html = get(url).decode("utf-8")
    meta = {}
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        data = json.loads(block)
        if data.get("@type") == "BlogPosting":
            meta = data
        elif data.get("@type") == "BreadcrumbList":
            meta["_tags"] = [
                i["name"].lstrip("#") for i in data["itemListElement"] if "/tag/" in i.get("item", "")
            ]
    date = re.search(r'<meta property="article:published_time" content="([^"]+)"', html)
    cover = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    author = meta.get("author") or {}
    if isinstance(author, list):
        author = author[0] if author else {}
    return {
        "title": meta.get("headline", ""),
        "author": author.get("name", ""),
        "date": (meta.get("datePublished") or (date.group(1) if date else ""))[:10],
        "description": meta.get("description", ""),
        "tags": meta.get("_tags", []),
        "cover": cover.group(1) if cover else "",
    }


def download(src: str, folder: Path, fallback: str) -> str | None:
    name = re.sub(r'[<>:"/\\|?*]', "_", Path(urlparse(src).path).name) or fallback
    if len(name) > 80:  # e.g. googleusercontent URLs: too long for Windows paths
        name = hashlib.sha1(src.encode()).hexdigest()[:16] + Path(name).suffix[:5]
    target = folder / "images" / name
    if not target.exists():
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(get(src))
        except Exception as e:
            print(f"  ! image failed {src}: {e}")
            return None
    return f"images/{name}"


def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def archive(url: str, force: bool) -> dict:
    slug = urlparse(url).path.strip("/").split("/")[-1]
    existing = next(POSTS.glob(f"*-{slug}/index.md"), None) if POSTS.exists() else None
    if existing and not force:
        print(f"= exists    {slug}")
        return read_front(existing)

    meta = metadata(url)
    markdown = get(url.rstrip("/") + ".md").decode("utf-8")
    folder = POSTS / f"{meta['date'] or 'undated'}-{slug}"
    folder.mkdir(parents=True, exist_ok=True)

    def localize(m: re.Match) -> str:
        local = download(m.group(2), folder, "image")
        return f"![{m.group(1)}]({local or m.group(2)})"

    body = IMG_RE.sub(localize, markdown)
    # Hashnode embeds (%[url]) are not rendered on GitHub: turn them into plain links
    body = re.sub(r"^%\[(\S+?)\]\s*$", r"[\1](\1)", body, flags=re.M)
    cover = download(meta["cover"], folder, "cover") if meta["cover"] else None
    front = [
        "---",
        f"title: {yaml_str(meta['title'] or slug)}",
        f"author: {yaml_str(meta['author'])}",
        f"date: {meta['date']}",
        f"tags: [{', '.join(yaml_str(t) for t in meta['tags'])}]",
        f"description: {yaml_str(meta['description'])}",
        f"cover: {cover or ''}",
        f"original_url: {url}",
        "---",
        "",
    ]
    (folder / "index.md").write_text("\n".join(front) + "\n" + body, encoding="utf-8")
    print(f"✓ archived  {folder.name}  ({meta['author']})")
    return {**meta, "path": f"posts/{folder.name}/index.md"}


def read_front(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").split("---", 2)[1]
    data = {}
    for line in text.strip().splitlines():
        key, _, value = line.partition(": ")
        value = value.strip()
        data[key] = json.loads(value) if value.startswith('"') else value
    data["path"] = path.relative_to(ROOT).as_posix()
    return data


def write_index(posts: list[dict]) -> None:
    rows = ["| Date | Title | Author |", "|------|-------|--------|"]
    for p in sorted(posts, key=lambda p: p.get("date", ""), reverse=True):
        title = p.get("title", "").replace("|", "\\|")
        rows.append(f"| {p.get('date', '')} | [{title}]({p['path']}) | {p.get('author', '')} |")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = text.index(INDEX_START) + len(INDEX_START), text.index(INDEX_END)
    readme.write_text(text[:start] + "\n" + "\n".join(rows) + "\n" + text[end:], encoding="utf-8")


def main() -> int:
    force = "--force" in sys.argv
    host = sys.argv[sys.argv.index("--host") + 1] if "--host" in sys.argv else "blog.leapp.cloud"
    posts, failed = [], 0
    for url in post_urls(host):
        try:
            posts.append(archive(url, force))
        except Exception as e:
            print(f"✗ failed    {url}: {e}")
            failed += 1
    write_index(posts)
    print(f"\n{len(posts)} posts archived, {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
