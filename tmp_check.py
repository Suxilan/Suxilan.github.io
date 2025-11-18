import pathlib

root = pathlib.Path("content")

for path in root.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    text = text.replace("\\$", "")
    text = text.replace("$$", "")
    count = text.count("$")
    if count % 2 != 0:
        print("Odd $ count", count, path)

