import re

with open("../data/memorize.txt", "r", encoding="utf8") as file:
    memo = file.read()
with open("../data/export.csv", "r", encoding="utf8") as file:
    bible = file.read().split("\n")

verse_regex = "([0-9]. )?[a-zA-Z].{1,5}. [0-9]*,[0-9]*"
tag_regex = "([a-zA-Z ] *)+"

verses = memo.split("\n")
export = ""
for verse in verses:
    verse = verse.strip()
    if re.fullmatch(verse_regex, verse):
        for (i, content) in enumerate(bible):
            if content.startswith(f"{verse}|"):
                bible[i] = f"{content} {tag}"
    elif re.fullmatch(tag_regex, verse):
        tag = verse.replace(" ", "_")

with open("../data/export-tags.csv", "x", encoding="utf8") as file:
    file.write("\n".join(bible))