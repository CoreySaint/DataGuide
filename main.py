import json
from DataGuide import DataGuide, Node

guide = DataGuide()

doc = {'a': 1, 'b': {'c': 'foo', 'd': 'bar', 'e': 4}, 'f': [1, 2, 3]}

guide.insert_document(doc)

guide.print_guide()

print(guide.search('b.c'))

guide.delete_document(doc)

guide.print_guide()

