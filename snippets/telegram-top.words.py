"""
Count top 30 unique words said by every user in a Telegram chat.

Usage:

    1. "Export chat history" from the desktop client.
    2. Open "ChatExport*" directory.
    3. Run the script from the directory.
"""

from pathlib import Path
from collections import defaultdict, Counter
from lxml import html
import re


rex = re.compile(r'\W+')
counters = defaultdict(Counter)

for path in Path().glob("*.html"):
    tree = html.fromstring(open('messages.html').read())
    user = ''
    for msg in tree.xpath('//div[@class="body"]'):
        divs = msg.xpath('div[@class="from_name"]')
        if divs:
            user = divs[0].text.strip() or user
        divs = msg.xpath('div[@class="text"]')
        if not divs:
            continue
        msg = divs[0].text.strip()
        # print(user, msg)
        words = msg.lower().split()
        words = [rex.sub('', word) for word in words]
        counters[user].update(Counter(words))


COUNT = 30


all_top_words = defaultdict(int)
for counter in counters.values():
    for word, _ in counter.most_common(COUNT):
        all_top_words[word] += 1

top_words = dict()
for name, counter in counters.items():
    top_words[name] = []
    for word, _ in counter.most_common(COUNT):
        if all_top_words[word] == 1:
            top_words[name].append(word)

for name, words in sorted(top_words.items()):
    print(name + ':', ', '.join(words))
