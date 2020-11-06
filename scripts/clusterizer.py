#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:17:25 2020

@author: ghassan
"""

from blast_hitter import BlastHitter
from itertools import combinations

class Clusterizer(BlastHitter) : 
    
    def __init__(self, proteomes) : 
        self.proteomes = list(combinations(proteomes, 2))
    
    @staticmethod
    def pair_rbh(file): 
        """This function parses the reciprocal best hits file and returns a 
        list of all rbh couples. it extracts the first and the second columns.
        
        Parameters
        ----------
        file : str
            The RBH file_path.

        Returns
        -------
        list
            a list of tuples of all RBH couples.

        """
    
        with open(file, 'r') as f : 
            return [(line.split('\t')[0], line.split('\t')[1]) for line in f]
    
    @staticmethod
    def all_pairs_rbh(files): 
        """This function take multiple RBH files and returns a long list of
        all RBH couples that are present in those FILES, it calls the previous
        class static method.
        
        Parameters
        ----------
        files : list
            a list of all RBH file paths to be analyzed.

        Returns
        -------
        total : list
            a list of tuples of all RBH couples in all specified files.

        """
        
        total = list()
        for rbh_file in files : 
            total.extend(Clusterer.pair_rbh(rbh_file))
        return total
    
    @staticmethod 
    def clustering(rbh_files): 
           
        cluster_algo = dict()   
        rbhits= Clusterer.all_pairs_rbh(rbh_files)
        for rbhit in rbhits :
            if rbhit[0] not in cluster_algo.keys() : 
                cluster_algo[rbhit[0]] = [rbhit[1]]
            elif rbhit[1] not in cluster_algo[rbhit[0]]: 
                cluster_algo[rbhit[0]].append(rbhit[1]) 
            else : 
                pass
            
        all_clusters = [(k, *v) for k,v in cluster_algo.items()]
        all_cluster_ids = [cid for cid in range(1, len(all_clusters) + 1)]
        
        return {cid : cluster for cid, cluster in zip(
            all_cluster_ids, all_clusters)}
            
        
    @staticmethod
    def clusters_to_txt(cluster_dict, out): 
        
        with open(out , 'w') as cluster_file :       
            for cluster in cluster_dict.values() :                      
                cluster_file.write('\t'.join(map(str,cluster))+'\n')
                
                
    @staticmethod
    def rbh_from_genome(blastp_file, proteome, out):
   
        with open(blastp_file, 'r') as bfile :
            bh_ids = [line.split('\t')[1] for line in bfile]
        
        best_hits = {h:seq for h, seq in BlastHitter.parse_fasta(
            proteome).items() if h[1:15] in bh_ids}
        
        with open(out, 'w') as bh_proteome : 
            for header, sequence in best_hits.items() : 
                bh_proteome.write('%s\n%s\n'%(header,sequence))
 