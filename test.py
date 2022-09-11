from NE_Extractor import Extraction

text = 'biden budget nominee absolutely backs u.s. minimum wage hike'
Tag = Extraction(text)
Tag.tagging()

print(Tag.get_tokens())
print(Tag.get_keys())
print(Tag.get_NEtag())