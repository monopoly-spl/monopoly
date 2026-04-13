from GPL import *
from plotting import * 
from analysis import *

GPL = VariationalMetamodel(features=gplFeatures,model=gpl_,featModel=GPLFeatModelConstraints)

gpl_analysis_instance = AnalysisInstance(GPL, atLeast2ClassesWithAtLeast4Fields)

gpl_analysis_instance.analyze("GPL_results.csv")

plot_results("gpl_results.csv", 'rq1_gpl.pdf')
plot_generalization_power("gpl_results.csv", 'rq2_gpl.pdf')
