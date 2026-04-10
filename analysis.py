"""
This file defines the general analysis procedure for analyzing product lines over monotone domains. 
To use the procedure, one must provide an instance of the `AnalysisInstance` class.
"""

from variational import Variational, checkSatWith
from z3 import BoolVal, Not, Or, sat, And, simplify
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import csv 

# def plot_results(total_products,csv_file="results.csv"):
#     iterations = []
#     percentages = []
#     colors = []

#     with open(csv_file, "r") as f:
#         reader = csv.DictReader(f)

#         for row in reader:
#             # skip summary or empty rows
#             if not row["iteration"].isdigit():
#                 continue

#             iteration = int(row["iteration"])
#             cumulative = int(row["cumulative_products"])
#             result = row["result"] == "True"

#             pct = (cumulative / total_products) * 100

#             iterations.append(iteration)
#             percentages.append(pct)
#             colors.append("green" if result else "red")

#     # Plot line
#     plt.plot(iterations, percentages, linestyle='-', color='black', alpha=0.6)

#     # Plot colored points
#     for x, y, c in zip(iterations, percentages, colors):
#         plt.scatter(x, y, color=c)
    

#     plt.xlabel("Number of Analysis Invocations")
#     plt.ylabel("Configurations Analyzed (% of Valid Configurationss)")
#     # plt.title("Configuration Coverage (Cumulative)")

#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

def count_models(solver, vars, closure):
    count = 0
    # print(solver.assertions())
    # return
    solver.push()
    solver.add(closure)

    while solver.check() == sat:     
        m = solver.model()
        count += 1 

        solver.add(Not(And([
        v == m.eval(v, model_completion=True)
        for v in vars
        ])))
        # if count % 500 == 0:
            # print(f"{count}")
        # print(solver.assertions())
    solver.pop()
    
    return count 

# def plot_generalization_power(csv_file, total_products):
#     iterations = []
#     percentages = []
#     colors = []

#     with open(csv_file, "r") as f:
#         reader = csv.DictReader(f)

#         for row in reader:
#             if not row["iteration"].isdigit():
#                 continue

#             iteration = int(row["iteration"])
#             closure_size = int(row["closure_products"])
#             result = row["result"] == "True"

#             pct = (closure_size / total_products) * 100

#             iterations.append(iteration)
#             percentages.append(pct)
#             colors.append("green" if result else "red")

#     # Line (optional but nice)
#     plt.plot(iterations, percentages, linestyle='-', color='black', alpha=0.6)

#     # Colored dots
#     for x, y, c in zip(iterations, percentages, colors):
#         plt.scatter(x, y, color=c)

#     plt.xlabel("Number of Analysis Invocations")
#     plt.ylabel("Closure Size (% of Valid Configurations)")
#     # plt.title("Size of Analysis Generalizations")
#     plt.ylim(0, 100)

#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

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

    # def getClosureExpression(self,result):
        
    def analyze(self): 
        
        explored = BoolVal(False)
        num_iter = 0
        total_size = 0
        print()

        data = []

        while self.done(explored) == False:
            num_iter +=1 
            print(f"beginning iteration {num_iter}")
            p = self.productLine.sampleProduct(Not(explored))
            result = self.analysis(p)

            if result:
                print(f"analysis succeeds on product")
                target = "upward" if not self.flip else "downward"
                print(f"computing {target} closure (easier problems)")
                if self.flip:
                    closure = self.productLine.downward(p)
                else: 
                    closure = self.productLine.upward(p)             
            else: 
                print(f"analysis failed on product")
                target = "downward" if not self.flip else "upward"
                print(f"computing {target} closure (harder problems)")
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
            print(f"closure generalizes result to {size} new products")
            explored = Or(explored, closure)

            data.append({
            "iteration": num_iter,
            "result": bool(result),   
            "new_products": size,
            "closure_products": total_closure_size,   
            "cumulative_products": total_size
            })

            print()

        print(f"analysis complete after directly analyzing {num_iter} products")
        print(f"analysis complete after indirectly analyzing {total_size} products")
        print()

        save_results(data,total_size,filename="results.csv")
        plot_results(total_size)
        plot_generalization_power("results.csv",total_size)


