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


# autres fonctionnalités à ajouter
###############################################################################
### Histogram
histo = "Streptococcus_pyogenes_strain=NCTC8232_vs_Rickettsia_rickettsii_str._Arizona_strain=Arizona.blastp"
BlastHitter.evalue_dist(histo)


### Seqkit stat
BlastHitter.seqkit_stat(proteomes[-1])
clust.rbh_files



"""
rbh = ['../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_pneumoniae_R6_strain=R6.blastp',
 '../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_pyogenes_strain=NCTC8232.blastp',
 '../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp',
 '../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Piscirickettsia_salmonis_strain=Psal-158.blastp',
 '../data/results_blast/RBH_Rickettsia_rickettsii_str._Arizona_strain=Arizona_Rickettsia_bellii_OSU_85-389_strain=OSU_85-389.blastp',
 '../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Streptococcus_pyogenes_strain=NCTC8232.blastp',
 '../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp',
 '../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Piscirickettsia_salmonis_strain=Psal-158.blastp',
 '../data/results_blast/RBH_Streptococcus_pneumoniae_R6_strain=R6_Rickettsia_bellii_OSU_85-389_strain=OSU_85-389.blastp',
 '../data/results_blast/RBH_Streptococcus_pyogenes_strain=NCTC8232_Streptococcus_thermophilus_LMD-9_strain=LMD-9.blastp',
 '../data/results_blast/RBH_Streptococcus_pyogenes_strain=NCTC8232_Piscirickettsia_salmonis_strain=Psal-158.blastp',
 '../data/results_blast/RBH_Streptococcus_pyogenes_strain=NCTC8232_Rickettsia_bellii_OSU_85-389_strain=OSU_85-389.blastp',
 '../data/results_blast/RBH_Streptococcus_thermophilus_LMD-9_strain=LMD-9_Piscirickettsia_salmonis_strain=Psal-158.blastp',
 '../data/results_blast/RBH_Streptococcus_thermophilus_LMD-9_strain=LMD-9_Rickettsia_bellii_OSU_85-389_strain=OSU_85-389.blastp',
 '../data/results_blast/RBH_Piscirickettsia_salmonis_strain=Psal-158_Rickettsia_bellii_OSU_85-389_strain=OSU_85-389.blastp']


https://www.youtube.com/watch?v=mV44dBi9qcQ

https://www.youtube.com/watch?v=zY0ZGwvFHJk

https://www.youtube.com/watch?v=BFGLxpJDns0

https://www.youtube.com/watch?v=Y2NHuxQ-VUI

https://www.youtube.com/watch?v=zSZpCrwgVOM&pbjreload=101

"""