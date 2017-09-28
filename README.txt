Greenhouse-MR
============
Using the Greenhouse API, scrape every job listing for a company and determine the most frequently used terms.

 
Usage
-----
Note that “Greenhouse-MR” depends on the “nltk” package for its stopwords filter. 

Install “nltk” via the command line:

python -c "import nltk; nltk.download('stopwords')"



Todo
----
Improve MapReduce function to recognize fuzzy matches, e.g. experience vs. experienced