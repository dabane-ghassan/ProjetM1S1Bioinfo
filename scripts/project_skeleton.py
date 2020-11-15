#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blast_hitter import BlastHitter
from clusterizer import Clusterizer


proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa",
"../data/genomes/Rickettsia_bellii_OSU_85-389_strain=OSU_85-389_protein.faa"
]

bhitters = BlastHitter.from_list(proteomes) 

for bh in bhitters  : 
    bh.blast_them()
    bh.rbh_them()

clust = Clusterizer(bhitters, proteomes)

clust.cluster_them()
clust.one_align_to_rule_them_all()
clust.draw_tree()

### Histogram
histo = "Streptococcus_pyogenes_strain=NCTC8232_vs_Rickettsia_rickettsii_str._Arizona_strain=Arizona.blastp"
BlastHitter.evalue_dist(histo)


### Seqkit stat
BlastHitter.seqkit_stat(proteomes[-1])



import networkx as nx
import matplotlib.pyplot as plt
all_clus = [tuple(line.strip().split('\t')) for line in open('../data/clusters/all_clusters.txt')]
clus = Clusterizer.all_pairs_rbh()
g = nx.Graph()
g.add_nodes_from(all_clus)
g.nodes()
pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True, node_size = 2, font_size = 1, alpha = 0.3, width = 0.2)
plt.savefig("../data/figures/g.png", dpi=1000)

"""
https://www.youtube.com/watch?v=mV44dBi9qcQ

https://www.youtube.com/watch?v=zY0ZGwvFHJk

https://www.youtube.com/watch?v=BFGLxpJDns0

https://www.youtube.com/watch?v=Y2NHuxQ-VUI

https://www.youtube.com/watch?v=zSZpCrwgVOM&pbjreload=101

color = list()
for k in g.nodes() :
    if (0 <= k < 50) :
        color.append('blue')
    else :
        color.append('red')
        
top = set(list(g.nodes())[0:50])
pos = nx.bipartite_layout(g, top)

pos = nx.bipartite_layout(g, top)
plt.savefig("bip.png", dpi=1000)

"""