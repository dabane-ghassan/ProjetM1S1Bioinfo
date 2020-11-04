#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 13:13:27 2020

@author: ghassan
"""

import os 
from BlastHitter import BlastHitter

if __name__ == "__main__" : 
    os.chdir("/home/ghassan/M1/ProjetM1S1Bioinfo/scripts")
    proteome1 = "../data/genomes/Yersinia_pestis_strain=FDAARGOS_protein.faa"
    proteome2 = "../data/genomes/Aliivibrio_salmonicida_LFI1238_strain=LFI_protein.faa" 

    h = BlastHitter(proteome1, proteome2)
    h.blast_it()
    h.extract_it()
    h.reblast_it()
    h.cluster_it()
    print('Done, Bravo !')

