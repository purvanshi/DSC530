
This file provides the instructions for running the code and the documentation of various functions

## Instructions for setting up the environment

* pip3 install -U nltk # Make sure the version is  at least 3.3.
* Download the CoreNLP packages
    * wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip
    * unzip stanford-corenlp-full-2018-02-27.zip
    * cd stanford-corenlp-full-2018-02-27
* Start the server still in the stanford-corenlp-full-2018-02-27 directory
    * java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,parse,depparse status_port 9000 -port 9000 -timeout 15000 & 
* Then in python
    * from nltk.parse import CoreNLPParser
    * parser = CoreNLPParser(url='http://localhost:9000')

You are all set to go!!

## The overall architechture of the main file is as follows -
* All parts (1 to 4) have been solved 
* You can give any sentence for processing. Change the sentence in the input.py file
* Various examples have been shown for the various types of sentences handles
* If the program runs into a confusion it throws an error to 'add more rules' and then continue
### Part 1 - Attach numeric word order indices to words
* The function traverse_tree() takes the parser output as input and traverses it in a recursive fashion counting the number of words passed
### Part 2 - Attach head words 
* The function dep_tree() takes the output of part 1 as input, traverses the tree in a recursuve fashion and finds the head of the phrases
* find_head() function takes a phrase as input and returns the head. It searches from a precedency_list, which specifies a criterion (like out of VB and NN, VB would be the head)
* An exception - 'Add rules' is thrown when the find_head function cannot find the head due to lack of rules
### Part 3 - Dependency Relations
* The function dep_list() takes the output of the parse tree marked with head words (part 2) as input and returns a list containing all the dependencies.
### Part 4 - Sorting Dependency Relations
* The output of part 3 is sorted using the sorted() function in python and key as the word suffixes

### The problems encountered during this assignment

The major task that I found difficult was to learn about the syntactic structure in a sentence and how to include it as rules for finding the head. Another problem was of handling the ambiguities during finding the heads of phrases. I went through Michael Collins desertation for understanding various rules and their significance. But for simplicity only a abasic form of those rules (in the form of a list) has been included during designing of the assignment. The search direction was always kept from left to right. 
Doing parts 3 and 4 gave me a better understanding of how to form dependency structure from phrase structure. After determining the heads in the tree, we can link the head words to their dependants which gives us the dependency structure.
