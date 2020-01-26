# open files for reading
bible = open("Docs/StemmedBible.txt", "r")
quran = open("Docs/StemmedQuran.txt", "r")

# read information into string
bibleText = bible.read()
quranText = quran.read()

# split on spaces and push into 2D list
documents = []
documents.append(bibleText.split(" "))
documents.append(quranText.split(" "))

