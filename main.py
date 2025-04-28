import json
from DataGuide_v4 import DataGuide, Node

#Testing basic functionality
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

#Testing file input
with open("example_2.json", "r") as f:
  data = json.load(f)

guide.insert_document(data)

guide.print_guide()
print()

#Testing card and core methods
coreguide = guide.core()

coreguide.print_guide()
print()

cardguide = guide.card()

cardguide.print_guide()

#Testing edge cases
edge_cases = DataGuide()

with open("EdgeCases.json", "r") as g:
  data_g = json.load(g)

edge_cases.insert_document(data_g)

edge_cases.print_guide()
print()

edge_core = edge_cases.core()
edge_code.print_guide()
print()

print(edge_cases.total_docs)
