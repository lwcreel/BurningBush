import tkinter as tk
from tkinter import *
from tkinter import ttk

import bm25

#Funtions
def donothing():
    x = 0

def about():
    window = tk.Toplevel(root)
    window.title('About')
    window.iconbitmap("icon.ico")
    S = Scrollbar(window)
    T = Text(window, height=10, width=51, font=("Cambria", 10))
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """The Burning Bush (TBB) is a search engine for religious texts.\nCurrently, the religious texts included are:\n
    \nThis application was made as a project in CSCE 470: Information Storage and Retrieval. It was created by Landon Creel, Hanna\nMitschke, and Sam Stone."""
    T.insert(END, quote)

def search():
    tab=tabParent.tab(tabParent.select(), "text")
    stemmer=bm25.stemmer
    results=""
    
    if (tab == "Bible Search"):

        # get needed values from controls
        book    = bookSpinBox.get()
        chapter = chapterSpinBox.get()
        verse   = verseSpinBox.get()
        query   = bibleSearchBox.get()

        if (chapter != ""):
            chapter = chapter + ":" # add colon if they have chapter
        if (book != "" and chapter != "" and verse != ""): # if have all 3, only search for one verse
            oneVerse = True
            stemmed_query = book + " " + chapter + verse
            results = bm25.OneVerse(stemmed_query, "b")
            results = results[0]
        else: # regular search
            stemmed_query = bm25.StemQuery(stemmer, query, "b", book, chapter)
            results = bm25.Search(stemmer, stemmed_query, bm25.corpusB, bm25.stemmedCorpusB, 10)
        i=0
        for i in range(len(results)):
            pos = i+1
            pos = str(pos) + '.0'
            compareResultBox.insert(pos, results[i]+'\n')

    elif (tab == "Quran Search"):
        surah = surahSpinBox.get()
        ayah  = ayahSpinBox.get()
        query   = quranSearchBox.get()

        if (surah != ""):
            surah = surah + "|" # add pipe if they have chapter
        if (surah != "" and ayah != ""): # if have both, only search for one verse
            oneVerse = True
            stemmed_query = surah + ayah
            results = bm25.OneVerse(stemmed_query, "q")
            results = results[0]
        else: # regular search
            stemmed_query = bm25.StemQuery(stemmer, query, "q", "", surah)
            results = bm25.Search(stemmer, stemmed_query, bm25.corpusQ, bm25.stemmedCorpusQ, 10)
        i=0
        for i in range(len(results)):
            pos = i+1
            pos = str(pos) + '.0'
            compareResultBox.insert(pos, results[i]+'\n')
    else:
        query   = compareSearchBox.get()
        both = True
        stemmed_query = bm25.StemQuery(stemmer, query, "x", "", "")
        # if both, they can only search with the query, so do a regular search for both
        resultsB = bm25.Search(stemmer, stemmed_query, bm25.corpusB, bm25.stemmedCorpusB, 5)
        resultsQ = bm25.Search(stemmer, stemmed_query, bm25.corpusQ, bm25.stemmedCorpusQ, 5)
        results  = resultsB + resultsQ
        i=0
        for i in range(len(results)):
            pos = i+1
            pos = str(pos) + '.0'
            compareResultBox.insert(pos, results[i]+'\n')



### GUI initialization ###

# initial configs
root = tk.Tk() 
root.title('The Burning Bush')
root.iconbitmap("icon.ico")
root.geometry('460x420')
root.maxsize(460,420)
root.minsize(460,420)

# create notebook and tabs
tabParent  = ttk.Notebook(root)
bibleTab   = ttk.Frame(tabParent)
quranTab   = ttk.Frame(tabParent)
compareTab = ttk.Frame(tabParent)

# add notebook tabs to GUI
tabParent.add(bibleTab, text = "Bible Search")
tabParent.add(quranTab, text = "Quran Search")
tabParent.add(compareTab, text = "Comparison Search")
tabParent.grid()

# config toolbar
menu = Menu(root) 
root.config(menu=menu) 
helpmenu = Menu(menu, tearoff = 0) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About', command=about) 
helpmenu.add_command(label='Settings', command=about)

### build bible tab ###

# create frames for entry and results
bibleFrameTop = Frame(bibleTab).grid(row=0)
bottomFrame   = Frame(bibleTab).grid(row=1)

# add labels
Label(bibleTab, text="Bible", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(bibleTab, text="Book", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=0, sticky=W)
Label(bibleTab, text="Chapter", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=2)
Label(bibleTab, text="Verse", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=4)
Label(bibleTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)
Label(bottomFrame, text="Results", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
bookSpinBox    = tk.Spinbox(bibleTab)
bookSpinBox.grid(row=1, column=1)
chapterSpinBox = tk.Spinbox(bibleTab, width=7)
chapterSpinBox.grid(row=1, column=3)
verseSpinBox   = tk.Spinbox(bibleTab, width=7)
verseSpinBox.grid(row=1, column=4+1)
bibleSearchBox = tk.Entry(bibleTab, width=30)
bibleSearchBox.grid(row=2, column=1)
bibleResultBox = tk.Text(bottomFrame, width=60-3, height=12)
bibleResultBox.grid(row=4, sticky=W)

### build quran tab ###

# add labels
Label(quranTab, text="Quran", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(quranTab, text="Surah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=0, sticky=W)
Label(quranTab, text="Ayah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=2)
Label(quranTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
surahSpinBox   = tk.Spinbox(quranTab)
surahSpinBox.grid(row=1, column=1)
ayahSpinBox    = tk.Spinbox(quranTab, width=7)
ayahSpinBox.grid(row=1, column=3)
quranSearchBox = tk.Entry(quranTab, width=30)
quranSearchBox.grid(row=2, column=1)
quranResultBox = tk.Text(bottomFrame,width=60-3, height=12)
quranResultBox.grid(row=4, sticky=W)

### build comparison tab ###

# add labels
Label(compareTab, text="Comparison", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(compareTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
compareSearchBox = tk.Entry(compareTab, width=30)
compareSearchBox.grid(row=2, column=1)
compareResultBox = tk.Text(bottomFrame, width=60-3, height=12, wrap="word", spacing1=8)
compareResultBox.grid(row=4, sticky=W)

### build bottom frame ###
Label(bottomFrame, text="Results", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)
searchButton = tk.Button(bottomFrame, text="Search", width=7 , padx=7, command=search)
searchButton.grid(row=2, sticky=E)

# run code
root.mainloop()
