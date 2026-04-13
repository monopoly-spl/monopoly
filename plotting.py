import csv
from matplotlib import pyplot as plt


## RQ1 Plotting
def plot_results(csv_file, filename):
    plt.figure(figsize=(9, 4.8))
    plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15
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

    true_x = [x for x, s in zip(iterations, styles) if s]
    true_y = [y for y, s in zip(cumulative_values, styles) if s]

    false_x = [x for x, s in zip(iterations, styles) if not s]
    false_y = [y for y, s in zip(cumulative_values, styles) if not s]

    plt.plot(iterations, cumulative_values, linestyle='-', color='black', alpha=0.6)
    plt.scatter(true_x, true_y, marker='x', color='green', label="Satsfied")
    plt.scatter(false_x, false_y, marker='o', facecolors='none', edgecolors='red', label="Violated")
    plt.legend(loc="lower right")
    plt.xlabel("Iteration")
    plt.ylabel("Cumulative Products Analyzed")
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig(filename)
    plt.close()


## RQ2 Plotting
def plot_generalization_power(csv_file, filename):

    plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15
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

    true_x = [x for x, s in zip(iterations, styles) if s]
    true_y = [y for y, s in zip(closure_values, styles) if s]

    false_x = [x for x, s in zip(iterations, styles) if not s]
    false_y = [y for y, s in zip(closure_values, styles) if not s]

    plt.scatter(true_x, true_y, marker='x', color='green', label="Satisfied")
    plt.scatter(false_x, false_y, marker='o', facecolors='none', edgecolors='red', label="Violated")

    plt.xlabel("Iteration")
    plt.ylabel("Number of Pruned Configurations")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    # plt.show()
    plt.savefig(filename)
    plt.close()
