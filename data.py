import numpy as np
import pandas as pd

inner_radius = 2.5
outer_radius = 4.0

years = tuple(range(9))

centers = pd.read_csv('centers.csv', index_col=0)
ideals = pd.read_csv('ideals.csv', index_col=0)
keys = ['Traditional', 'Low End', 'High End', 'Performance', 'Size']
colors = dict(zip(keys, ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))

_across = np.ones(len(years))
products = pd.DataFrame({'Low End Starting X': 2.3 * _across,
                         'Low End Starting Y': 17.8 * _across,
                         'Traditional Starting X': 4.8 * _across,
                         'Traditional Starting Y': 15.3 * _across,
                         'High End Starting X': 7.3 * _across,
                         'High End Starting Y': 12.8 * _across,
                         'Performance Starting X': 8.7 * _across,
                         'Performance Starting Y': 16.3 * _across,
                         'Size Starting X': 3.3 * _across,
                         'Size Starting Y': 11.8 * _across})
products.index.name = 'Year'

center_keys = ['Low End', 'Traditional', 'High End']
_ix = [['%s Starting X' % key, '%s Starting Y' % key] for key in center_keys]
center_products = products[sum(_ix, [])]
size_products = products[['Size Starting X', 'Size Starting Y']]
performance_products = products[['Performance Starting X', 
                                 'Performance Starting Y']]

def edit_product(product):
    import qgrid
    df = product.T
    cols = df.columns
    df['Product'] = df.index
    df.index = np.arange(df.shape[0])
    df = df[['Product'] + list(cols)]
    widget = qgrid.show_grid(df, grid_options=dict(filterable=False), 
                             show_toolbar=True,
                             column_definitions={
                                 'Product': dict(minWidth=100, width=200),
                                 'index': dict(maxWidth=0, minWidth=0, width=0)
                                 },
                             )
    return widget

def get_product(widget):
    df = widget.get_changed_df()
    cols = list(df.columns)
    cols.remove('Product')
    df.index = df['Product']
    return df[cols].T



