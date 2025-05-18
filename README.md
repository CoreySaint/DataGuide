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
implemented, their purpose, and their variables.

------------------------------------------Required Packages------------------------------------------

**Regular Expressions**

  The regular expressions package is a built in module, so no installation is necessary, just 
  importation:

    import re

**JSON**

  The JSON package is a built in module, so no installation is necessary, just importation:

    import json

**Python Version**

  Built using Python 3.12.2

-----------------------------------------------Classes-----------------------------------------------

**Node Class**

  The Node class is used to create individual node objects which are contained in the 
  dataguide in a tree-like structure. Each node initializes with an empty children 
  dictionary and a template counters dictionaries containing all possible types and initial 
  counts of zero.

    node = Node()

**DataGuide Class**

  The DataGuide class is used to store all nodes present in the document and has most of the
  necessary methods for creation and maintenance of the guide. Each DataGuide intializes with 
  a root node being created and a total document count attribute being set to zero.

    dataguide = Dataguide()

----------------------------------------------Functions----------------------------------------------

**counters():**

  This is the only function used in the dataguide program, it simply returns a template dictionary 
  containing all possible types with initial counts of zero, used in initialization of a node.

-----------------------------------------------Methods-----------------------------------------------

**node.update_counter(type_name, delta=1):**

  Increases or decreases counter for a specific type in a node based on input type and delta 
  (default = 1). Used when inserting documents into a dataguide.

    node.update_count('int', -1)

**node.to_dict():**

  Converts a node to dictionary format for exportation into text file.

**node.from_dict(doc):**

  Converts a node from a dictionary format in a text file into a node object. The input "doc" specifies 
  the document from which the node will be created. The document will have to be loaded into python prior
  and stored as a variable. Here is an example of how to accomplish this:

    with open("filename.txt", r) as f:
      doc = json.load(f)
    node.from_dict(doc)

**dataguide.search(path):**

  Takes a path as input which should be a sequence of keys exactly as they appear in the document seperated 
  by dots (.). Returns boolean based on if the path is present or not. To access arrays, add a star after 
  the key of the array (Example path: a.b.c.* if c is the key for an array)

    dataguide.search("a.b.c")

**dataguide.insert_document(doc):**

  Takes a document as input and adds said document to the dataguide. Specifically iterates through document 
  key-value pairs and increments counters based on type of value, also increases total_docs by one.

    dataguide.insert_document({"a": 1, "b": {"c": 'foo', "d": 2}, "e": [1, 2, 3]})

**dataguide.delete_document(doc):**

  Takes a document as input and removes said document from the dataguide. Specifically iterates through document 
  and finds the key-values pairs in the dataguide. Then it decrements counters based on type of value at each 
  specific key and decrements total_docs by one. Additionally, will remove a key if all counters are at zero.

    dataguide.delete_document({"a": 1, "b": {"c": 'foo', "d": 2}, "e": [1, 2, 3]})
    
**dataguide.print_guide():**

  Prints the dataguide with each key and associated counters dictionary on a distinct line.

**dataguide.clear():**

  Removes all keys and counters from the dataguide and resets total_docs to zero.

**dataguide.save(filename):**

  Converts dataguide into JSON format and saves to text file named based on input filename variable.

    dataguide.save("test.txt")

**dataguide.to_dict():**

  Converts dataguide to single dictionary, used when saving dataguide to file.

**dataguide.from_dict(doc):**

  Takes a file containing a dataguide and converts it back into dataguide object with nodes. The doc variable is 
  the document being converted and requires it to be saved as a variable prior to loading.

    with open("filename.txt", r) as f:
      doc = json.load(f)
    dataguide.from_dict(doc)

**dataguide.load(filename):**

  Can take a specific files path as input and from it convert it into a dataguide with accurate nodes.

    dataguide.load("text.txt")

**dataguide.core():**

  Returns a list of all core keys and their value counts. A core key is one that appears in every document.

    dataguide_core = dataguide.core()

