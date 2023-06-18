from nltk.tokenize import MWETokenizer, word_tokenize
from nltk.corpus import stopwords, wordnet
import re
from marisa_trie import Trie
import nltk
import operator

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
    def __init__(self, text,NE_dict,remove_key):
        self.NE_dict = NE_dict
        self.remove_key = remove_key
        self.wtag = []
        self.class_tag = []
        self.text = text

    def tokenize(self):
	    return self.text.split(',')

    def token_dict(self):
	    tokenizer = MWETokenizer(mwes=None, separator=' ')
	    for w in self.NE_dict.keys():
		    word = str(w).rstrip().split()
		    tokenizer.add_mwe(word)
	    return tokenizer


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
        self.token_list = []
        rgx = re.compile('[^a-zA-Z]')
        text = self.replace_char()
        split = text.lower().rstrip().split()
        word = self.remove_suffix(split)
        tokenizer = self.token_dict()
        tokens = tokenizer.tokenize(word)
        self.tokens = [t for t in tokens if t != '' and t not in stop_words]
        for w in self.tokens:
            if self.NE_dict.get(w) != None:
                self.wtag.append(w)
                self.class_tag.append(self.NE_dict[w])
            self.token_list.append(w)

    def get_tokens(self):
        return self.token_list

    def get_keys(self):
        return self.wtag

    def get_NEtag(self):
        return self.class_tag

class Classify:
    def __init__(self, tag_list, tokens,model,vectorizer):
        self.tag_list = tag_list
        self.tokens = tokens
        self.model = model
        self.vectorizer = vectorizer
        self.category_cafs = []
        self.category_pred = []

    def cafs_rules(self):
      cate = {'cryptocurrency': 0.0, 'stocks': 0.0,'commodities': 0.0, 'forex': 0.0, 'economy': 0.0,'other': 0.0}
      if 'CMD' in self.tag_list:
        cate['commodities'] = cate['commodities'] + 0.82
      if 'CMD' in self.tag_list and 'GPE' in self.tag_list:
        cate['commodities'] = cate['commodities'] + 0.81
      if 'CYP' in self.tag_list:
        cate['cryptocurrency'] = cate['cryptocurrency'] + 0.96
      if 'BNK' in self.tag_list:
        cate['economy'] = cate['economy'] + 0.34
      if 'IND' in self.tag_list:
        cate['economy'] = cate['economy'] + 0.43
      if 'IND' in self.tag_list and 'GPE' in self.tag_list:
        cate['economy'] = cate['economy'] + 0.5
      if 'FRX' in self.tag_list:
        cate['forex'] = cate['forex'] + 0.98
      if 'MNY' in self.tag_list:
        cate['forex'] = cate['forex'] + 0.82
      if 'GPE' in self.tag_list and 'MNY' in self.tag_list:
        cate['forex'] = cate['forex'] + 0.8
      if 'STK' in self.tag_list:
        cate['stocks'] = cate['stocks'] + 0.6

      find = max(cate.items(), key=operator.itemgetter(1))
      if find[1] == 0:
        category_cafs = 'other'
      else:
         category_cafs = find[0]
      return category_cafs

    def hybrid_classify(self):
      if not self.tag_list:
        category_pred = 'other'
      else:
        cafs_pred = self.cafs_rules()
        X = self.vectorizer.transform(self.tokens)
        category  = self.model.predict(X)[0]
        if cafs_pred == 'forex' or cafs_pred == 'cryptocurrency' or cafs_pred == 'commodities':
                category_pred = cafs_pred
        elif cafs_pred == 'stocks':
          if category == 'economy' or category == 'cryptocurrency' or category == 'other':
              category_pred = category
          else:
              category_pred = cafs_pred
        else:
          category_pred = category
      return category_pred