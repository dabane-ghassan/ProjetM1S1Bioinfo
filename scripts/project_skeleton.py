#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blast_hitter import BlastHitter
from clusterizer import Clusterizer


proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa"]

# pas relancer ce code pcq ça va tout recalculer
"""
for bh in BlastHitter.from_list(proteomes) : 
    bh.blast_them()
    bh.rbh_them()
"""


# stats de protéomes
BlastHitter.seqkit_stats(proteomes[0])
BlastHitter.seqkit_stats(proteomes[1])
BlastHitter.seqkit_stats(proteomes[2])
BlastHitter.seqkit_stats(proteomes[3])
BlastHitter.seqkit_stats(proteomes[4])

BlastHitter.parse_fasta(proteomes[0])


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
Clusterizer.clusters_to_txt(clss, '../data/results_blast/clusters.txt')

Clusterizer.parse_fasta(proteomes[4]).keys()
Clusterizer.parse_fasta(proteomes[4]).keys()
Clusterizer.parse_fasta(proteomes[4]).keys()
Clusterizer.parse_fasta(proteomes[4]).keys()

for node in clss[66] :   
    for k in Clusterizer.parse_fasta(proteomes[4]).keys() : 
        if node in k : 
            print(k)



