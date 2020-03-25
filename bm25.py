# have to do: pip install rank_bm25

import re
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

stemmer = PorterStemmer()

corpus = [
    "1:1 In the beginning God created the heaven and the earth.",
    "1:2 And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.",
    "1:3 And God said, Let there be light: and there was light.",
    "1:4 And God saw the light, that it was good: and God divided the light from the darkness.",
    "1:5 And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day."
]

stemmedCorpus = [
    "1:1 begin god creat heaven earth",
    "1:2 earth without form void dark upon face deep spirit god move upon face water",
    "1:3 god said let light light",
    "1:4 god saw light good god divid light dark",
    "1:5 god call light day dark call night even morn first day"
]

tokenized_corpus = [doc.split(" ") for doc in stemmedCorpus]
bm25 = BM25Okapi(tokenized_corpus)

query = "god"

pat = re.compile(r'[^A-Za-z0-9 \:]+')
query = re.sub(pat, '', query).lower()
tokenized_query = query.split(" ")
tokenized_query = [word for word in tokenized_query if word not in stopwords.words('english')]
stemmed_query = [];
for word in tokenized_query:
    word = stemmer.stem(word)
    stemmed_query.append(word)
print(stemmed_query)

doc_scores = bm25.get_scores(stemmed_query)
print (doc_scores)
doc_scores = list(doc_scores)

matches = []
length = len(doc_scores)
doc_scores_sorted = sorted(doc_scores, reverse=True)
print(doc_scores_sorted)
# doc_scores = [.1,.3,.3,.2,.3]
# doc_scores_sorted = [.3,.3,.3,.2,.1]
# # [1,2,4,3,0]

i = 0
while (i < len(doc_scores_sorted) and doc_scores_sorted[i] > 0): 
    match = doc_scores.index(doc_scores_sorted[i])
    matches.append(match) # matches will have the indices of the ones over 0
    doc_scores[match] = "done"
    i += 1   
        
print("matches: ",matches)

# allResults = bm25.get_top_n(tokenized_query, stemmedCorpus, n=10)

results = [corpus[i] for i in matches]

if (len(results) == 0):
    print("No results found")
elif (len(results) < 10):
    print(results)
else:
    for i in range(10):
        print (results[i])