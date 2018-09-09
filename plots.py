import numpy as np
import matplotlib.pyplot as plt

import data

def style_setup():
    # There are better ways to do this, but I'm being lazy.
    plt.rcParams['font.size'] = 14.0
    plt.rcParams['legend.fontsize'] = 'medium'
    plt.rcParams['axes.labelsize'] = 'large'


def cluster_plot(cluster):
    style_setup()
    linear_position = position_factory(cluster)
    height = 0.2

    fig, ax = plt.subplots(figsize=(12, 10))
    for year in data.years:
        offset = -(0.5 + (len(cluster) // 2)) * height
        for key in cluster:
            size, performance = data.centers.ix[year][[key + ' X', key + ' Y']]
            x0 = linear_position(size, performance)
            ax.bar(x0 - data.outer_radius, height, 2 * data.outer_radius, year + offset,
                   align='edge',
                   color=data.colors[key], alpha=0.5)
            ax.bar(x0 - data.inner_radius, height, 2 * data.inner_radius, year + offset,
                   align='edge',
                   color=data.colors[key], label=key if year == 0 else None)        
            
            x1 = linear_position(*data.ideals.ix[year][[key + ' X', key + ' Y']])
            ax.plot(x1, year + offset + 0.5 * height, marker='.', color='k')
            
            offset += height

    ax.set(yticks=data.years, xticks=[], xlabel='Position', ylabel='Year')
    ax.legend(loc='upper right')

    return fig, ax, linear_position

def plot_products(ax, products, reproject):
    names = sorted(set([x.rstrip('XY ') for x in products.columns]))
    for name in names:
        cols = [name + ' X', name + ' Y']
        data = products[cols].dropna()
        x, y = [], []
        for year, xy in data.iterrows():
            x0 = reproject(*xy)
            x.extend([x0, x0, x0])
            y.extend([year - 0.25, year, year + 0.25])
        ax.annotate(name, xy=(x[0], -0.25), xytext=(0, 5), xycoords='data', 
                    textcoords='offset points', ha='center', va='bottom')
        ax.plot(x, y, color='gray', lw=2)

    ax.set_ylim([-.7, 8.5])
    ax.invert_yaxis()

def position_factory(keys):
    """
    Define basis vectors based on a market cluster and return a function that
    projects size/performance data into a 1D space along the market cluster's
    trajectory over time.
    """
    # Define new basis vectors for center cluster
    cluster = []
    for key in keys:
        cluster.append(data.centers[[key + ' X', key + ' Y']].values)
    cluster = np.vstack(cluster)
    vals, vecs = np.linalg.eigh(np.cov(cluster.T))
    _idx = np.argmax(vals)
    direc = -1 if vecs[0,1] < 0 else 1

    def linear_position(x, y):
        return direc * vecs.dot([[x], [y]])[_idx][0]

    return linear_position

