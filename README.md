# Economic and Financial Entity
Economic and Financial Entity is a domain-specific dictionary for named entity recognition in the economic and financial domain. It's suitable for uses in named entities extraction or any tasks that are proposed for a specific term in economics and financial domain. This dictionary is maintained by the Data Science Group in the Department of Computer Science, Faculty of Science, Chiangmai University. Although we do our best, we cannot guarantee the relevance and accuracy of every entry in this dictionary. We intend to continually update the dictionary by correcting existing entries and by adding new ones. The details about our twelve economics and financial entities are described as follows. <br/>

![alt text](https://github.com/Wilawan-Y/EconomicFinancial-NE-Extractor/blob/main/entity.jpg?raw=true)

# Category-Associated Feature Set (CAFS) Classifier
We introducing the use of economics and financial entities as a representative feature for economic and financial news, then delivers the classifiers based on the category-associated feature set. Moreover, the use of CAFS with the existing text classification baselines can improves out-of-domain news classification performances.  <br/>
# Instructions:
If you add words to this dictionary or correct words in your version of this dictionary, we would appreciate it if you could send these additions and corrections to us (wilawan_y@cmu.ac.th) for consideration in a subsequent version. All submissions will be reviewed and approved by the current maintainer.

# Getting started
## install package with pip
```python
pip install  git+https://github.com/Wilawan-Y/CAFS-Classifier.git
```
## dowload and unzipped file 
- download the whole code in a zip file 
- Extract or unzipped file into a convenient location on your computer and start working on it.
  
## Dependencies:
- marisa_trie <br/>
- nltk <br/>
- pickle <br/>
- regex <br/>
- operator <br/>
- scikit-learn <br/>

# Usage:
## prepare additional usage files
```python
from CAFS import Extraction, Classify
import pickle

def tokenize(text):
    return text.split(',')

NE_dict = pickle.load(open('NE.dict', 'rb'))
remove_key = pickle.load(open('remove.list', 'rb'))
vectorizer = pickle.load(open('vectorizer.vec', 'rb'))
model = pickle.load(open('svm.model', 'rb'))
```
## Name Entity Extraction
```python
text = 'U.S. coffee roasters weigh price increases, cite shipping inflation'
Tag = Extraction(text,NE_dict,remove_key)
Tag.tagging() # Name Entity Extraction module

print(Tag.get_tokens()) # Get word tokenization based on domain-specific dictionary
print(Tag.get_keys()) # Get Name Entity words
print(Tag.get_NEtag()) # Get Name Entity Tagged
```
```
['u.s.', 'coffee', 'roasters', 'weigh', 'price', 'increases', 'cite', 'shipping', 'inflation'] <br/>
['u.s.', 'coffee', 'inflation'] <br/>
['GPE', 'CMD', 'IND'] <br/>
```
## News Categorization
```python
Category = Classify(Tag.get_NEtag(),Tag.get_tokens(),model,vectorizer)

print("CAFS Clssification: ", Category.cafs_rules()) # Get classification result from CAFS Clasifier
print("Hybrid Clssification: ", Category.hybrid_classify()) # Get classification result from Hybrid Approach

# SVM Baseline Clasifier
X = vectorizer.transform(Tag.get_tokens())
print("SVM Baseline Clssification Result: ", model.predict(X)[0])
```
```
CAFS Clssification:  commodities <br/>
Hybrid Clssification:  commodities <br/>
SVM Baseline Clssification:  stocks <br/>
```
# Reference:
- Wilawan Yathongkhum, Department of Computer Science, Faculty of Science, Chiangmai University.
