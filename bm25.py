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
    "1:1 in the begin god creat the heaven and the earth",
    "1:2 and the earth wa without form and void and dark wa upon the face of the deep and the spirit of god move upon the face of the water",
    "1:3 and god said let there be light and there wa light",
    "1:4 and god saw the light that it wa good and god divid the light from the dark",
    "1:5 and god call the light day and the dark he call night and the even and the morn were the first day"
]

tokenized_corpus = [doc.split(" ") for doc in stemmedCorpus]
bm25 = BM25Okapi(tokenized_corpus)

query = "the day"

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

matches = []
length = len(doc_scores) 
for i in range(length): # this keeps a count of how many of the results have a score over some cutoff
    if(doc_scores[i] > 0):
        matches.append(i)

# all_results = bm25.get_top_n(tokenized_query, corpus)#, n=1)

results = [corpus[i] for i in matches]

if (len(results) == 0):
    print("No results found")
elif (len(results) < 10):
    print(results)
else:
    for i in range(10):
        print (results[i])