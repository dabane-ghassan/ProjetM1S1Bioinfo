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
max_one = Clusterizer.max_one_species_per_cluster(spss, clss)
#Clusterizer.clusters_to_txt(max_one, '../data/clusters/max_one_clusters.txt')

all_afa = Clusterizer.mafft(max_one, proteomes)

oneMSA = Clusterizer.super_alignement(all_afa)


"""
test_afa = all_afa
out = []
first = test_afa.pop(0)

profile_align = subprocess.run(['muscle', '-profile', '-in1', first,
                                '-in2', test_afa.pop(0)], capture_output=True)
output = '../data/phylogeny/clusters_1_2.afa'
with open(output, 'wb') as afa :    
    afa.write(profile_align.stdout) 
out.append(output)

for i in range(len(test_afa)) : 
    second_align = subprocess.run(['muscle', '-profile', '-in1', out[-1],
                                    '-in2', test_afa.pop(0)], capture_output=True)
    output = '../data/phylogeny/clusters.afa'
    with open(output, 'wb') as afa :    
        afa.write(second_align.stdout) 
    out.append(output)
"""