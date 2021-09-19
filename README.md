## metroplot - a compact alternative to pairwise significance brackets.

![Figure 1](/images/figure_1.png)

A closed dot connected to a set of open dots indicates that the condition aligned with the closed dot significantly "dominates" all of the conditions aligned with the open dots. The meaning of domination is context-dependent (e.g., significantly better accuracy, significantly lower error rate, significantly higher count and so on). This visualization convention was first introduced [here](https://doi.org/10.1073/pnas.1912334117). 

A more elaborate usage case:

![Figure 1](/images/figure_2.png)

See demo.py for how to use this code.

Requirements: matplotlib and pandas.

The demo uses also [seaborn](https://github.com/mwaskom/seaborn) (for barplots and boxplots), [statsmodels](https://github.com/statsmodels/statsmodels), and numpy. The demo data (Eysenck, 1974) is from [David Howell's website](https://www.uvm.edu/~statdhtx/methods8/DataFiles/DataSets.html).
