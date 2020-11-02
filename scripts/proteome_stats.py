#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:01:31 2020

@author: ghassan
"""

proteome = 'Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa'

def num_seqs(proteome) : 
    with open(proteome, 'r') as pr : 
        return [line for line in pr if line.startswith('>')]

 
