
# Libraries

from statistics import mean
from collections import Counter


# In[2]:


class Explainer:
    
    def __init__(self, name, explainer_properties):
        """
            explainer: the name of the explainer
            properties: the key-values that represent the properties of the explainer
        """
        # name of the explainers
        self.name = name
        # dictionary with the explainer properties
        self.properties = explainer_properties
        
    def explainerName(self):
        return self.name
    
    def explainerProperties(self):
        return self.properties
    
    def printProperties(self):
        properties_print = ""
        
        for prop in self.properties.items():
            properties_print = properties_print + prop[0] + ": " + prop[1] + "; "
            
        return properties_print
    
    def printExplainer(self):
        print("My explainer is " + self.explainerName() + " and its properties are " + self.printProperties())
        
    def explainerPropertyNames(self):
        """
            returns the names of the explainer properties
        """
        return list(self.properties.keys())
    
    def get_property_value(self, propertyName):
        """
            propertyName is a a property that this Explainer has to have
        """
        myValue = self.properties.get(propertyName)
        if myValue == None:
            print("The explainer " + explainerName(self) + " has not got the property " + propertyName)
        else:
            return myValue
        


class ExplanationStrategy:
    
    def __init__(self, explainers_input, structure_input={}):  
        """
            explainers -> dictionary of explainers that the strategy has. This has to be a list of keys1-values1: keys1,
            the name of the explainer, values1: the keys2-values2 properties for each explainer. 
            The keys2 can be customised but all the explainers should have the same names.
            
            Only needed when the structure of the strategy is a behaviour tree
            structure={"nodes":[],"adj":[]} has the tree structure: list of nodes and the adjacency list
            
            returns a list of Explainers, and a list of the property names
        """    
        
        # If everything is right, we create Explainer objects
        # list of explainers
        self.explainers = [Explainer(explainer[0], explainer[1]) for explainer in explainers_input.items()]
        
        # check if all the explainers have the same property names
        fst_explainer_props = self.explainers[0].explainerPropertyNames()
        
        i = 0
        foundError = False
        self.properties_explainers = list()
        while i < len(self.explainers) and foundError == False:
            if fst_explainer_props != self.explainers[i].explainerPropertyNames():
                raise Exception("Error: the explainer property names have to be the same for all the explainers in the strategy.")
                foundError = True
            else:
                i = i + 1
        
        self.properties_explainers = fst_explainer_props
        self.structure = structure_input
        if structure_input != {}:
            self.supplement = len([x for x in structure_input["nodes"] if x == "Supplement"]) 
            self.replacement = len([x for x in structure_input["nodes"] if x == "Replacement"]) 
            self.variant = len([x for x in structure_input["nodes"] if x == "Variant"]) 
            self.complement = len([x for x in structure_input["nodes"] if x == "Complement"]) 
        else:
            self.supplement = 0
            self.replacement = 0
            self.variant = 0
            self.complement = 0
      
    
    def getExplainers(self):
        return self.explainers
    
    def getExplainersNames(self):
        return [e.explainerName() for e in self.explainers]
    
    def getPropertyNames(self):
        return self.properties_explainers
    
    def getSupplementNodes(self):
        return self.supplement
    
    def getReplacementNodes(self):
        return self.replacement
    
    def getVariantNodes(self):
        return self.variant
    
    def getComplementNodes(self):
        return self.complement
    
    def numberElements(self):
        """
            It returns the number of elements that form the strategy regarding the elements involved
            in completeness and diversity
        """
        numElements = len(self.explainers) + self.supplement + self.replacement + self.variant + self.complement
        return numElements
    
    def getExplainerByName(self, name):
        """
            Get a specific explainer
        """
        i = 0
        found = False
        my_explainer = ""
        
        while i < len(self.explainers) and found == False:
            if self.explainers[i].explainerName() == name:
                my_explainer = self.explainers[i]
                found = True
            else:
                i = i + 1
        
        return my_explainer
    
    
    def getExplainerPropValue(self, my_explainer, my_property):
        """
            Get the value of a specific explainer for a specific property in the strategy
        """
        specific_explainer = self.getExplainerByName(my_explainer)
        value_property = specific_explainer.get_property_value(my_property)
        
        return value_property  
    
    
    def getAllValueProperty(self, my_property):
        """
            Get all the property values in all the explainers for a specific property
        """
        
        my_values = list()
        
        for explainer in self.explainers:
            my_values.append(explainer.get_property_value(my_property))
            
        return my_values
    
    def numberNodes(self):
        """
            Returns the number of nodes in the tree
        """
        return len(self.structure["nodes"]) 
        
    def numberExplainers(self):
        """
            Returns the number of explainers in the tree
        """  
        return len(self.explainers)
        
    def numberConditionNodes(self):
        """
            Returns a dictionary where we find the different of condition nodes that we have in the tree
            In an iSee BT we have sequence nodes, priority nodes, variant, replacement, complement, supplement
        """
        priority_nodes = len([x for x in self.structure["nodes"] if x == "Priority"]) 
        sequence_nodes = len([x for x in self.structure["nodes"] if x == "Sequence"])
        
        return priority_nodes + sequence_nodes + self.getVariantNodes() + self.getReplacementNodes() + self.getComplementNodes() + self.getSupplementNodes()
        
    def numberQuestionNodes(self):
        """
            Returns the number of questions in the tree 
        """ 
        return len([x for x in self.structure["nodes"] if x not in self.getExplainersNames() and x not in ["root","Priority", "Sequence", "Variant", "Replacement", "Complement", "Supplement"]])
        
    def adjacencyLength(self):
        """
            Returns the number of connections in the BT
        """
        
        return len([x for x in self.structure["adj"] if x != []])   
    




