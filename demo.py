
from itertools import combinations

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

import seaborn as sns
import numpy as np
import pandas as pd
import statsmodels.api as sm

from metroplot import metroplot

# Metroplot usage example

# Read Eysenck (1974) table from David Howell's website
data=pd.read_csv('https://www.uvm.edu/~statdhtx/methods8/DataFiles/Tab13-2.dat',delimiter='\t')
data['Condition'] = [{1:'Counting', 2:'Rhyming', 3:'Adjective', 4:'Imagery', 5:'Intention'}[c] for c in data['Condition']]
data['Age'] = [{1:'Old', 2:'Young'}[c] for c in data['Age']]

def pairwise_ttest(data, factor, dependent):
    """ run t-tests between all levels of a factor and  """
    levels=data[factor].unique()

    # test all pairwise comparisons
    pairwise_comparisons=[]
    for level1, level2 in combinations(levels,r=2):
        a = data.loc[data[factor]==level1,dependent]
        b = data.loc[data[factor]==level2,dependent]

        t, p_value, df=sm.stats.ttest_ind(a,b)

        pairwise_comparisons.append({
            'level1':level1,
            'level2':level2,
            'effect_direction':np.sign(t),
            'p_value':p_value,
        })
    pairwise_comparisons=pd.DataFrame(pairwise_comparisons)

    # multiple comparison correction
    is_sig, corrected, _, _, = sm.stats.multipletests(pairwise_comparisons['p_value'], method='fdr_bh')

    pairwise_comparisons['is_sig'] = is_sig
    pairwise_comparisons['corrected_p_value'] = corrected # this is not currently used

    return pairwise_comparisons

pairwise_comparisons = pairwise_ttest(data, 'Condition', 'Recall')

conditions = data['Condition'].unique()

print('pairwise comparisons results:')
print(pairwise_comparisons)

fig=plt.figure(figsize=(5,4))
gs=GridSpec(2,1,height_ratios=[0.75,5],hspace=0.05,figure=fig) # we create two subplots, one for the main plot and one for the metroplot.
ax0=fig.add_subplot(gs[1])
sns.barplot(data=data,x='Condition',y='Recall',order=conditions)
sns.despine(fig)
gs.tight_layout(fig)

# # grab colors from Seaborn's barplot.
bars = [r for r in ax0.get_children() if type(r)==Rectangle]
colors = [c.get_facecolor() for c in bars[:-1]]
level_palette = {cond:color for cond, color in zip(conditions,colors)}

level_to_location = {cond:i for i, cond in enumerate(conditions)} # map categories to x axis locations.
ax1=fig.add_subplot(gs[0])
metroplot(pairwise_comparisons,level_to_location=level_to_location,metroplot_element_order=conditions,
                                ax=ax1,level_axis='x',dominating_effect_direction=1,
                                level_pallete=level_palette, level_axis_lim=ax0.get_xlim())
# # note that level_axis_lim=ax0.get_xlim() aligns the metrplot with the main plot

# %%
# a slightly more complicated example

fig=plt.figure(figsize=(6,6))
gs=GridSpec(1,2,width_ratios=[4,2.5],wspace=0.01, figure=fig)
ax0=fig.add_subplot(gs[0])

data['Group']=[cond + ' ' + age for age, cond in zip(data['Age'],data['Condition'])]
level_palette={'Counting':'#a6cee3', 'Rhyming':'#1f78b4', 'Adjective':'#b2df8a', 'Imagery':'#33a02c', 'Intention':'#fb9a99'}

pairwise_comparisons = pairwise_ttest(data, 'Group', 'Recall')

print('pairwise comparisons results:')
print(pairwise_comparisons)

conditions = data['Group'].unique()
conditions.sort()

sns.boxplot(data=data, y='Group',x='Recall', ax=ax0, color='w', order=conditions)#, hue='Condition', palette=level_palette)
gs.tight_layout(fig)

level_to_location = {cond:i for i, cond in enumerate(conditions)} # map categories to y axis locations.

ax1=fig.add_subplot(gs[1])
metroplot(pairwise_comparisons,level_to_location=level_to_location,metroplot_element_order=conditions,
                                ax=ax1, level_axis='y',dominating_effect_direction=1,
                                level_pallete='k', level_axis_lim=ax0.get_ylim())
# # note that level_axis_lim=ax0.get_ylim() aligns the metrplot with the main plot

plt.show()
