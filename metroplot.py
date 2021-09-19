import warnings

import matplotlib.pyplot as plt

def metroplot(df, level_to_location, metroplot_element_order,
                level_axis='y',dominating_effect_direction=1, ax=None,
                level_pallete=None, level_axis_lim=None,
                element_axis_lim=None, open_dot_fill_color='w',
                marker='o', linewidth=0.5, markeredgewidth=0.5, markersize=8):
    """ Plot a 'metroplot' pairwise comparisons significance plot.

    Each row in df should describe the outcome of one pair-wise comparison.

    args:
    df (pd.DataFrame) with the columns: level1 (str), level2 (str), effect_direction (1|-1), is_sig (bool).
    level_to_location (dict) a dictionary mapping level names (as in level1 and level2 in df) to locations on level_axis.
        Generally, this should correspond with the tick locations of the categories in the main plot.
    metroplot_element_order (list) list of strings - the order in which the metroplot elements should be plotted.
    level_axis (str) 'x'|'y' which axis should be used to plot levels. For example, use 'x' for horizontal bar plots.
    dominating_effect_direction (int) -1 or 1. Changing this flips the roles of open and closed markers.
    ax (matplotlib.axes._subplots.AxesSubplot) axes handle for plotting the metroplot.
    level_pallete (dict) a dictionary mapping levels to colors. Alternatively, you pass a single color.
    level_axis_lim (tuple) the axis limits of level_axis. Typically this should match the limits of the main plot.
    dot_fill_color (color) the fill color of open ("dominated") levels
    marker, linewidth, markeredgewidth and markersize are fed to plt.plot and control the elements' appearance
    """

    if ax is None:
        ax =plt.gca()

    # eliminate comparisons between conditions that don't appear in level_to_location
    df=df[df.level1.isin(level_to_location) | df.level2.isin(level_to_location)]

    # eliminate non-significant comparisons
    df=df[df.is_sig]

    cur_line_x=0
    for dominating_level in metroplot_element_order:

        if dominating_level is None:
            continue

        # find dominated levels
        row_filter = (df.level1 == dominating_level) & (df.level2.isin(level_to_location)) & (df['effect_direction']==dominating_effect_direction)
        dominated_levels_list = list(df[row_filter].level2)
        row_filter = (df.level2 == dominating_level) & (df.level1.isin(level_to_location)) & (df['effect_direction']==-dominating_effect_direction)
        dominated_levels_list.extend(list(df[row_filter].level1))

        if len(dominated_levels_list)==0:
            continue

        # the following notation assumes the level_axis is y.
        x=[]
        y=[]
        c_fill=[]
        c_edge=[]

        if isinstance(level_pallete,dict):
            element_color=level_pallete[dominating_level]
        elif level_pallete is not None:
            element_color = level_pallete
        else:
            element_color='k'

        # add points to represent the dominated level
        for dominated_level in dominated_levels_list:
            y.append(level_to_location[dominated_level])
            x.append(cur_line_x)
            c_fill.append(open_dot_fill_color)
            c_edge.append(element_color)

        # add a point to represent the dominating level
        y.append(level_to_location[dominating_level])
        x.append(cur_line_x)
        c_fill.append(element_color)
        c_edge.append(element_color)

        cur_line_x+=1

        if level_axis.lower() == 'y':
            pass
        elif level_axis.lower() == 'x':
            x, y = y, x # flip axes.
        else:
            raise ValueError('level_axis must be x or y.')

        ax.plot(x,y,'-',color=element_color,clip_on=False,linewidth=linewidth) # plot line
        for i in range(len(x)): # plot dots
            ax.plot(x[i],y[i],marker,markerfacecolor=c_fill[i],markeredgecolor=c_edge[i],clip_on=False,markeredgewidth=markeredgewidth, markersize=markersize) # plot markers

    if level_axis_lim is not None:
        if level_axis.lower() == 'y':
            ax.set_ylim(level_axis_lim)
        else:
            ax.set_xlim(level_axis_lim)

    if element_axis_lim is not None:
        if level_axis.lower() == 'y':
            cur_ax=ax.get_xlim()
            set_func = ax.set_xlim
        else:
            cur_ax=ax.get_ylim()
            set_func = ax.set_ylim
        if cur_ax[0] < element_axis_lim[0]:
            warnings.warn(f"element_axis_lim[0] too small ({cur_ax[0]} < {element_axis_lim[0]}) adjusting to avoid clipped elements.")
            element_axis_lim[0]=cur_ax[0]
        if cur_ax[1] > element_axis_lim[1]:
            warnings.warn(f"element_axis_lim[1] too small ({cur_ax[1]} > {element_axis_lim[1]}) adjusting to avoid clipped elements.")
            element_axis_lim[1]=cur_ax[1]

        set_func(element_axis_lim)

    ax.axis('off')