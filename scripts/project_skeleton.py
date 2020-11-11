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


acc_species = {clus : spec for clus, spec in zip(
    max_one_clusters[1], max_one_species[1])}

acc_aseq = {h[1:15] : aseq for h, aseq in BlastHitter.parse_fasta(
    all_afa[0]).items()}


{'>'+acc_species[h] : aseq for h, aseq in acc_aseq.items()}

#BlastHitter.parse_fasta(all_afa[0]).values() 
