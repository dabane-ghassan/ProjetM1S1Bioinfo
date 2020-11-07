#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from blast_hitter import BlastHitter

class Clusterizer: 
    
    def __init__(self, blasthitters) : 
        
        self.rbh_files = [bh.getRbh() for bh in blasthitters]
    
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
    def species_cluster(cluster_dict, proteomes) : 
    
        dic = {h[1:15] : prot.split("/")[-1] for prot in proteomes for h in BlastHitter.parse_fasta(prot).keys()}
        
        all_species = []
        for cluster in cluster_dict.values():      
            species = tuple([list(dic.values())[list(
                dic.keys()).index(accession)] for accession in cluster])
            all_species.append(species)
            
        return dict(zip(range(1, len(cluster_dict) + 1), all_species))
    
    @staticmethod
    def max_one_species_per_cluster(cluster_species, cluster_dict) : 
        
   
        filtered_cids =  [cid for cid, name in cluster_species.items() if (len(
            cluster_species[cid]) - len(set(cluster_species[cid]))) == 0] 
    
        return {cid : cluster for cid, cluster in cluster_dict.items() if (
            cid in filtered_cids)}


                
    @staticmethod
    def cluster_from_proteome(cluster, proteomes, out):
   
        all_fasta = dict()
        for proteome in proteomes : 
            all_fasta.update(BlastHitter.parse_fasta(proteome))
         
        fasta_cls = {h:s for h,s in all_fasta.items() if h[1:15] in cluster}
                
        with open(out, 'w') as cluster_fasta : 
            for header, sequence in fasta_cls.items() : 
                cluster_fasta.write('%s\n%s\n'%(header,sequence))


    @staticmethod 
    def muscle_them_all(cluster_dict, proteomes):
        
        for cid, cluster in cluster_dict.items() : 
            fasta, afasta = '%s.fa'% cid, '%s.afa'% cid
            output_dir = '../data/multiple_alignements/cluster%s'
            Clusterizer.cluster_from_proteome(cluster, proteomes,
                                              output_dir % fasta)
            
            multialign = subprocess.run(['muscle', '-in', output_dir % fasta],
                                        capture_output=True)
            with open(output_dir % afasta, 'wb') as afa :    
                afa.write(multialign.stdout)                
 