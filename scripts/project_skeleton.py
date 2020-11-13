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
 

"""  
from ete3 import Tree, TreeStyle, NodeStyle  
Clusterizer.tree_generator('../data/phylogeny/super_align.afa')

t = Tree('../data/phylogeny/RAxML_bipartitions.species')
# Basic tree style
ts = TreeStyle()
ts.show_leaf_name = True

# Draws nodes as small red spheres of diameter equal to 10 pixels
nstyle = NodeStyle()
nstyle["shape"] = "sphere"
nstyle["size"] = 10
nstyle["fgcolor"] = "darkred"

# Gray dashed branch lines
nstyle["hz_line_type"] = 1
nstyle["hz_line_color"] = "#cccccc"

# Applies the same static style to all nodes in the tree. Note that,
# if "nstyle" is modified, changes will affect to all nodes
for n in t.traverse():
   n.set_style(nstyle)

t.show(tree_style=ts)
"""

