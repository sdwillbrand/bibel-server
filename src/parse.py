import re

with open("../data/memorize.txt", "r", encoding="utf8") as file:
    memo = file.read()
with open("../data/export.csv", "r", encoding="utf8") as file:
    bible = file.read().split("\n")

verse_regex = "[a-zA-Z].{2,5}. [0-9]*,[0-9]*"
tag_regex = "([a-zA-Z ] *)+"

verses = memo.split("\n")
for verse in verses:
    verse = verse.strip()
    if re.fullmatch(verse_regex, verse):
        result = [b for b in bible if b.startswith(f"{verse}|")]
        if result == []:
            print(verse)
        else:
            print(result)
    elif re.fullmatch(tag_regex, verse):
        tag = verse.replace(" ", "_")
        print(tag)
