Tutorial
========
Once the package has been installed, you can import the package as follows:

.. ipython:: python
   
   import py_stringmatching as sm

Using Tokenizers
----------------
py_stringmatching currently provides five different tokenizers: alphabetical tokenizer, alphanumeric tokenizer, delimiter-based tokenizer, qgram tokenizer, and whitespace tokenizer (more tokenizers can easily be added). A tokenizer can be created as follows:

.. ipython:: python

   # create an alphabetical tokenizer
   alphabet_tok = sm.AlphabeticTokenizer()
    
   # create an alphanumeric tokenizer
   alnum_tok = sm.AlphanumericTokenizer()
    
   # create a delimiter tokenizer using comma as a delimiter
   delim_tok = sm.DelimiterTokenizer(delim_set=[','])
    
   # create a qgram tokenizer using q=3
   qg3_tok = sm.QgramTokenizer(qval=3)
    
   # create a whitespace tokenizer
   ws_tok = sm.WhitespaceTokenizer()

By default, all the tokenizers return a bag of tokens. You can use the **return_set** parameter to specify if the tokenizer
should return a set or bag of tokens. Few examples are shown below:

.. ipython:: python

   # create an alphabetical tokenizer, which returns a set of tokens
   alphabet_tok_set = sm.AlphabeticTokenizer(return_set=True)
    
   # create a delimiter tokenizer using comma as a delimiter, which returns a set of tokens
   delim_tok_set = sm.DelimiterTokenizer(delim_set=[','], return_set=True)
 
All tokenizers have a **tokenize** method which tokenizes a given input string into a set or bag of tokens (depending on whether the flag return_set is True or False):

.. ipython:: python

   test_string = ' .hello, world!! data, science, is    amazing!!. hello.'

   # tokenize into alphabetical tokens
   alphabet_tok.tokenize(test_string)

   # tokenize into alphabetical tokens (with return_set set to True)
   alphabet_tok_set.tokenize(test_string)

   # tokenize using comma as the delimiter
   delim_tok.tokenize(test_string)

   # tokenize using whitespace as the delimiter
   ws_tok.tokenize(test_string)

Using Similarity Measures
-------------------------
py_stringmatching currently provides 14 different similarity measures (with plan to add more). To use a similarity measure, you first need to create a similarity measure object, as illustrated by the following examples:

.. ipython:: python

   # create a Jaccard similarity measure object
   jac = sm.Jaccard()
    
   # create a Levenshtein similarity measure object
   lev = sm.Levenshtein()

There are two main types of similarity measures,

(1) Those that when given two input strings will compute a true similarity score, which is a number in the range [0,1] such that the higher this number, the more similar the two input strings are. 

(2) Those that when given two input strings will compute a distance score, which is a number such that the higher this number, the more **dissimilar** the two input strings are. Clearly, Type-2 measures (also known as distance measures), are the reverse of Type-1 measures. 

For example, Jaccard similarity measure will compute a true similarity score in [0,1] for two input strings. Levenshtein similarity measure, on the other hand, is really a distance measure, which computes the edit distance between the two input strings (see for example Wikipedia or the string matching chapter in the book "Principles of Data Integration"). It is easy to convert a distance score into a true similarity score (again, see examples in the above book chapter). 

Given the above, each similarity measure object in py_stringmatching is supplied with two methods: **get_raw_score** and **get_sim_score**. The first method will compute the raw score as defined by that type of similarity measures, be it similarity score or distance score. For example, for Jaccard this method will return a true similarity score, whereas for Levenshtein it will return an edit distance score. 

The method **get_sim_score** normalizes the raw score to obtain a true similarity score (a number in [0,1], such that the higher this number the more similar the two strings are). For Jaccard, **get_sim_score* will simply call **get_raw_score**. For Levenshtein, however, **get_sim_score** will normalize the edit distance to return a true similarity score. 

Here are some examples of using the **get_raw_score** method:

.. ipython:: python

   # input strings
   x = 'string matching package'
   y = 'string matching library'

   # compute Jaccard score over tokens of x and y, tokenized using whitespace
   jac.get_raw_score(ws_tok.tokenize(x), ws_tok.tokenize(y))

   # compute Jaccard score over tokens of x and y, tokenized into qgrams (with q=3)
   jac.get_raw_score(qg3_tok.tokenize(x), qg3_tok.tokenize(y))
    
   # compute Levenshtein distance between x and y
   lev.get_raw_score(x, y)
    
Here are some example of using the **get_sim_score** method:

.. ipython:: python

   # get normalized Levenshtein similarity score between x and y
   lev.get_sim_score(x, y)
    
   # get normalized Jaccard similarity score (this is the same as the raw score)
   jac.get_sim_score(ws_tok.tokenize(x), ws_tok.tokenize(y))
   
So depending on what you want, you can call **get_raw_score** or **get_sim_score**. Note, however, that certain measures such as Affine Gap, Monge-Elkan, Needleman-Wunsch, Smith-Waterman and Soft TF/IDF do not have a **get_sim_score** method, because the raw scores of these measures cannot be normalized into similarity scores in [0,1] (see the Developer Manual for further explanation). More precisely, similarity measure objects of these types have **get_sim_score** methods, but calling these methods returns only a warning. 
