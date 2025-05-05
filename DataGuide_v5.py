import re
import json

#Basic function to return dictionary of counters based on common types
def counters():
    return {"int": 0, "str": 0, "float": 0, "date":0, "obj": 0, "arr": 0}

class Node:
    def __init__(self):
        """
        Initialization method for Node
        """
        #Children dictionary
        self.children = {}
        #Add counters dictionary
        self.counters = counters()

    def update_counter(self, type_name, delta=1):
        """
        Increases or decreases counter for the specific type input (based on delta)
        """
        #If the specific type is present in the node
        if type_name in self.counters:
            #increase or decrease counter
            self.counters[type_name] += delta
        #Fallback if unexpected type
        else:
            #set counter equal to delta
            self.counters[type_name] = delta
        
    def to_dict(self):
        """
        Method to convert node to dictionary for output
        """
        #Create children dictionary and fill with values
        children_dict = {key: child.to_dict() for key, child in self.children.items()}
        return {
            "counters": self.counters,
            "children": children_dict
        }
    
    @classmethod
    def from_dict(cls, d):
        """
        Class method to convert data guide text file to dictionary for output
        """
        #Create a new node
        node = cls()
        #Add counters to node
        node.counters = d.get("counters", counters())
        #Add children to node
        node.children = {key: cls.from_dict(child_dict) for key, child_dict in d.get("children", {}).items()}
        return node

