import os
import networkx as nx
import glob
import pandas as pd
from collections import defaultdict


segment = '256b'
dct = defaultdict(list)

global sum_density
sum_density = 0


indir = '//Users/Torben/Desktop/Python/consensus/allgraphmlfiles/bitcoin-gml-network-heur_2s.%s/' % (
    segment)
filecounter = len(glob.glob(indir + "segment_*.graphml"))

for root, dirs, filenames in os.walk(indir):
    for counter, f in enumerate(filenames, start=1):
        g = nx.read_graphml(os.path.join(root, f))
        dens = nx.density(g)
        sum_density += dens
        print(dens, "; density Graph ", counter, '/', filecounter)
        dct['density'].append(dens)
        # dct['counter'].append(counter)


mytable = pd.DataFrame(dct)
print(mytable)

mytable.to_csv('densityT.csv', index=False, sep=',', encoding='utf-8')


avg_density = sum_density / filecounter
print("Average Density: ", avg_density)
