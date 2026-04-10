import csv 
from matplotlib import pyplot as plt

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