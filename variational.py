"""
This file defines the `Variational` class, which is a generic class for variational datatypes (i.e., product lines). 
It defines a small number of abstract methods that need to be implemented for each product line type.
"""

from abc import ABC, abstractmethod
from z3 import Solver, Not, BoolRef, BoolVal
from util import checkSatWith

class Variational(ABC):
    """
    The parent class of variational types (product lines).
    Each instance requires:
    - a set of `features` 
    - a `model`, i.e., some data structure with variability annotations over the given language of features
    - a feature model `featModel` describing the set of valid features
    
    Note that (for now) we are representing features as z3 Boolean variables and feature expressions as z3 Boolean Expressions

    Each instance of the `Variational` class also carries around a z3 solver to handle various sat-checking operations.
    """
    def __init__(self, 
                 features: list[BoolRef], 
                 model, 
                 featModel: BoolRef):
        """
        Populate the variational object, and initialize the solver with feature model as an assertion 
        (so that all SAT operations are taken in conjuction with the feature model)
        """
        self.model = model 
        self.features = features 
        self.featModel = featModel
        self.solver = Solver()
        self.solver.add(featModel)
    
    @abstractmethod
    def derive(self, config : set[BoolRef]):
        """
        The derivation operator: given the set of features `config`, derive from annotated PL model the product induced by `config`.

        Needs to implemented for each different type of product line.
        """
        pass

    
    def constraintsFromConfig(self,config : set[BoolRef]) -> BoolRef:
        """
        Given the configuration (set of features) `config`, return the equivalent feature expression.
        
        That is, return a conjunction which includes literal `f` for every feature `f` in `config` and 
        literal `not f` for every `f` not in `config`.
        """
        constraints = []
        for f in self.features:
            if f in config:
                constraints += [f]
            else:
                constraints += [Not(f)]
        return constraints
    
    def present(self, pc : BoolRef, config : set[BoolRef]) -> bool:
        """
        Return `True` iff the presence condition `pc` evaluates to True under `config`
        """
        result = checkSatWith(self.solver,self.constraintsFromConfig(config) + [pc])
        return True if result == 'sat' else False
    
    
    
    def sampleConfig(self, restriction : BoolRef = BoolVal(True)) -> set[BoolRef]:
        """ 
        Sample a configuration of features satisfying the feature model as well as the given `restriction` (=True by default).

        Raises an error if the conjunction of feature model and `restriction` is not satisfiable.
        """
        self.solver.push()
        self.solver.add(restriction)
        result = str(self.solver.check())
        if result == 'unsat':
            raise ValueError("No products to sample")
        else:
            assert result == 'sat'
            model = self.solver.model()
            self.solver.pop()
            config = set()
            for f in self.features:
                if model[f] == True:
                    config.add(f)
            return config       

    def sampleProduct(self,restriction : BoolRef = BoolVal(True)):
        """
        Sample a valid product from the product line model.
           
        Can provide a feature expression `restriction` which specifies a particular subset of configurations to sample from.
        """
        conf = self.sampleConfig(restriction)
        # print(conf)
        return self.derive(conf)

    @abstractmethod
    def upward(self, p):
        """
        Given the product `p`, compute the feature expression representing the upward closure of `p`.
        
        Needs to be implemented for each type of product line.
        """
        pass 

    @abstractmethod
    def downward(self,p):
        """
        Given the product `p`, compute the feature expression representing the downward closure of `p`.
        
        Needs to be implemented for each type of product line.
        """
        pass
