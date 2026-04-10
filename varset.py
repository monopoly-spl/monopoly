"""
This files defines the class (type) of variational sets, i.e, sets whose elements are annotated by presence conditions.

This class inherits from the `Variational` parent class defined in `variational.py`.

The actual representation of the set is a dictionary where each key/value pair `(k,v)` indicates that element `k` has presence condition `v`. 

That is, `k` is in the product set under some configuration only if that configurations satisfies `v`.
"""

from z3 import Solver, And, Not, BoolVal, BoolRef
from variational import Variational
from util import checkSatWith

class VarSet(Variational):
        
    def __init__(self, features : list[BoolRef], model, featModel : BoolRef):
        super().__init__(features, model, featModel)    

    def getPC(self, elem) -> BoolRef:
        """
        Get the presence condition of element `elem` in the annotated set. 
        If `elem` is not annotated, return presence condition `false` (satisfied by no configuration).
        """
        return self.model[elem] if elem in self.model.keys() else BoolVal(False)
    
    def derive(self, config : set[BoolRef]):
        """
        Derive the (ordinary) set induced by `config` by identifying the subset of elements whose 
        presence conditions are satisfied by `config`.

        Raises a `ValueError` if `config` is not valid w.r.t. the feature model.
        """
        if checkSatWith(self.solver, self.constraintsFromConfig(config)) == 'unsat':
            raise ValueError("configuration is invalid with respect to feature model")
        
        result = set()
        for (elem, pc) in self.model.items():
            self.solver.push()
            if self.present(pc, config): 
                result.add(elem)
            self.solver.pop()
        return result
    
    def upward(self, p) -> BoolRef:
        """
        The implementation of the upward closure operator for variational sets. 

        We are considering the partial order induced by set inclusion, so the upward closure 
        of set `p` is the set of all supersets of `p`. 

        We can get the associated feature expression for this set of sets by conjoining the 
        presence conditions of all elements in the set `p`.
        """
        constraints = []
        for elem in p:
            constraints += [self.getPC(elem)]
        return And(constraints) if len(constraints) > 1 else constraints[0]
    
    def downward(self, p) -> BoolRef:
        """
        The implementation of the upward closure operator for variational sets. 

        We are considering the partial order induced by set inclusion, so the upward closure 
        of set `p` is the set of all subsets of `p`. 

        We can get the associated feature expression for this set of sets by conjoining the 
        *negations* of the presence conditions of all elements *not* in the set `p`.
        """
        constraints = []
        for (elem,pc) in self.model.items():
            if elem not in p:
                constraints += [Not(pc)]
        return And(constraints) if len(constraints) > 1 else constraints[0]
    

