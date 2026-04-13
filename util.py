from z3 import Solver,BoolRef

def checkSatWith(solver : Solver,constraints : list[BoolRef]) -> str:
    """
    Add `constraints` to the assertion stack of `solver`, checks for satisfiability, and returns the result. 
    The state of the assertion stack is restored upon termination.
    """
    solver.push()
    solver.add(constraints)
    result = str(solver.check())
    solver.pop()
    return result