**dataguide.card(path=None):**

  Returns a single counter dictionary containing the total variable type counts for an entire path or dataguide.
  If no path is specified, will return for total dataguide.

    dataguide_card = dataguide.card()

**dataguide.union(other):**

  Returns a new dataguide made up of all keys and values from both dataguides. The input variable, other, is a
  second dataguide.

    union_guide = dataguide1.union(dataguide2)

**dataguide.intersect(other):**

  Returns a new dataguide made up of keys and values that would be present if the original JSON files were
  intersected. The input variable, other, is a second dataguide.

    intersection_guide = dataguide1.intersect(dataguide2)

**dataguide.difference(other):**

  Returns a new dataguide made up of the difference between two dataguides. The input variable, other, is a 
  second dataguide.

    difference_guide = dataguide1.difference(dataguide2)

--------------------------------------------Helper Methods-------------------------------------------
    
*These methods are called by the above methods and do not need to be called by user*

**dataguide._traverse_path(path):**

  Method used to traverse through a path, the final node in the path is returned if the path exists, if
  not then None is returned. Used in conjunction with multiple other methods.

**dataguide._get_type(value):**

  Used to get the specific type of a variable, used when adding or removing documents. Returns string
  representing type (int, string, float, etc.)

**dataguide._is_date(s):**

  Used to tell if a string is a date or just a string, returns True if string is a date else false.

**dataguide._insert_value(node, value):**

  Used to insert a single value into a dataguide, recursively called on each child node.

**dataguide._delete_value(node, value):**

  Method used to decrease counter for a type when deleting documents. Will delete key/node if all
  counters are zero after decrease.

**dataguide._extract_core(node):**

  Method used to check if a single node is a core node or not, recursively called on children of node.
  Node object is returned if it is a core node, if not then None returned.

**dataguide._sum_counters(node):**

  Used to sum all the counters together starting with input node, recursively called on children.
  Dictionary containing total counts returned.

**dataguide._union_nodes(node1, node2):**

  Helper method that takes two nodes, one from each dataguide, and adds them to the new guide. If the
  nodes share the same key, their counts are summed and combined, if they do not, then they are simply
  added to the new guide.

**dataguide._gather_paths(self, node, prefix="")**

  Helper method that takes a node and a prefix and returns all paths that branch from that node.
  If a root node is input, will return all paths in document. Prefix is used when a node is not
  the root node, this ensures the path in its entirety is stored.

**dataguide._max_noncommon(self, all_paths, common_paths)**
  Helper method that takes all paths and the common paths of two dataguides that were calculated
  in the intersect method. Returns the maximum total of counters in the noncommon paths (paths
  present in only one of the dataguides).

**dataguide._subtract_nodes(node1, node2):**

  Helper method that recursively takes two nodes, one from each dataguide, and returns the difference
  between nodes. If the nodes share a key, node2's counts are subtracted from node1's. Additionally
  removes nodes with zero counts after difference.

**dataguide._clone_subtree(node):**

  Helper method that recursively copies and returns a node along with all of its children. Used in
  _subtract_nodes method when a key appears in only the first dataguide and not in the second.

-----------------------------------------Creating a DataGuide----------------------------------------

**1. Import DataGuide**

    from DataGuide.py import DataGuide
   
**2. Create DataGuide object**

    dataguide = DataGuide()
     
**3. Load data**

   **a. From JSON file**

    with open("filename.json", "r") as f
      data = json.load(f)

    dataguide.insert_document(data)
   
   **b. From dictionary**

    dict = {"a": 1, "b": "foo"}

    dataguide.insert_document(dict)

   **c. From dataguide file**

    dataguide.load("filename.txt")
   
**4. Check dataguide**

    dataguide.print_guide()
   
**5. Save dataguide**

    dataguide.save("filename.txt")

**6. Run Methods**

    dataguide.search("a")

    core = dataguide.core()

    card = dataguide.card()

    union = dataguide.union(dataguide2)
