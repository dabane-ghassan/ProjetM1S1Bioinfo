#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:35:02 2020

@author: ghassan
"""

def parse_fasta(proteome) : 
    """This function parses genome or proteome fasta files.

    Parameters
    ----------
    proteome : TYPE str
        DESCRIPTION. the file path for a given fasta file

    Returns
    -------
    seqdic : TYPE dict
        DESCRIPTION. a dictionary of the proteome with the fasta headers as 
                    keys and the corresponding fasta sequences as values.

    """
    
    list_seqs = open(proteome, 'r').read().split('>')[1:]  # split the file
    seqdic = {}

    for seq in list_seqs:
        seq = seq.strip().split(
            '\n')  # strip each sequence from spaces then split it
        seqdic['>' + seq[0]] = ''.join(seq[1:])
    return seqdic
    