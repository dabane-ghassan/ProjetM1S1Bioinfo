#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:35:02 2020

@author: ghassan
"""

def parse_fasta(proteome) : 
    
    list_seqs = open(proteome, 'r').read().split('>')[1:]  # split the file
    seqdic = {}

    for seq in list_seqs:
        seq = seq.strip().split(
            '\n')  # strip each sequence from spaces then split it
        seqdic['>' + seq[0]] = ''.join(seq[1:])
    return seqdic
    