# 3744 : automata
def plot_comparison_separate(csv_a, csv_b, total_products_a, total_products_b):

    def load_data(csv_file, total_products):
        iterations = []
        cumulative_pct = []
        closure_pct = []
        colors = []

        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if not row["iteration"].isdigit():
                    continue

                iteration = int(row["iteration"])
                cumulative = int(row["cumulative_products"])
                closure = int(row["closure_products"])
                result = row["result"] == "True"

                iterations.append(iteration)
                cumulative_pct.append((cumulative / total_products) * 100)
                closure_pct.append((closure / total_products) * 100)
                colors.append("green" if result else "red")

        return iterations, cumulative_pct, closure_pct, colors

    # Load data
    it_a, cum_a, clo_a, col_a = load_data(csv_a, total_products_a)
    it_b, cum_b, clo_b, col_b = load_data(csv_b, total_products_b)

    # =========================
    # GRAPH 1: CUMULATIVE
    # =========================
    plt.figure(figsize=(9, 5))

    # lines
    plt.plot(it_a, cum_a, color='black', alpha=0.5, linestyle='-')
    plt.plot(it_b, cum_b, color='black', alpha=0.5, linestyle='--')

    # points
    for x, y, c in zip(it_a, cum_a, col_a):
        plt.scatter(x, y, color=c, marker='o', s=50)

    for x, y, c in zip(it_b, cum_b, col_b):
        plt.scatter(x, y, color=c, marker='s', s=50)

    plt.xlabel("Number of Analysis Invocations")
    plt.ylabel("Cumulative Coverage (% of Valid Configurations)")
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Automata',
               markerfacecolor='black', markersize=8),
        Line2D([0], [0], marker='s', color='w', label='GPL',
               markerfacecolor='black', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Positive',
               markerfacecolor='green', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Negative',
               markerfacecolor='red', markersize=8),
    ]

    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.show()

    # =========================
    # GRAPH 2: GENERALIZATION
    # =========================
    plt.figure(figsize=(9, 5))

    # lines
    plt.plot(it_a, clo_a, color='black', alpha=0.5, linestyle='-')
    plt.plot(it_b, clo_b, color='black', alpha=0.5, linestyle='--')

    # points
    for x, y, c in zip(it_a, clo_a, col_a):
        plt.scatter(x, y, color=c, marker='o', s=50)

    for x, y, c in zip(it_b, clo_b, col_b):
        plt.scatter(x, y, color=c, marker='s', s=50)

    plt.xlabel("Number of Analysis Invocations")
    plt.ylabel("Size of Generalization (% of Valid Products)")
    plt.ylim(0, 100)
    # plt.title("Generalization Power Comparison")
    plt.grid(True, alpha=0.3)

    plt.legend(handles=legend_elements)
    plt.tight_layout()
    plt.show()

# plot_comparison_separate("automata.csv", "gpl.csv", 3744, 840)

## RQ1 Plotting
def plot_results(csv_file):
    plt.rcParams.update({
    "font.size": 12,        
    "axes.labelsize": 14,  
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
    })
    iterations = []
    cumulative_values = []
    styles = []

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if not row["iteration"].isdigit():
                continue

            iteration = int(row["iteration"])
            cumulative = int(row["cumulative_products"])
            result = row["result"] == "True"

            iterations.append(iteration)
            cumulative_values.append(cumulative)
            styles.append(result)

    plt.plot(iterations, cumulative_values, linestyle='-', color='black', alpha=0.6)

    # markers depend on analysis returning true/false
    for x, y, is_true in zip(iterations, cumulative_values, styles):
        if is_true:
            plt.scatter(x, y, marker='o', color='black')  # filled
        else:
            plt.scatter(x, y, marker='o', facecolors='none', edgecolors='black')  # empty

    plt.xlabel("Number of Analysis Invocations")
    plt.ylabel("Cumulative Products Analyzed")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

## RQ2 Plotting
def plot_generalization_power(csv_file):
    plt.rcParams.update({
    "font.size": 12,        # base size
    "axes.labelsize": 14,   # axis labels
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
    })
    iterations = []
    closure_values = []
    styles = []

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if not row["iteration"].isdigit():
                continue

            iteration = int(row["iteration"])
            closure_size = int(row["closure_products"])
            result = row["result"] == "True"

            iterations.append(iteration)
            closure_values.append(closure_size)
            styles.append(result)

    # markers depend on analysis returning true/false
    for x, y, is_true in zip(iterations, closure_values, styles):
        if is_true:
            plt.scatter(x, y, marker='o', color='black')  
        else:
            plt.scatter(x, y, marker='o', facecolors='none', edgecolors='black')  

    plt.xlabel("Number of Analysis Invocations")
    plt.ylabel("Number of Applicable Products")
    plt.grid(True)
    plt.tight_layout()
    plt.show()