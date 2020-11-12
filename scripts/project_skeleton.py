#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blast_hitter import BlastHitter
from clusterizer import Clusterizer
from ete3 import Tree, TreeStyle, NodeStyle


proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa"]

# pas relancer ce code pcq ça va tout recalculer

for bh in BlastHitter.from_list(proteomes) : 
    bh.blast_them()
    bh.rbh_them()

#####################   
    
rbh = ["../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Piscirickettsia_salmonis_strain=Psal-158.blastp",
       "../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_pneumoniae_R6_strain=R6.blastp",
       "../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_pyogenes_strain=NCTC8232.blastp",
       "../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp",
       "../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Piscirickettsia_salmonis_strain=Psal-158.blastp",
       "../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Streptococcus_pyogenes_strain=NCTC8232.blastp",
       "../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp",
       "../data/results_blast/RBH_Streptococcus_pyogenes_strain=NCTC8232_Piscirickettsia_salmonis_strain=Psal-158.blastp",
       "../data/results_blast/RBH_Streptococcus_pyogenes_strain=NCTC8232_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp",
       "../data/results_blast/RBH_Streptococcus_thermophilus_LMD-9_strain=LMD-9_Piscirickettsia_salmonis_strain=Psal-158.blastp",         
       ]


clss = Clusterizer.clustering(rbh)
#Clusterizer.clusters_to_txt(clss, '../data/clusters/all_clusters.txt')

spss = Clusterizer.species_cluster(clss, proteomes)
max_one_clusters, max_one_species = Clusterizer.max_one_species_per_cluster(spss, clss)
#Clusterizer.clusters_to_txt(max_one, '../data/clusters/max_one_clusters.txt')

all_afa = Clusterizer.muscle(max_one_clusters, proteomes)   

super_align = Clusterizer.super_alignement(max_one_clusters, max_one_species, all_afa, '../data/phylogeny/super_align.afa')


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
