import re

quran = open("Docs/QuranWithSpaces.txt", "r")
quranText = quran.read()
quranText = quranText.split()

l = []
prev = "0"
prevV = ""
for word in quranText: 
    if (re.match(r"[0-9]+\|[0-9]+", word)):
        a = word.split('|')
        ch = a[0]
        verse = a[1]
        if (ch != prev):
            l.append(prevV)
            prev = ch
        prevV = verse
l.pop(0)
l.append('6')

d=dict()
i = 0
for x in range(1,115):
    d[str(x)]=int(l[i])
    i = i + 1
print(d)