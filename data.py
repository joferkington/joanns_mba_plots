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
products = pd.DataFrame({'Bead X': 2.3 * _across,
                         'Bead Y': 17.8 * _across,
                         'Baker X': 4.8 * _across,
                         'Baker Y': 15.3 * _across,
                         'Bid X': 7.3 * _across,
                         'Bid Y': 12.8 * _across,
                         'Bold X': 8.7 * _across,
                         'Bold Y': 16.3 * _across,
                         'Buddy X': 3.3 * _across,
                         'Buddy Y': 11.8 * _across})
products.index.name = 'Year'

center_keys = ['Bead', 'Baker', 'Bid']
_ix = [['%s X' % key, '%s Y' % key] for key in center_keys]
center_products = products[sum(_ix, [])]
size_products = products[['Bold X', 'Bold Y']]
performance_products = products[['Buddy X', 
                                 'Buddy Y']]

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



