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

def clear():
    # clear all entries and result box
    tab=tabParent.tab(tabParent.select(), "text")
    if (tab == "Bible Search"):
        bookSpinBox.set(" ")
        chapterSpinBox.set(" ")
        verseSpinBox.config(state = NORMAL)
        verseSpinBox.delete(0,"end")
        verseSpinBox.config(state = DISABLED)
        bibleSearchBox.delete(0,"end")
    elif (tab == "Quran Search"):
        surahSpinBox.set(" ")
        ayahSpinBox.set(" ")
        quranSearchBox.delete(0,"end")
    else:
        compareSearchBox.delete(0,"end")
    compareResultBox.config(state=NORMAL)
    compareResultBox.delete("1.0","end")
    compareResultBox.config(state=DISABLED)

def updateBible(*args):
    chapter = chapterSpinBox.get()
    book = bookSpinBox.get()
    book = (book.encode('ascii', 'ignore')).decode("utf-8")
    if (book == ' '): # lock the chapterSpinBox and verseSpinBox if there is no book
        chapterSpinBox.set(" ")
        verseSpinBox.delete(0,"end")
        chapterSpinBox.config(state=DISABLED)
        verseSpinBox.config(state=DISABLED)
    if (chapter == ' '): # lock the verseSpinBox if there is no chapter
        verseSpinBox.config(state=NORMAL)
        verseSpinBox.delete(0,"end")
        verseSpinBox.config(state=DISABLED)
    if (book != ' '): # unlock the chapterSpinBox if there is a book
        maxChapter = bookswChapter[book] # get number of chapters given book
        chapters = [" "] + list(range(1, maxChapter+1))
        chapterSpinBox.config(values=(chapters), state="readonly")
    if(book != ' ' and chapter != ' '): # unlock the verseSpinBox if there is a book and chapter
        verseSpinBox.config(state="readonly")

def updateQuran(*args):
    surah = surahSpinBox.get()
    if (surah == ' '): # lock the ayahSpinBox if there is no surah
        ayahSpinBox.set(" ")
        ayahSpinBox.config(state=DISABLED)
    elif (surah != ' '): # unlock the ayahSpinBox if there is a surah
        ayahSpinBox.config(state=NORMAL)
        ayahSpinBox.set(" ")
        maxAyah = surahswAyah[surah] # get number of ayah given surah
        ayahs = [" "] + list(range(1, maxAyah+1))
        ayahSpinBox.config(values=(ayahs), state="readonly")

