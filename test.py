from CAFS import Extraction, Classify
import pickle
import operator

def tokenize(text):
    return text.split(',')

NE_dict = pickle.load(open('NE.dict', 'rb'))
remove_key = pickle.load(open('remove.list', 'rb'))
vectorizer = pickle.load(open('vectorizer.vec', 'rb'))
model = pickle.load(open('svm.model', 'rb'))

text = 'biden budget nominee absolutely backs u.s. minimum wage hike'
#text = 'U.S. coffee roasters weigh price increases, cite shipping inflation'
Tag = Extraction(text,NE_dict,remove_key)
Tag.tagging()

print("Word Tokenization: ", Tag.get_tokens())
print("Entity Keyword: ", Tag.get_keys())
print("Entity Tagged: ", Tag.get_NEtag())
#tokens : ['biden', 'budget', 'nominee', 'absolutely', 'backs', 'u.s.', 'minimum wage', 'hike']
#keys: ['biden', 'u.s.', 'minimum wage']
#NE tag: ['PER', 'GPE', 'IND']

X = vectorizer.transform(Tag.get_tokens())
print("SVM Baseline Clssification Result: ", model.predict(X)[0])

cate = Classify(Tag.get_NEtag(),Tag.get_tokens(),model,vectorizer)
print("CAFS Clssification Result: ", cate.cafs_rules())
print("Hybrid Clssification Result: ", cate.hybrid_classify())
