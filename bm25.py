# have to do: pip install rank_bm25

from rank_bm25 import BM25Okapi

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]
tokenized_corpus = [doc.split(" ") for doc in corpus]
print(tokenized_corpus)
# we will have to make sure our corpus is is all lowercase and has no puncutation and all that

bm25 = BM25Okapi(tokenized_corpus)

query = "windy London"
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)
print (doc_scores)

count = 0
length = len(doc_scores) 
for i in range(length): # this keeps a count of how many of the results have a score over some cutoff (I made it .5 for now)
    if(doc_scores[i] > .5):
        count += 1

all_results = bm25.get_top_n(tokenized_query, corpus)#, n=1)

results = []
for i in range(count): # this puts the results only above the cutoff in a list (the get_top_n function sorts them by score)
    results.append(all_results[i])

if(len(results) == 0):
    print("No results found")
else:
    print (results) # prints results in order