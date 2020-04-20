# How to run The Burning Bush


You have to run the following commands in the terminal:

pip install rank_bm25
pip install pyspellchecker


You have to have the following lines in a file and run the file (see setup.py):

import nltk
nltk.download('punkt')
nltk.download('stopwords')

(These commands are also already conveniently in bm25.py, which will run when you run TBB.py (the main file).  You can comment the last 2 lines above out when you have already downloaded them once, but leave the first one uncommented.)


After all of the above has been done, run by doing: 

py TBB.py