# # Evaluation metrics
COMPUTATIONAL_COMPLEXITY_VALUES = ["constant_time", "logarithmic_time", "linear_time", "log_linear_time", "quadratic_time", "polynomial_time", "exponential_time", "factorial_time"]
cc_enum = enumerate(COMPUTATIONAL_COMPLEXITY_VALUES)
CC_LIST = list(cc_enum)
# print(CC_LIST)



def raiseExceptionNotProperty(my_property, explanation_strategy):
    if my_property not in explanation_strategy.getPropertyNames():
        msg = "The property " + my_property + " has to be included for all the explainers in the strategy."
        raise Exception(msg)
    

def getComputationalComplexityEnumValue(cc_value):
    value = [cc[0] for cc in CC_LIST if cc[1] == cc_value]
    if value == []:
        raise Exception("The value " + cc_value + " is not a proper value for computational complexity. Please look over the following proper values: constant_time, logarithmic_time, linear_time, log_logarithmic_time, linearithmic_time, quadratic_time, polynomial_time, exponential_time, factorial_time")
    return value[0]

def timeliness(explanation_strategy):
    """
        To execute this metric, the explanations in the explanation strategy have to have 
        computational_complexity as a property, and the possible values for this property should be among the following:
        
        constant_time - (O(1))
        logarithmic_time - (O(log n))
        linear_time - (O(n))
        log_linear_time - (O(n log n))
        quadratic_time - (O(n^2))
        polynomial_time - (O(n^a) when a > 2)
        exponential_time - (O(a^n) when a > 2)
        factorial_time - (O(n!))
               
               
        It returns the highest computational complexity of all the explainers within the explanation strategy 
    """
    
    raiseExceptionNotProperty("computational_complexity", explanation_strategy)
        
    comput_complex_values = explanation_strategy.getAllValueProperty("computational_complexity")
    
    cc_value = 0
    i = 0
    found = False
    while i < len(comput_complex_values) and found == False:
        cc_current_value = getComputationalComplexityEnumValue(comput_complex_values[i])
        if cc_current_value == CC_LIST[-1][0]: # this means it is the highest value and we dont need to check more
            found = True
            cc_value = cc_current_value
        else:
            i = i + 1
            if cc_current_value > cc_value:
                cc_value = cc_current_value
                
    return cc_value/CC_LIST[-1][0]


def popularity(explanation_strategy, min_popularity, max_popularity):
    """
        It returns the mean popularity of all the explainers in the strategy
        The explainers have to include the property popularity.
        Moreover, min_popularity and max_popularity are the range of the popularity values
    """
    raiseExceptionNotProperty("popularity", explanation_strategy)
    
    #print(explanation_strategy.getAllValueProperty("popularity"))
    popularity_values_mean = mean(explanation_strategy.getAllValueProperty("popularity"))
    
    # normalisation (value - min)/(max - min) 
    return (popularity_values_mean - min_popularity)/(max_popularity - min_popularity)


def completeness_plain(explanation_strategy):
    """
        This function is an auxiliar function to be used in diversity and completeness. 
        It is going to retrieve the completeness value, i.e. how the score that says if the explainers 
        in an explanation strategy are equals
        0: totally diverse
        1: totally complete
    """
    compl_score_tmp = 0
    for explainer_property in explanation_strategy.getPropertyNames():
        my_values = Counter(explanation_strategy.getAllValueProperty(explainer_property))
        count = 0
        for key, value in my_values.items():
            count = count + (value - 1)
        denominator = (len(explanation_strategy.getExplainers()) - 1) 
        mean = 1
        if denominator != 0:
            mean = count/denominator
        compl_score_tmp = compl_score_tmp + mean
    compl_score = compl_score_tmp/len(explanation_strategy.getPropertyNames())
    
    return compl_score




# ### Type of condition nodes that affect completness and diversity:
# - Replacement: The children nodes offer explanations that are completely different from each other
# - Variant: Right sibling(s) generate explanations that clarify explanations generated by the left sibling(s). Example: alternative visualisation with more information
# - Complement: Right sibling(s) generate explanations that provides a different perspective to the explanations generated by the left sibling(s).
# - Supplement: Right sibling(s) generate explanations that provide more information to the  explanations generated by the left sibling(s). Ex: DiCE presenting an additional counterfactual
#


