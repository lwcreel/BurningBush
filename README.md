# How to run The Burning Bush


You have to run the following commands in the terminal:<br>

pip install rank_bm25<br>
pip install pyspellchecker <br><br>


You have to add the following lines in a file and run the file (see setup.py):<br>

import nltk<br>
nltk.download('punkt')<br>
nltk.download('stopwords')<br>

(These commands are also already conveniently in bm25.py, which will run when you run TBB.py (the main file).  You can comment the last 2 lines above out when you have already downloaded them once, but leave the first one uncommented.) <br><br>


After all of the above has been done, run by doing: <br>

py TBB.py
