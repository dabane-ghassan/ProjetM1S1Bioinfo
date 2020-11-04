#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
os.chdir("/home/ghassan/M1/ProjetM1S1Bioinfo/scripts") # mégane change le chemin pour que ça colle avec ton ordi
from first_program import parse_fasta, seqkit_stats, blast, best_hits, extract_best_hits, bidir_best_hits

# Localisation des 2 protéomes a étudier
proteome1 = "../data/genomes/Yersinia_pestis_strain=FDAARGOS_protein.faa"
proteome2 = "../data/genomes/Aliivibrio_salmonicida_LFI1238_strain=LFI_protein.faa" 

# stats des protéomes
seqkit_stats(proteome1)
seqkit_stats(proteome2)

prot1 = parse_fasta(proteome1)
prot2 = parse_fasta(proteome2)

# Lancement du blast1 : proteome 1 contre proteome 2
cmdblast1, output1 = blast(proteome1,proteome2)

cmdblast1
output1

os.system(cmdblast1)

# Sélection des best hits du blast1
bhits1 = best_hits(output1)

# Récupération des id,et de leurs séquence, des best hits du blast1
proteome2_bh = extract_best_hits(proteome2,bhits1)
# Lancement du blast2 : best hits du proteome 2 obtenues lors du blast1 contre le proteome 1
cmdblast2, output2 = blast(proteome2_bh, proteome1)

cmdblast2
output2

os.system(cmdblast2)

# Sélection des best hits du blast2
bhits2 = best_hits(output2)

# Récupération des best hits bidirectionnels
bidir_best_hits(bhits1, bhits2)
        