def conditionNodesScores(explanation_strategy):
    supplement_score = explanation_strategy.getSupplementNodes()/explanation_strategy.numberElements() * 0.1 
    replacement_score = explanation_strategy.getReplacementNodes()/explanation_strategy.numberElements() * 0.1 
    variant_score = explanation_strategy.getVariantNodes()/explanation_strategy.numberElements() * 0.1 
    complement_score = explanation_strategy.getComplementNodes()/explanation_strategy.numberElements() * 0.1 
    
    return supplement_score, replacement_score, variant_score, complement_score


def completeness(explanation_strategy):
    """
        Returns a score that decides the level of completeness of the strategy
        Completeness can be enhanced if the strategy includes variant and/or supplement nodes
        it can be decreased if the strategy includes replacement and/or complement nodes
        It is symmetric with diversity
        It returns a value between 0 (totally diverse) and 1 (totally complete)
    """
    
    supplement_score,replacement_score,variant_score,complement_score = conditionNodesScores(explanation_strategy)
    
    score_temp = completeness_plain(explanation_strategy)
    completness_score_tmp = score_temp + variant_score + supplement_score - replacement_score - complement_score
        
    return completness_score_tmp


def diversity(explanation_strategy):
    """
        Returns a score that decides the level of diversity of the strategy
        Diversity can be decreased if the strategy includes variant and/or supplement nodes
        it can be enhanced if the strategy includes replacement and/or complement nodes
        It is symmetric with completeness
        It returns a value between 0 (totally complete) and 1 (totally diverse)
    """
    return 1 - completeness(explanation_strategy)


def serendipity(explanation_strategy):
    """
        It measures if there is 1/4 of the explainer in the strategy that are different from the rest of explainers 
        to surprise the users. 
        We need to check all the properties of each explainer. If the explainer is very different from the rest 
        (i.e. 1/4 of its properties is different form the rest):
        serendipity = true, else = false
    """
    properties = explanation_strategy.getPropertyNames()
    
    # this is the number of properties that has to be different so the explainer is selected as it has serendipity
    properties_needed_serendipity = len(properties) - int(len(properties)/4)
    
    explainers = explanation_strategy.getExplainersNames()
    # I am going to keep a dictionary pairs where 
    # key=property, value=list[explainers that are different for this property]
    serendipity_values = {}
    for my_property in properties:
        
        property_explainers = explanation_strategy.getAllValueProperty(my_property)
        
        my_values = dict(Counter(property_explainers))
        
        serendipity_values[my_property] = []
        # 1. from my_values get the last element (or even the second to last etc if they have the same number
        # of ocurrences)
        if len(my_values) != 1 and min(list(my_values.values())) == 1:
            my_keys = [key for key, value in my_values.items() if value == 1] 
            
            # 2. See where that value is, i.e. which explainer has that value for this property
            explainers_serendipity_prop = [explainer for explainer in explainers if explanation_strategy.getExplainerPropValue(explainer, my_property) in my_keys] 
            
            # 3. save the data in the dictionary serendipity_values
            serendipity_values[my_property] = explainers_serendipity_prop
    
    serendipity_values_tmp = serendipity_values.values()
    # we need to do a counter for the list of lists, and check if there is one explainer that appears in all 
    # the properties or at least in properties_needed_serendipity
    
    candidates_explainers_serendipity = list(set([explainer for candidates in serendipity_values_tmp for explainer in candidates]))
    
    # we crate a dictionary with the times that the candidates appear in the lists
    candidates = {explainer: 0 for explainer in candidates_explainers_serendipity}
    
    for list_property in serendipity_values_tmp: 
        for candidate in candidates.keys():
            if candidate in list_property:
                candidates[candidate] = candidates[candidate] + 1
                
    serendipity_explainers = [explainer for explainer in candidates.keys() if candidates[explainer] >= properties_needed_serendipity]
    
    if len(serendipity_explainers) <= (len(properties) - properties_needed_serendipity) and len(serendipity_explainers) != 0:
        return (True, "The explainers that are a surprise are " + str(serendipity_explainers))
    else:
        return (False, "No serendipity")


def granularity(explanation_strategy):
    """
    Clarification: this is not a metric [0,1] is a measure (the higher the granularity is, the higher the score is)
    
        This measure measures the level of detail of the strategy considering its types of nodes and connections
        the more the number of connections are, the more the number
        of nodes are, the higher the granularity score is
        we give more importance to number of connections and number of explainers
    """
    
    nodes = explanation_strategy.numberNodes()
    
    adj = explanation_strategy.adjacencyLength()/nodes * 0.5 #
    explainers = (explanation_strategy.numberExplainers()/nodes) * 0.3
    conditions = (explanation_strategy.numberConditionNodes()/nodes) * 0.1
    questions = (explanation_strategy.numberQuestionNodes()/nodes) * 0.1
    
    
    return explainers + conditions + questions + adj