def search():
    tab=tabParent.tab(tabParent.select(), "text")
    stemmer=bm25.stemmer
    results=""
    compareResultBox.config(state=NORMAL)
    compareResultBox.delete("1.0","end")

    misspelledMsg = []
    # booleans needed to check various conditions
    oneVerse = False 
    both = False
    
    if (tab == "Bible Search"):
        # get needed values from controls
        book    = bookSpinBox.get()
        book    = (book.encode('ascii', 'ignore')).decode("utf-8")
        if (book == ' '):
            book = ''
        chapter = chapterSpinBox.get()
        if (chapter == ' '):
            chapter = ''
        verse   = verseSpinBox.get()
        query   = bibleSearchBox.get()

        if(book == "" and chapter == "" and verse == "" and query == ""):
            return
        if (chapter != ""):
            chapter = chapter + ":" # add colon if they have chapter
        if (book != "" and chapter != "" and verse != ""): # if have all 3, only search for one verse
            oneVerse = True
            if (query != ""):
                tk.messagebox.showinfo("Single verse search", "Disregarding query and searching for particular verse instead.")
            stemmed_query = book + " " + chapter + verse
            results = bm25.OneVerse(stemmed_query, "b")
            if (len(results) != 0):
                results = results[0]
        else: # regular search
            stemmed_query, misspelledMsg = bm25.StemQuery(stemmer, query, "b", book, chapter)
            results = bm25.Search(stemmer, stemmed_query, bm25.corpusB, bm25.stemmedCorpusB, 10)

    elif (tab == "Quran Search"):
        surah = surahSpinBox.get()
        if (surah == ' '):
            surah = ''
        ayah  = ayahSpinBox.get()
        if (ayah == ' '):
            ayah = ''
        query = quranSearchBox.get()

        if (surah != ""):
            surah = surah + "|" # add pipe if they have chapter
        if (surah != "" and ayah != ""): # if have both, only search for one verse
            oneVerse = True
            if (query != ""):
                tk.messagebox.showinfo("Single verse search", "Disregarding query and searching for particular verse instead.")
            stemmed_query = surah + ayah
            results = bm25.OneVerse(stemmed_query, "q")
            results = results[0]
        else: # regular search
            stemmed_query, misspelledMsg = bm25.StemQuery(stemmer, query, "q", "", surah)
            results = bm25.Search(stemmer, stemmed_query, bm25.corpusQ, bm25.stemmedCorpusQ, 10)
    else:
        query = compareSearchBox.get()
        both = True
        stemmed_query, misspelledMsg = bm25.StemQuery(stemmer, query, "x", "", "")
        # if both, they can only search with the query, so do a regular search for both
        resultsB = bm25.Search(stemmer, stemmed_query, bm25.corpusB, bm25.stemmedCorpusB, 5)
        resultsQ = bm25.Search(stemmer, stemmed_query, bm25.corpusQ, bm25.stemmedCorpusQ, 5)
        results  = ["Bible: \n"] + resultsB + ["Quran: "] + resultsQ

    # show misspelling correction(s)
    if(len(misspelledMsg) != 0 ):
        allMisspellings = ""
        msgTitle = ""
        msg = ""
        for sentence in misspelledMsg:
            allMisspellings = allMisspellings + sentence + "\n"
        if (len(misspelledMsg) == 1):
            msgTitle = "Found misspelling"
            msg = "\nIf this correction was not desired, recheck the spelling of your query and try again."
        elif (len(misspelledMsg) > 1):
            msgTitle = "Found misspellings"
            msg = "\nIf these corrections were not desired, recheck the spelling of your query and try again."
        tk.messagebox.showinfo(msgTitle, allMisspellings + msg)

    # check if there are results
    if (oneVerse and len(results) == 0):
        tk.messagebox.showwarning("No results found","Verse out of range.")
    elif (both and len(resultsB) == 0 and len(resultsQ) == 0):
        tk.messagebox.showwarning("No results found","Suggestions: make your query more specific and check for misspellings.")
    elif (not oneVerse and not both and len(results) == 0):
        tk.messagebox.showwarning("No results found","Suggestions: make your query more specific and check for misspellings.")
    else: # display results
        if (oneVerse): # if there is only 1 verse to print
            compareResultBox.insert(0.0, results)
        else:
            i=0
            for i in range(len(results)):
                pos = i+1
                pos = str(pos) + '.0'
                compareResultBox.insert(pos, results[i] + '\n')
    compareResultBox.config(state=DISABLED)



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

### create frames ###

# create frames for entry and results
topFrame = Frame(bibleTab).grid(row=0)
bottomFrame   = Frame(bibleTab).grid(row=1)

# create clear button to clear entry and results
clearButton = tk.Button(topFrame, text="Clear", width=7 , padx=7, command=clear).grid(row=0, column=0, sticky=NE)

### build bible tab ###

