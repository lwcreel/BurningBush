# have to do: pip install rank_bm25
# have to do: pip install pyspellchecker

import re
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# functions:
# creates both the regular corpus and the stemmed corpus by splitting by " _ "
def CreateCorpus(file1, file2):
    corpus = []
    stemmedCorpus =[]
    doc = open("Docs/"+file1, "r")
    stemmedDoc = open("Docs/"+file2, "r")
    corpus = doc.read().split(" _ ") 
    stemmedCorpus = stemmedDoc.read().split(" _ ")
    return corpus, stemmedCorpus

# small function to replace an word in a list with replaceWith, used in FixMisspellings function
def replace(l, word, replaceWith):
    for i, element in enumerate(l):
        if element == word:
            l[i] = replaceWith
    return l

# cleans up the texts for the FixMisspellings function
def CleanTexts (document):
    doc = open("Docs/"+document+".txt", "r")
    docText = doc.read() # read data
    docText = docText.replace('\n', ' ') # replace new line with spaces
    pat = re.compile(r'[^A-Za-z0-9 \:\|]+') # get rid of puncuation besides : and |
    docText = re.sub(pat, '', docText)
    docText = docText.split() # split into words by spaces
    docText = [word.lower() for word in docText] # make lowercase
    return docText

# fixes any misspellings in the query
def FixMisspellings(tokenized_query):
    spell = SpellChecker()
    misspelledMsg = []
    # gets rid of puncuation, makes lowercase
    bibleText = CleanTexts("BibleWithBookNames")
    quranText = CleanTexts("QuranWithSpaces")
    # add words to their dictionary, I fed in the entire Bible and Quran, along with all the books of the Bible
    spell.word_frequency.load_words(["Genesis‌","Exodus","Leviticus‌","Numbers‌","Deuteronomy","Joshua","‌Judges","‌Ruth","‌1Samuel‌‌","2Samuel","‌‌1Kings‌‌","2Kings‌‌","1Chronicles‌","2Chronicles‌","Ezra‌","Nehemiah","‌Esther","‌Job","‌Psalms‌","Proverbs","‌Ecclesiastes‌","SongofSolomon‌","Isaiah‌","Jeremiah","‌Lamentations‌","Ezekiel","‌Daniel‌","Hosea","‌Joel‌","Amos‌","Obadiah‌","Jonah","Micah","Nahum","‌Habakkuk","Zephaniah‌","‌Haggai‌","Zechariah","Malachi‌","Matthew‌","Mark","‌Luke‌","John","‌Acts‌","Romans‌","‌1‌Corinthians","2Corinthians‌","Galatians‌","Ephesians‌","Philippians‌","Colossians‌","1Thessalonians‌","2Thessalonians‌","1Timothy‌","2Timothy‌","Titus‌","Philemon‌","Hebrews‌","James","1Peter‌","2Peter","1John‌","2John‌","3John‌","Jude‌","Revelation"])
    spell.word_frequency.load_words(bibleText+quranText)
    misspelled = spell.unknown(tokenized_query) # finds the misspelled words
    for word in misspelled: # replaces misspelled words with the most likely replacement
        if word == "":
            pass
        else:
            tokenized_query = replace(tokenized_query,word,spell.correction(word))
            if word != spell.correction(word):
                print ("Replacing \"" + word +"\" with \""+ spell.correction(word) + "\"")
                misspelledMsg.append("Replaced \"" + word +"\" with \""+ spell.correction(word) + "\"")
    return tokenized_query, misspelledMsg

# cleans up the query and adds book/chapter to query if needed
def StemQuery(stemmer, query, doc, book, chapter):
    pat = re.compile(r'[^A-Za-z0-9 \:\|]+') # remove everything but letters, numbers, :, and |
    query = re.sub(pat, '', query).lower() # make query lowercase
    tokenized_query = query.split(" ") # split query by space
    tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')] # remove stop words from query
    tokenized_query, misspelledMsg = FixMisspellings(tokenized_query) # fix any misspellings that may be in query
    stemmed_query = []
    if (tokenized_query != ['']): # only need to stem if there is a query
        for word in tokenized_query: # stem query
            word = stemmer.stem(word)
            stemmed_query.append(word)
    if (doc == "b"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter) # adds chapter in front of query if included
        if (book != ""):
            stemmed_query.insert(0, book) # adds book in front of query if included
    elif (doc == "q"):
        if (chapter != ""):
            stemmed_query.insert(0, chapter) # adds chapter in front of query if included
    elif (doc == "x"): # can only search query when comparing so do nothing
        pass
    # print(stemmed_query)
    return stemmed_query, misspelledMsg

