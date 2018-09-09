import numpy as np
import matplotlib.pyplot as plt

raw_center = """
4.3	15.8	1.8	18.3	6.8	13.3	7.3	17.8	2.3	12.8
5	15.1	2.3	17.8	7.7	12.4	8.3	17.1	3	11.8
5.7	14.4	2.8	17.3	8.6	11.5	9.3	16.4	3.7	10.8
6.4	13.7	3.3	16.8	9.5	10.6	10.3	15.7	4.4	9.8
7.1	13	3.8	16.3	10.4	9.7	11.3	15	5.1	8.8
7.8	12.3	4.3	15.8	11.3	8.8	12.3	14.3	5.8	7.8
8.5	11.6	4.8	15.3	12.2	7.9	13.3	13.6	6.5	6.8
9.2	10.9	5.3	14.8	13.1	7	14.3	12.9	7.2	5.8
9.9	10.2	5.8	14.3	14	6.1	15.3	12.2	7.9	4.8
"""										
raw_ideal = """
4.3	15.8	1	19.1	8.2	11.9	8.7	16.8	3.3	11.4
5	15.1	1.5	18.6	9.1	11	9.7	16.1	4	10.4
5.7	14.4	2	18.1	10	10.1	10.7	15.4	4.7	9.4
6.4	13.7	2.5	17.6	10.9	9.2	11.7	14.7	5.4	8.4
7.1	13	3	17.1	11.8	8.3	12.7	14	6.1	7.4
7.8	12.3	3.5	16.6	12.7	7.4	13.7	13.3	6.8	6.4
8.5	11.6	4	16.1	13.6	6.5	14.7	12.6	7.5	5.4
9.2	10.9	4.5	15.6	14.5	5.6	15.7	11.9	8.2	4.4
9.9	10.2	5	15.1	15.4	4.7	16.7	11.2	8.9	3.4
"""

keys = ['Traditional', 'Low End', 'High End', 'Performance', 'Size']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

centers = [map(float, item.split('\t')) for item in raw_center.strip().split('\n')]
ideals = [map(float, item.split('\t')) for item in raw_ideal.strip().split('\n')]

rounds = []
for center_row, ideal_row in zip(centers, ideals):
    data = {}
    for i, key in enumerate(keys):
        center = center_row[i*2:i*2+2]
        ideal = ideal_row[i*2:i*2+2]
        data[key] = {'center': center, 'ideal': ideal}
    rounds.append(data)

def double_circle(ax, xy, label, color):
    a, b = 2.5, 4.0
    x, y = xy
    inner = plt.Circle((xy), a, fc=color, ec='black', alpha=0.4)
    outer = plt.Circle((xy), b, fc=color, ec='gray', alpha=0.2)
    edge = plt.Circle((xy), b, fc='none', ec='gray', alpha=0.5, ls=':')
    ax.add_artist(inner)
    ax.add_artist(outer)
    ax.add_artist(edge)
    ax.text(x, y, label, ha='center', va='center', clip_on=False)


for i, data in enumerate(rounds):
    fig, ax = plt.subplots()
    ax.axis([0, 20, 0, 20])
    ax.set(aspect=1.0, xlabel='Performance', ylabel='Size', 
           title='Perceptual map (End of year {})'.format(i))
    ax.grid(color='gray')

    for key, color in zip(keys, colors):
        double_circle(ax, data[key]['center'], key, color)
        x, y = data[key]['ideal']
        ax.plot([x], [y], marker='.', color='black', ms=8)
    fig.savefig('model_year_{}.png'.format(i))
#    plt.show()

#
#double_circle(ax, 2, 18, 'Low End', 'lightblue')
#double_circle(ax, 7, 17.5, 'Performance', 'salmon')
#double_circle(ax, 4, 16, 'Traditional', 'lightgreen')
##double_circle(ax, 4, 16, 'Traditional', 'lightgreen')
#plt.show()

