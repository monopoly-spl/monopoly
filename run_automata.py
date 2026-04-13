from automataPL import *
from metamodel import atLeast2ClassesWithAtLeast4Fields
from plotting import *

automataPL = VariationalMetamodel(features,autopl,featModelConstraints)    

automata_analysis_task = AnalysisInstance(automataPL, atLeast2ClassesWithAtLeast4Fields)

automata_analysis_task.analyze("automata_results.csv")

plot_results("automata_results.csv", 'rq1_aut.pdf')
plot_generalization_power("automata_results.csv", 'rq2_aut.pdf')