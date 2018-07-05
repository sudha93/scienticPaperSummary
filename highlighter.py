import os 
import subprocess
import json
from nltk import sent_tokenize,word_tokenize,ngrams
# This code attempts to highlight/select the important sentences in a scientific paper 
# for extractive summary. We are assuming the important sentences as the sentences in 
# abstract, conclusion and the 2nd half of introduction. We try to find sentences which are
# similar to these and add them in summary.


# This function returns list of sentences 
def preprocess(string):
    sents = sent_tokenize(string)  
    return sents

# This funciton returns a set of unigrams
def setFunction(sentList,n):
    # Manual method for ngrams 
    #myUniSet = set(t for s in sentList for t in word_tokenize(s))
    #myBiSet = set(t for s in sentList for t in zip(word_tokenize(s)[:-1],word_tokenize(s)[1:]))
    #return myUniSet,myBiSet
    if type(sentList) is list:
        sumSet = set(t for s in sentList for t in ngrams(word_tokenize(s),n))
    else:
        sumSet = set(t for t in ngrams(word_tokenize(sentList),n))
    return sumSet

'''
string = os.system('curl -v -H "Content-type: application/pdf" --data-binary @/DATA1/USERS/anirudh/mindmap/code/sample.pdf "http://scienceparse.allenai.org/v1"')
'''
'''
string = subprocess.check_output('curl -v -H "Content-type: application/pdf" --data-binary @/DATA1/USERS/anirudh/mindmap/code/sample.pdf "http://scienceparse.allenai.org/v1"')
'''

string = subprocess.check_output('curl -v -H "Content-type: application/pdf" --data-binary @sample.pdf "http://scienceparse.allenai.org/v1"', shell=True)

#print "This is the string\n"
d = json.loads(string.decode('utf-8'))
#print d
#print d['title'],'\n'
#print d['abstractText'],'\n'
l = d['sections']

# list of sentences other than the important ones
text_sents = []
for element in l:
    #print element,'\n'
    if len(element) >1 :
        h = element['heading']
        if 'introduction' in h.lower():
            intro = element['text']
        elif 'conclusion' in h.lower():
            conclusion = element['text']
        else:
            text = preprocess(element['text'])
            text_sents += text


# Preprocessing
# Initial summary contains title,abstract, 2nd half of introduction,conclusion
title = d['title']
summary = [title]
abs_sents = preprocess(d['abstractText'])
intro_sents = preprocess(intro)
intro_sents = intro_sents[len(intro_sents)/2:]
con_sents = preprocess(conclusion)
#print abs_sents
# List of sentences in the summary 
summary = summary + abs_sents + intro_sents + con_sents

# Using the n-gram overlap to pick summary sentences
valueDict = {}
sumSet1 = setFunction(summary,1)
sumSet2 = setFunction(summary,2)
sumSet3 = setFunction(summary,3)
for i,sent in enumerate(text_sents):
    
    number = len(sumSet1 & setFunction(sent,1)) + len(sumSet2 & setFunction(sent,2))+ len(sumSet3 & setFunction(sent,3))
    valueDict[i] = number
#print valueDict

# Sort dictionary elements based on their values
tuples = sorted(valueDict.items(), key=lambda x:x[1])[::-1]
print tuples 

# We can a no.of them and add to the summary , like a 1/4 th or put a threshold score etc 

























