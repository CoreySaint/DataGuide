import json
from DataGuide import DataGuide, Node

guide = DataGuide()

data = {'a': 1, 'b': {'c': 'foo', 'd': 'bar', 'e': 4}, 'f': [1, 2, 3]}

guide.insert_document(data)

guide.print_guide()
print()

print(guide.search('b.c'))
print()

guide.delete_document(data)

guide.print_guide()
print()

with open("example_2.json", "r") as f:
  data = json.load(f)

guide.insert_document(data)

guide.print_guide()
