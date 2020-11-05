#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from blast_hitter import BlastHitter
from itertools import combinations


proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa"]

prots = list(combinations(proteomes, 2))

prots

BlastHitter.seqkit_stats(proteomes[0])
BlastHitter.seqkit_stats(proteomes[1])
BlastHitter.seqkit_stats(proteomes[2])
BlastHitter.seqkit_stats(proteomes[3])
BlastHitter.seqkit_stats(proteomes[4])


blast_hitters = [BlastHitter(couple[0], couple[1]) for couple in prots]

# pas relancer ce code
"""
for bh in blast_hitters : 
    bh.blast_them()
    bh.cluster_them()
"""
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

def pair_rbh(file) : 
    
    with open(file, 'r') as f : 
        return [(line.split('\t')[0], line.split('\t')[1]) for line in f]
    
def all_pairs_rbh(rbh_files) : 
    
    total = list()
    for rbh_file in rbh_files : 
        total.extend(pair_rbh(rbh_file))
    return total
    
rbhits= all_pairs_rbh(rbh)

clusters = dict()
for rbhit in rbhits :
    if rbhit[0] not in clusters.keys() : 
        clusters[rbhit[0]] = [rbhit[1]]
    elif rbhit[1] not in clusters[rbhit[0]]: 
        clusters[rbhit[0]].append(rbhit[1]) 
    else : 
        pass

len(list(clusters.keys()))
        
for k,v in clusters.items() : 
    if len(v) == 2 : 
        print(k,v)




