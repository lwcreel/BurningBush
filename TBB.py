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
    
    if (tab == "Bible Search"):

        # get needed values from controls
        book    = bookSpinBox.get()
        chapter = chapterSpinBox.get()
        verse   = verseSpinBox.get()
        query   = bibleSearchBox.get()

        query = bm25.StemQuery(stemmer, query, "b", book, chapter)

    elif (tab == "Quran Search"):
        pass
    else:
        pass


acronym_dictionary={"AKA":"Also known as", "OT":"Overtime"}

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
bookSpinBox    = tk.Spinbox(bibleTab).grid(row=1, column=1)
chapterSpinBox = tk.Spinbox(bibleTab, width=7).grid(row=1, column=3)
verseSpinBox   = tk.Spinbox(bibleTab, width=7).grid(row=1, column=4+1)
bibleSearchBox = tk.Entry(bibleTab, width=30).grid(row=2, column=1)
bibleResultBox = tk.Text(bottomFrame, width=60-3, height=12, state=DISABLED).grid(row=4, sticky=W)

### build quran tab ###

# add labels
Label(quranTab, text="Quran", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(quranTab, text="Surah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=0, sticky=W)
Label(quranTab, text="Ayah", font=("Times New Roman", 12), padx=3, pady=7).grid(row=1, column=2)
Label(quranTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
surahSpinBox   = tk.Spinbox(quranTab).grid(row=1, column=1)
ayahSpinBox    = tk.Spinbox(quranTab, width=7).grid(row=1, column=3)
quranSearchBox = tk.Entry(quranTab, width=30).grid(row=2, column=1)
quranResultBox = tk.Text(bottomFrame,width=60-3, height=12, state=DISABLED).grid(row=4, sticky=W)

### build comparison tab ###

# add labels
Label(compareTab, text="Comparison", font=("Helvetica", 16), padx=3, pady=7).grid(row=0, column=0, sticky=W)
Label(compareTab, text="Query", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)

# add controls for search
compareSearchBox = tk.Entry(compareTab, width=30).grid(row=2, column=1)
compareResultBox = tk.Text(bottomFrame,width=60-3, height=12, state=DISABLED).grid(row=4, sticky=W)

### build bottom frame ###
Label(bottomFrame, text="Results", font=("Times New Roman", 12), padx=3, pady=7).grid(row=2, column=0, sticky=W)
searchButton = tk.Button(bottomFrame, text="Search", width=7 , padx=7, command=search).grid(row=2, sticky=E)

# run code
root.mainloop()
