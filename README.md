## Analyzing Product Lines with Monotonicity

Install requirements: `pip install -r requirements.txt`
 
#### Contents 
```text
monopoly/
├── analysis.py (main analysis procedure)
├── automataPL.py (encoding of Automata metamodel product line)
├── GPL.py (encoding of GPL metamodel product line)
├── metamodel.py (definition of (product) metamodel class)
├── plotting.py (plotting scripts)
├── README.md 
├── requirements.txt
├── run_automata.py (script to run analysis over Automata product line)
├── run_gpl.py (script to run analysis over GPL product line)
├── util.py (misc. utility scripts)
├── variational.py  (abstract parent class for product line objects)
├── varset.py (class of variational sets)
└── vmetamodel.py (definition of variational metamodel class)
```


#### Instructions to Reproduce Experiments

Use the following commands to run the sample analysis on the two metamodel product lines and plot the results. 

 - `python run_automata.py` : stores analysis result in `automata_results.csv` file, plots stored as `rq1_aut.pdf` and `rq2_aut.pdf`
 - `python run_gpl.py` : stores analysis result in `gpl_results.csv` file, plots stored as `rq1_gpl.pdf` and `rq2_gpl.pdf`

Note that, due to potential nondeterminism in theorem proving behaviour, the quantitative results obtained may vary slightly between different instances.