# Burning Bush

Our plan for the CSCE 470 project is to create a search engine, known as The Burning Bush (TBB), for religious texts, such as the Bible and the Quran, in order to aid comparative religious scholars. TBB could also be used by those who want to look up something specific from a specific religious document, or those that are curious about differences between religious texts. The proposed implementation of TBB will be in Python. We plan on preparing the text documents with Porter’s Stemming algorithm and storing the stemmed, relevant words in a positional index in order to be able to search the unstructured data. We chose to use a positional index in order for the user to be able to search using longer phrase queries. We will return the results, sorted by most relevant, using Okapi BM25. The user will interface with TBB through the usage of a graphical user interface (GUI) made using the Python GUI library Tkinter.

Things we have to worry about:<br>
GUI<br>
Searching<br>
Returning results<br>
Fixing misspellings?<br>

Possibly helpful links: <br>
https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089<br>
http://lixinzhang.github.io/implementation-of-okapi-bm25-on-python.html<br>
https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/summarization/bm25.py<br>
https://stackoverflow.com/questions/40966014/how-to-use-gensim-bm25-ranking-in-python

https://www.geeksforgeeks.org/python-gui-tkinter/<br>
http://code.activestate.com/recipes/580773-tkinter-search-box/

https://pypi.org/project/pyspellchecker/