class DataGuide:
    def __init__(self):
        """
        Initialization method for DataGuide
        """
        #Create Node object for root
        self.root = Node()
        #Initialize document counter
        self.total_docs = 0

    def search(self, path):
        """
        Search method, returns boolean based on if path is present in data guide
        """
        #Call helper method to move through path
        node = self._traverse_path(path)
        #Return boolean based on if path is present
        return node is not None

    def _traverse_path(self, path):
        """
        Helper method to move through a path, starting at the root node and moving from child to child until path is complete or and end is reached
        """
        #Check if path input is root, if so return root
        if not path or path == "root":
            return self.root
        #Split path into individual nodes
        parts = path.split('.')
        #Start at root node
        current = self.root
        #Iterate through nodes
        for part in parts:
            #Check if next node is a child of current node
            if part in current.children:
                current = current.children[part]
            else:
                #Return None if node not a child of current node
                return None
        #Return leaf node of path
        return current
    
    def _get_type(self, value):
        """
        Helper method to return the type of data stored at a key
        """
        #Check if value is dictionary (nested JSON object)
        if isinstance(value, dict):
            return "obj"
        #Check if value is list (array)
        elif isinstance(value, list):
            return "arr"
        #Check if value is integer
        elif isinstance(value, int):
            return "int"
        #Check if value is float
        elif isinstance(value, float):
            return "float"
        #Check if value is a string (date or string)
        elif isinstance(value, str):
            #Call helper method to check if string contains a date
            if self._is_date(value):
                return "date"
            #String does not contain a date
            else:
                return "str"
        else:
            #Fallback method, return type of value if not one included
            return type(value).__name__
        
    def _is_date(self, s):       
       """
       Helper method to check if a string is a date based on regular expression
       """
       #return boolean based on if input string is date
       return bool(re.match(r"\d{4}-\d{2}\d{2}", s))
    
    def insert_document(self, doc):
        """
        Method used to insert a document into data guide
        """
        #Check if JSON file contains multiple documents
        if isinstance(doc, list):
            #Iterate over documents in file
            for d in doc:
                self.total_docs += 1
                self._insert_value(self.root, d)
        #If single document
        elif isinstance(doc, dict):
            self.total_docs += 1
            self._insert_value(self.root, doc)

    def _insert_value(self, node, value):
        """
        Helper method to insert a single value, called recursively on objects and arrays
        """
        #Check if current value is a dictionary (nested JSON object)
        if isinstance(value, dict):
            #Increment object counter
            node.update_counter("obj")
            #Iterate over keys and subvalues contained in object
            for key, subvalue in value.items():
                #Add key if not already present
                if key not in node.children:
                    node.children[key] = Node()
                #Recusive call for children
                self._insert_value(node.children[key], subvalue)
        #Check if current value is a list (array)
        elif isinstance(value, list):
            #Increment array counter
            node.update_counter("arr")
            #Add * to children if not already present
            if "*" not in node.children:
                node.children["*"] = Node()
            #Iterate over array elements
            for element in value:
                #Recursive call for array elements
                self._insert_value(node.children["*"], element)
        #Value is not object or array
        else:
            #Return type of value
            type_name = self._get_type(value)
            #Increase counter for value
            node.update_counter(type_name)
    
    def delete_document(self, doc):
        """
        Method to delete document from data guide
        """
        #Decrement document counter, ensure negative document amount does not occur
        self.total_docs = max(0, self.total_docs - 1)
        #Call helper method to update data guide
        self._delete_value(self.root, doc)

    def _delete_value(self, node, value):
        """
        Helper method to delete keys and decrement counters for a document
        """
        #Check if value is a dictionary (nested JSON object)
        if isinstance(value, dict):
            #Decrement object counter
            node.update_counter("obj", delta=-1)
            #Initialization of list to store keys to be removed
            keys_to_delete = []
            #Iterate over key value pairs
            for key, subvalue in value.items():
                #Check if key is in current nodes children
                if key in node.children:
                    #Recursive call to function for children nodes
                    self._delete_value(node.children[key], subvalue)
                    #Check if all counters are zero and node does not have any children
                    if all(count <= 0 for count in node.children[key].counters.values()) and not node.children[key].children:
                        #Add key to list for deletion
                        keys_to_delete.append(key)
            #Iterate of keys in list
            for key in keys_to_delete:
                #Remove key from children list
                del node.children[key]
        #Check if value is a list (array)
        elif isinstance(value, list):
            #Decrement array counter
            node.update_counter("arr", delta=-1)
            #Check for values stored in array
            if "*" in node.children:
                #Iterate over values stored in array
                for element in value:
                    #Recursive call to function for array elements
                    self._delete_value(node.children["*"], element)
                #Check if all counters are zero and array node does not have children
                if all(count <= 0 for count in node.children["*"].counters.values()) and not node.children["*"].children:
                    #Delete array children
                    del node.children["*"]
        #Not object or array
        else:
            #Return type stored
            type_name = self._get_type(value)
            #Update counter of type stored
            node.update_counter(type_name, delta=-1)
        
    def print_guide(self):
        """
        Method to print the data stored in a dataguide
        """
        #Submethod to print individual node in data guide
        def _print_node(node, path="root"):
            #Print key and counters dictionary for node
            print(f"{path}: {node.counters}")
            #Recursive call to function for child nodes
            for key, child in node.children.items():
                _print_node(child, path + "." + key)
        #Start by printing root node
        _print_node(self.root)

    def clear(self):
        """
        Method to clear dataguide when debugging
        """
        #Reset root node
        self.root = Node()
        #Reset total docs counter
        self.total_docs = 0

    def save(self, filename):
        """
        Method to save data guide as text file
        """
        #Open/Create file
        with open(filename, "w") as f:
            #Dump data guide contents to file as dictionary
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        """
        Method to convert data guide to dictionary for output
        """
        #Recursive call to iterate through data guide and convert to dictionary
        return{
            "total_docs": self.total_docs,
            "root": self.root.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        """
        Class method to convert data guide text file to dictionary for output
        """
        #Create new data guide
        guide = cls()
        #Get total documents number from data guide text file
        guide.total_docs = d.get("total_docs", 0)
        #Set root node and recursively call function to iterate through data guide dictionary in text file
        guide.root = Node.from_dict(d.get("root", {}))
        return guide

    
    
    @classmethod
    def load(cls, filename):
        """
        Class method to load a data guide text file as a data guide object
        """
        #Open text file
        with open(filename, "r") as f:
            #Load information
            d = json.load(f)
        #Convert from dictionary to data guide object
        return cls.from_dict(d)
    
    def core(self):
        """
        Method to return core items from data guide
        -- A core item is one present in every document
        """
        #Create new data guide object for core
        core_guide = DataGuide()
        #Get total number of documents from data guide
        core_guide.total_docs = self.total_docs
        #Call extract core function to get core items
        core_guide.root = self._extract_core(self.root)
        return core_guide
    
    def _extract_core(self, node):
        """
        Helper method to check if an item appears in every document
        """
        #Create a new node to store core nodes
        new_node = Node()
        #Iterate over type counter for node to see if it has the same amount as documents present
        for type_name, count in node.counters.items():
            #Fill new node with core node items
            new_node.counters[type_name] = count if count == self.total_docs else 0
        #Iterate over children of node
        for key, child in node.children.items():
            #Recursive call on child nodes
            core_child = self._extract_core(child)
            #Add core children to core node if a core child
            if any(val == self.total_docs for val in child.counters.values()):
                new_node.children[key] = core_child
        return new_node
    
    def card(self, path=None):
        """
        Method to extract cardinality from data guide
        """
        #If no path is input, compute cardinality of root
        if path is None:
            node = self.root
        #Path is input
        else:
            #Traverse input path
            node = self._traverse_path(path)
            #If node holds no values return empty counters dictionary
            if node is None:
                return counters()
        #Call sum counters method
        return self._sum_counters(node)
    
    def _sum_counters(self, node):
        """
        Method to return the sum of counters for path or data guide
        """
        #Create empty total dictionary
        total = {}
        #Iterate over key value pairs at node
        for key, value in node.counters.items():
            #Store key and sum counters
            total[key] = total.get(key, 0) + value
        #Iterate over children of node
        for child in node.children.values():
            #Recusive call to function to sum child node counters
            child_sum = self._sum_counters(child)
            #Iterate over key value pairs in child sum dictionary
            for key, value in child_sum.items():
                #Store key and sum counters
                total[key] = total.get(key, 0) + value
        return total
