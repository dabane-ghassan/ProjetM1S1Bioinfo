#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blast_hitter import BlastHitter
from clusterizer import Clusterizer


proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa"]

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


import networkx as nx
all_clus = [line.strip().split('\t') for line in open('../data/clusters/all_clusters.txt')]

"""
https://www.youtube.com/watch?v=mV44dBi9qcQ

https://www.youtube.com/watch?v=zY0ZGwvFHJk

https://www.youtube.com/watch?v=BFGLxpJDns0

https://www.youtube.com/watch?v=Y2NHuxQ-VUI

https://www.youtube.com/watch?v=zSZpCrwgVOM&pbjreload=101

color = list()
for k in bip.nodes() :
    if (0 <= k < 50) :
        color.append('blue')
    else :
        color.append('red')
        
top = set(list(bip.nodes())[0:50])
pos = nx.bipartite_layout(bip, top)
nx.draw(bip, pos, node_color = color, with_labels=True, node_size = 16, font_size = 4, alpha = 0.3, width = 0.2)
plt.savefig("bip.png", dpi=1000)


"""