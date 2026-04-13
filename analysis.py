"""
This file defines the general analysis procedure for analyzing product lines over monotone domains. 
To use the procedure, one must provide an instance of the `AnalysisInstance` class.
"""

from variational import Variational, checkSatWith
from z3 import BoolVal, Not, Or, sat, And, simplify
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import csv 

def count_models(solver, vars, closure):
    count = 0
    solver.push()
    solver.add(closure)

    while solver.check() == sat:     
        m = solver.model()
        count += 1 

        solver.add(Not(And([
        v == m.eval(v, model_completion=True)
        for v in vars
        ])))
    solver.pop()
    
    return count 


def save_results(records, total_size, filename="results.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "iteration",
                "result",
                "new_products",
                "closure_products",  
                "cumulative_products"
            ]
        )
        writer.writeheader()
        writer.writerows(records)

        # Optional: summary row
        writer.writerow({})
        writer.writerow({
            "iteration": "TOTAL",
            "result": "",
            "new_products": total_size,
            "cumulative_products": total_size
        })

class AnalysisInstance():
    """
    Class for defining a particular kind of product line analysis problem. 
    Requires: 
    - a `productLine`, which is itself an instance of a subclass of the `Variational` parent class 
    - an `analysis`, i.e., a procedure that takes a product (of the type represented in `productLine`) and returns a Boolean result 
    """

    def __init__(self, productLine : Variational, analysis, flip=False):
        self.productLine = productLine
        self.analysis = analysis        
        # Note that the solver provided by 'productLine' is already initialized with feature model constraints
        self.solver = productLine.solver
        self.flip = flip

    def done(self,explored):
        return checkSatWith(self.solver,Not(explored)) == 'unsat'

        
    def analyze(self,filename): 
        
        explored = BoolVal(False)
        num_iter = 0
        total_size = 0
        # print()

        data = []

        while self.done(explored) == False:
            num_iter +=1 
            # print(f"beginning iteration {num_iter}")
            p = self.productLine.sampleProduct(Not(explored))
            result = self.analysis(p)

            if result:
                # print(f"analysis succeeds on product")
                # target = "upward" if not self.flip else "downward"
                # print(f"computing {target} closure (easier problems)")
                if self.flip:
                    closure = self.productLine.downward(p)
                else: 
                    closure = self.productLine.upward(p)             
            else: 
                # print(f"analysis failed on product")
                # target = "downward" if not self.flip else "upward"
                # print(f"computing {target} closure (harder problems)")
                if self.flip:
                    closure = self.productLine.upward(p)
                else: 
                    closure = self.productLine.downward(p)

            size = count_models(self.solver,self.productLine.features,And(Not(explored),closure))
            total_closure_size = count_models(
                self.solver,
                self.productLine.features,
                closure
            )
            total_size += size
            # print(f"closure generalizes result to {size} new products")
            explored = Or(explored, closure)

            data.append({
            "iteration": num_iter,
            "result": bool(result),   
            "new_products": size,
            "closure_products": total_closure_size,   
            "cumulative_products": total_size
            })

            # print()

        # print(f"analysis complete after directly analyzing {num_iter} products")
        # print(f"analysis complete after indirectly analyzing {total_size} products")
        # print()

        save_results(data,total_size,filename)
