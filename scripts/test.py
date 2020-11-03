#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:46:59 2020

@author: ghassan
"""
import os 
from seqkit_stats import stats
from parse_proteome import parse_fasta

# os.chdir("") répertoire des scripts

proteome1 = "../data/genomes/Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa"
proteome2 = "../data/genomes/Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa" 

stats(proteome1)
stats(proteome2)

prot1 = parse_fasta(proteome1)
prot2 = parse_fasta(proteome2)
