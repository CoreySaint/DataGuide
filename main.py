import json
from DataGuide_v5 import DataGuide, Node

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

print(cardguide)
print()

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

data1 = {"a": 2, "b": {"c": 7, "d": 'bar', "e": 4}, "f": [1, 2, 3]}
data2 = {"a": 2, "b": {"c": 'bar'}, "g": 7}

guide1 = DataGuide()
guide2 = DataGuide()

guide1.insert_document(data1)
guide2.insert_document(data2)

union = guide1.union(guide2)
union.print_guide()
print()

data1 = [
    { "a": 1, "common": { "x": 10 }, "u1": "foo" },
    { "a": 2, "common": { "x": "twenty" }, "u2": "bar" },
    { "a": 3, "common": { "x": 30 } }
]

data2 = [
    { "a": 100, "common": { "x": 40 }, "v1": 3.14 },
    { "a": 200, "common": { "x": 20 }},
    { "a": 300, "common": { "x": "gamma" }, "v2": 2.71 }
]

guide3 = DataGuide()
guide4 = DataGuide()

guide3.insert_document(data1)
guide4.insert_document(data2)

difference = guide3.difference(guide4)
difference.print_guide()
print()