# returns only one verse from the text
def OneVerse(query, doc):
    if (doc == "b"):
        results = [i for i in corpusB if query in i] 
    elif (doc == "q"):
        results = [i for i in corpusQ if query in i] 
    return results

# uses BM25 on the stemmed corpus to give scores for each document in order to return the top <amt> of documents from corpus that are most relevant
def Search(stemmer, stemmed_query, corpus, stemmedCorpus, amt):
    tokenized_corpus = [doc.split(" ") for doc in stemmedCorpus] # split stemmedcorpus by space
    bm25 = BM25Okapi(tokenized_corpus) # run BM25 on tokenized stemmed corpus
    doc_scores = list(bm25.get_scores(stemmed_query)) # get scores of all the documents and make it a list
    doc_scores_sorted = sorted(doc_scores, reverse=True) # sort scores in decreasing order (highest score first)
    if (len(doc_scores_sorted) < amt): # it will find top <amt> results (or less)
        length = len(doc_scores_sorted)
    else:
        length = amt
    # have to translate stemmed corpus results to corpus results so we can return the nonstemmed results
    matches = []
    i = 0
    while (i < length and doc_scores_sorted[i] > 0):
        match = doc_scores.index(doc_scores_sorted[i])
        matches.append(match) # matches will contain the indices in corpus of the results with a score over 0
        doc_scores[match] = "done"
        i += 1
    results = [corpus[i] for i in matches] # this holds the final results from regular corpus
    return results


# main: 
# variables
results = []
resultsB = []
resultsQ = []
oneVerse = False 
both = False

stemmer = PorterStemmer()

# make corpus and stemmed corpus for both Bible and Quran
corpusB, stemmedCorpusB = CreateCorpus("BibleWithBookNames.txt", "StemmedBibleWithBookNames.txt")
corpusQ, stemmedCorpusQ = CreateCorpus("QuranWithSpaces.txt", "StemmedQuranWithSpaces.txt")

# user input / query section
doc = "b" # b for Bible, q for Quran, x for both
book = ""
chapter = ""
verse = ""
query = "real"

misspelledMsg = []

# separated based on the doc (b, q, or x)
if (doc == "b"):
    if (chapter != ""):
        chapter = chapter + ":" # add colon if they have chapter
    if (book != "" and chapter != "" and verse != ""): # if have all 3, only search for one verse
        oneVerse = True
        stemmed_query = book + " " + chapter + verse
        results = OneVerse(stemmed_query, "b")
    else: # regular search
        stemmed_query, misspelledMsg = StemQuery(stemmer, query, "b", book, chapter)
        results = Search(stemmer, stemmed_query, corpusB, stemmedCorpusB, 10)
elif (doc == "q"):
    if (chapter != ""):
        chapter = chapter + "|" # add pipe if they have chapter
    if (chapter != "" and verse != ""): # if have both, only search for one verse
        oneVerse = True
        stemmed_query = chapter + verse
        results = OneVerse(stemmed_query, "q")
    else: # regular search
        stemmed_query, misspelledMsg = StemQuery(stemmer, query, "q", "", chapter)
        results = Search(stemmer, stemmed_query, corpusQ, stemmedCorpusQ, 10)
elif (doc == "x"):
    both = True
    stemmed_query, misspelledMsg = StemQuery(stemmer, query, "x", book, chapter)
    # if both, they can only search qith the query, so do a regular search for both
    resultsB = Search(stemmer, stemmed_query, corpusB, stemmedCorpusB, 5)
    resultsQ = Search(stemmer, stemmed_query, corpusQ, stemmedCorpusQ, 5)


# if (oneVerse and len(results) == 0):
#     print("No results found. Chapter or verse out of range.")
# elif (both and len(resultsB) == 0 and len(resultsQ) == 0):
#     print("No results found. Suggestions: make your query more specific and check for misspellings.")
# elif (not oneVerse and not both and len(results) == 0):
#     print("No results found. Suggestions: make your query more specific and check for misspellings.")
# else:
#     if (oneVerse):
#         results = results[0] # only keep the very first result
#         print(*results, sep = "")
#     elif (both):
#         print("Bible:")
#         print(*resultsB, sep = "\n")
#         print("\nQuran:")
#         print(*resultsQ, sep = "\n")
#     else:
#         print(*results, sep = "\n")





# could do the substring thing to make a new corpus and only search the smaller corpus if book and/or chapter
# corpusB = [i for i in corpusB if stemmed_query in i] 
# stemmed_query = book + " " + chapter
# stemmedCorpusB = [i for i in corpusB if stemmed_query in i] 