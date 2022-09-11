from nltk.tokenize import MWETokenizer, word_tokenize
from nltk.corpus import stopwords, wordnet
import re
from marisa_trie import Trie
import pickle
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('Corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))


class Extraction:
    def __init__(self, text):
        self.NE_dict = pickle.load(open('NE.dict', 'rb'))
        self.remove_key = pickle.load(open('remove.list', 'rb'))
        self.wtag = []
        self.class_tag = []
        self.text = text
        self.tokenizer = MWETokenizer(mwes=None, separator=' ')
        for w in self.NE_dict.keys():
            self.tokenizer.add_mwe(str(w))


    def replace_char(self):
        re_text = str(self.text).strip()
        Hash = re.sub('#[^\s]+', '', re_text)
        Tweet = re.sub('@[^\s]+', '', Hash)
        http = re.sub(r'http\S+', '', Tweet)
        texts = http.replace("’", "'")
        texts = texts.replace('"', '')
        texts = texts.replace("' ", ' ')
        texts = texts.replace(" '", ' ')
        texts = texts.replace('[', '')
        texts = texts.replace(']', '')
        texts = re.sub('^UPDATE.[0-9]-', '', texts)
        texts = re.sub('^TOPWRAP.[0-9]-', '', texts)
        texts = re.sub('^WRAPUP.[0-9]-', '', texts)
        texts = re.sub('^UDPATE.[0-9]-', '', texts)
        texts = texts.lower()
        for w in self.remove_key:
            texts = texts.replace(w, '')

        pattern = r'[“”–‘’`:(){}!;?%*]'
        texts = re.sub(pattern, '', texts)
        return texts

    def remove_suffix(self, words):
        wordlist = []
        for str in words:
            if str.endswith("'s"):
                if str != "macy's" and str != "people's" and str != "han's" and str != "reddy's":
                    wordlist.append(str[:-2])
                else:
                    wordlist.append(str[:])
            elif str.endswith('-') or str.endswith("'") or str.endswith(':') or str.endswith(',') or str.endswith(
                    ';') or str.endswith('”') or str.endswith('+') or str.endswith('*'):
                if str != "+":
                    if str.endswith("'") and str.startswith("'"):
                        wordlist.append(str[1:-1])
                    else:
                        wordlist.append(str[:-1])
                else:
                    wordlist.append(str[:])
            elif str.startswith("'"):
                wordlist.append(str[1:])
            else:
                wordlist.append(str[:])
        return wordlist

    def tagging(self):
        text = self.replace_char()
        split = text.lower().rstrip().split()
        word = self.remove_suffix(split)
        tokens = self.tokenizer.tokenize(word)
        tokens = [t for t in tokens if t != '' and t not in stop_words]
        for w in tokens:
            if self.NE_dict.get(w) != None:
                self.wtag.append(w)
                self.class_tag.append(self.NE_dict[w])


    def get_key(self):
        return self.wtag

    def get_NEtag(self):
        return self.class_tag