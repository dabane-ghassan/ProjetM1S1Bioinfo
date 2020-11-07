#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from blast_hitter import BlastHitter

class Clusterizer: 
    
    def __init__(self, blasthitters) : 
        
        self.rbh_files = [bh.get_rbh_file() for bh in blasthitters]
    
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
            total.extend(Clusterizer.pair_rbh(rbh_file))
        return total
    
    @staticmethod 
    def clustering(rbh_files): 
        """The main clustering algorithm to find reciprocal best hits among
        multiple RBH blast files. it uses the class's all_pairs_rbh static
        method as a starting point. After getting the list of all RBH couples
        in all RBH files, it traverses it taking the first element and 
        appending it as key in a dictionary if it's not already present. 
        Otherwise (i.e if the accession number is present), it appends the
        second element to the value list in order to get all the hits in 
        common.
        
        Parameters
        ----------
        rbh_files : list
            A list of RBH blast file paths.

        Returns
        -------
        dict
            a dictionary of all clusters present among all RBH files,
            keys are auto incremented integers which correspond to cluster IDs,
            values are NCBI accession numbers of the proteins present in a
            given cluster.

        """
                  
        clusters_list = []

        for rbh1, rbh2 in Clusterizer.all_pairs_rbh(rbh_files):
            
            for cluster in clusters_list:
                if rbh1 in cluster or rbh2 in cluster:
                    cluster.add(rbh1)
                    cluster.add(rbh2)
                    break
            else:
                
                clusters_list.append(set([rbh1, rbh2]))
        results = [tuple(cluster) for cluster in clusters_list]
            
        return dict(zip(range(1, len(clusters_list) + 1), results))
        
    @staticmethod
    def clusters_to_txt(cluster_dict, out): 
        
        with open(out , 'w') as cluster_file :       
            for cluster in cluster_dict.values() :                      
                cluster_file.write('\t'.join(map(str,cluster))+'\n')
     
    @staticmethod 
    def cluster_species(cluster_dict, proteomes) : 
    
        dic = {h[1:15] : prot.split("/")[-1] for prot in proteomes for h in BlastHitter.parse_fasta(prot).keys()}
        
        all_species = []
        for cluster in cluster_dict.values():      
            species = tuple([list(dic.values())[list(dic.keys()).index(accession)] for accession in cluster])
            all_species.append(species)
            
        return dict(zip(range(1, len(cluster_dict) + 1), all_species))

                
    @staticmethod
    def rbh_from_genome(blastp_file, proteome, out):
   
        with open(blastp_file, 'r') as bfile :
            bh_ids = [line.split('\t')[1] for line in bfile]
        
        best_hits = {h:seq for h, seq in BlastHitter.parse_fasta(
            proteome).items() if h[1:15] in bh_ids}
        
        with open(out, 'w') as bh_proteome : 
            for header, sequence in best_hits.items() : 
                bh_proteome.write('%s\n%s\n'%(header,sequence))
 