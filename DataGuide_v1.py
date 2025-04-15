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

class DataGuide:
     def __init__(self):
        """
        Initialization method for DataGuide
        """
        self.root = Node()
        self.total_docs = 0