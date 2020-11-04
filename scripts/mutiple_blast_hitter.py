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

for bh in blast_hitters : 
    bh.blast_them()
    bh.cluster_them()

