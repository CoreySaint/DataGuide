------------------------------------------------Intro------------------------------------------------

The purpose of this project is to implement methods into python that create a dataguide
given JSON documents and perform various tasks on them. A dataguide is essentially a schema
for a JSON document containing the keys as well as a count of data types contained in the
document(s). The main methods necessary for this include reading/writing JSON documents,
searching the document, identify and counting types, deleting documents from the dataguide, 
printing the guide, saving/loading dataguides, and clearing the guide. Additional methods 
are included as well to help identify characteristics of the dataguide like core (extracts 
keys present in all documents),card (extracts total counts of a document), union, 
intersection, and projection. Below contains all the classes, functions, and methods 
implemented, their purpose, and their variables

-----------------------------------------------Classes-----------------------------------------------

Node Class

  The Node class is used to create individual node objects which are contained in the 
  dataguide in a tree-like structure. Each node initializes with an empty children 
  dictionary and a template counters dictionaries containing all possible types and initial 
  counts of zero.

DataGuide Class

  The DataGuide class is used to store all nodes present in the document and has most of the
  necessary methods for creation and maintenance of the guide. Each DataGuide intializes with 
  a root node being created and a total document count attribute being set to zero.

----------------------------------------------Functions----------------------------------------------

counters():

  This is the only function used in the dataguide program, it simply returns a template dictionary 
  containing all possible types with initial counts of zero, used in initialization of a node.

-----------------------------------------------Methods-----------------------------------------------

node.update_counter(type_name, delta=1):

  Increases or decreases counter for a specific type in a node based on input type and delta 
  (default = 1). Used when inserting documents into a dataguide.

node.to_dict():

node.from_dict(doc):

dataguide.search(path):

dataguide.insert_document(doc):

dataguide.delete_document(doc):

dataguide.print_guide():

dataguide.clear():

dataguide.save():

dataguide.to_dict():

dataguide.from_dict(doc):

dataguide.load(filename):

dataguide.core():

dataguide.card(path=None):

--------------------------------------------Helper Methods-------------------------------------------
    *These methods are called by the above methods and do not need to be called by user*

dataguide._traverse_path(path):

dataguide._get_type(value):

dataguide._is_date(s):

dataguide._insert_value(node, value):

dataguide._delete_value(node, value):

dataguide._extract_core(node):

dataguide._sum_counters(node):
