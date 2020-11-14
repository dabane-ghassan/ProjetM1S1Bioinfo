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



