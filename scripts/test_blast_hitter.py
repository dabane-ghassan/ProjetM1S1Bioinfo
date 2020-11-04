#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
from blast_hitter import BlastHitter

if __name__ == "__main__" : 
    os.chdir("/home/ghassan/M1/ProjetM1S1Bioinfo/scripts")
    proteome1 = "../data/genomes/Yersinia_pestis_strain=FDAARGOS_protein.faa"
    proteome2 = "../data/genomes/Aliivibrio_salmonicida_LFI1238_strain=LFI_protein.faa" 

    h = BlastHitter(proteome1, proteome2)
    h.blast_them()
    h.cluster_them()
    print('Done, Bravo !')

 

            
            
