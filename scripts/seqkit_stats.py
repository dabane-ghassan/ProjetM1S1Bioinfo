#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:01:31 2020

@author: ghassan
"""

from parse_proteome import parse_fasta

def stats(proteome):
    """This function sends back some statistics based on the proteome fasta 
    file, its serves a similar purpose to seqkit stats.
    

    Parameters
    ----------
    proteome : TYPE str
        DESCRIPTION. proteome file path

    Returns
    -------
    None.

    """
    seqdic = parse_fasta(proteome) # parsing proteome to get a dictionary
    length_seq = [len(seq) for seq in seqdic.values()
                  ]  # to facilitate calculating min, max, sum and average

    print(
        " name : %s \n num_seq : %s \n sum_len : %s \n min_len : %s \n avg_len : %s \n max_len : %s"
        % (proteome.rsplit('/')[-1], len(seqdic.keys()), sum(length_seq),
           min(length_seq), sum(length_seq) / len(seqdic.keys()),
           max(length_seq)))