# add labels
Label(bibleTab, text="Bible", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(bibleTab, text="Book", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=0, sticky=W)
Label(bibleTab, text="Chapter", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=2)
Label(bibleTab, text="Verse", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=4)
Label(bibleTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)
Label(bottomFrame, text="Results", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
bookswChapter = {"Genesis":50,"Exodus":40,"Leviticus":27,"Numbers":36,"Deuteronomy":34,"Joshua":24,"‌Judges":21, "Ruth":4,"1Samuel":31,"2Samuel":24,"1Kings":22,"2Kings":25,"1Chronicles":29,"2Chronicles":36,"Ezra":10,"Nehemiah":13,"Esther":10,"Job":42,"Psalms":150,"Proverbs":31,"Ecclesiastes":12,"SongofSolomon":8,"Isaiah":66,"Jeremiah":52,"Lamentations":5,"Ezekiel":48,"Daniel":12,"Hosea":14,"Joel":3,"Amos":9,"Obadiah":1,"Jonah":4,"Micah":7,"Nahum":3,"Habakkuk":3,"Zephaniah":3,"Haggai":2,"Zechariah":14,"Malachi":4,"Matthew":28,"Mark":16,"Luke":24,"John":21,"Acts":28,"Romans":16,"1Corinthians":16,"2Corinthians":13,"Galatians":6,"Ephesians":6,"Philippians":4,"Colossians":4,"1Thessalonians":5,"2Thessalonians":3,"1Timothy":6,"2Timothy":4,"Titus":3,"Philemon":1,"Hebrews":13,"James":5,"1Peter":5,"2Peter":3,"1John":5,"2John":1,"3John":1,"Jude":1,"Revelation":22}
books = [" "] + list(bookswChapter.keys())

changeVerse = tk.StringVar()
changeVerse.trace('w', updateBible)
chapterSpinBox = ttk.Combobox(bibleTab, width=6, textvariable=changeVerse, state = DISABLED)
chapterSpinBox.grid(row=1, column=3)
verses = [""] + list(range(1, 177))
verseSpinBox = tk.Spinbox(bibleTab, width=6, values = (verses), state = DISABLED) # 176 b/c that is the highest verse number
verseSpinBox.grid(row=1, column=4+1)
bibleSearchBox = tk.Entry(bibleTab, width=30)
bibleSearchBox.grid(row=2, column=1)
bibleResultBox = tk.Text(bottomFrame, width=60-3, height=12)
bibleResultBox.grid(row=4, sticky=W)
changeBook = tk.StringVar()
changeBook.trace('w', updateBible)
# bookSpinBox    = tk.Spinbox(bibleTab, values=books)
bookSpinBox = ttk.Combobox(bibleTab, width = 27, values = (books), textvariable=changeBook, state="readonly")
bookSpinBox.grid(row=1, column=1)

### build quran tab ###

# add labels
Label(quranTab, text="Quran", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(quranTab, text="Surah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=0, sticky=W)
Label(quranTab, text="Ayah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=2)
Label(quranTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
surahswAyah = {'1': 7, '2': 286, '3': 200, '4': 176, '5': 120, '6': 165, '7': 206, '8': 75, '9': 129, '10': 109, '11': 123, '12': 111, '13': 43, '14': 52, '15': 99, '16': 128, '17': 111, '18': 110, '19': 98, '20': 135, '21': 112, '22': 78, '23': 118, '24': 64, '25': 77, '26': 227, '27': 93, '28': 88, '29': 69, '30': 60, '31': 34, '32': 30, '33': 73, '34': 54, '35': 45, '36': 83, '37': 182, '38': 88, '39': 75, '40': 85, '41': 54, '42': 53, '43': 89, '44': 59, '45': 37, '46': 35, '47': 38, '48': 29, '49': 18, '50': 45, '51': 60, '52': 49, '53': 62, '54': 55, '55': 78, '56': 96, '57': 29, '58': 22, '59': 24, '60': 13, '61': 14, '62': 11, '63': 11, '64': 18, '65': 12, '66': 12, '67': 30, '68': 52, '69': 52, '70': 44, '71': 28, '72': 28, '73': 20, '74': 56, '75': 40, '76': 31, '77': 50, '78': 40, '79': 46, '80': 42, '81': 29, '82': 19, '83': 36, '84': 25, '85': 22, '86': 17, '87': 19, '88': 26, '89': 30, '90': 20, '91': 15, '92': 21, '93': 11, '94': 8, '95': 8, '96': 19, '97': 5, '98': 8, '99': 8, '100': 11, '101': 11, '102': 8, '103': 3, '104': 9, '105': 5, '106': 4, '107': 7, '108': 3, '109': 6, '110': 3, '111': 5, '112': 4, '113': 5, '114': 6}
surahs = [" "] + list(surahswAyah.keys())

changeAyah = tk.StringVar()
changeAyah.trace('w', updateQuran)
surahSpinBox   = ttk.Combobox(quranTab, values = (surahs), textvariable=changeAyah, state = "readonly")
surahSpinBox.grid(row=1, column=1)
ayahSpinBox    = ttk.Combobox(quranTab, width=7, state = DISABLED)
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
compareResultBox = tk.Text(bottomFrame, width=60-3, height=12, wrap="word", spacing1=8, state=DISABLED)
compareResultBox.grid(row=4, sticky=W)

### build bottom frame ###
Label(bottomFrame, text="Results", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)
searchButton = tk.Button(bottomFrame, text="Search", width=7 , padx=7, command=search)
searchButton.grid(row=2, sticky=E)

# run code
root.mainloop()

