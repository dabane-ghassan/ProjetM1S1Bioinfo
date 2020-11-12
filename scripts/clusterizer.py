#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from blast_hitter import BlastHitter


class Clusterizer:
    """This is a class for clusterizing groups of orthologue proteines (OG),
    extracting their respective sequences from the corresponding given 
    proteome, aligning each cluster individually and then constructing the 
    super-alignement.
    
    Attributes  
    ------------
    rbh_files : list
        A list of reciprocal best hits file paths generated after each blast
        hitter object.
    proteomes : list
        A list of all proteome paths present in a given analysis
        
    """
    def __init__(self, blasthitters, proteomes):
        """The class constructor, given a list of BlastHitter objects, the 
        corresponding RBH file will be extracted (by a getter method)
        and will be collected in the attribute rbh_files for further analysis.
        

        Parameters
        ----------
        blasthitters : list
            A list of BlastHitters objects.
        proteomes : list
            A list of proteomes paths.

        Returns
        -------
        Class object.

        """

        self.rbh_files = [bh.getRbh() for bh in blasthitters]
        self.proteomes = proteomes

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

        with open(file, 'r') as f:
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
        for rbh_file in files:
            total.extend(Clusterizer.pair_rbh(rbh_file))
        return total

    @staticmethod
    def clustering(rbh_files):
        """The main clustering algorithm to find reciprocal best hits among
        multiple RBH blast files. it uses the class's all_pairs_rbh static
        method as a starting point. After getting the list of all RBH couples
        in all RBH files (a list of tuples), it traverses it and throws the 
        couple of RBHs in a set inside a list if one of them is present in a
        given set, otherwise if the loop exited without a break, create 
        another cluster from the two RBHs, Time complexity O(n²).
        
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

        with open(out, 'w') as cluster_file:
            for cluster in cluster_dict.values():
                cluster_file.write('\t'.join(map(str, cluster)) + '\n')

    @staticmethod
    def species_cluster(cluster_dict, proteomes):

        dic = {
            h[1:15]:
            prot.rsplit("/")[-1][0:prot.rsplit('/')[-1].find('_protein.faa')]
            for prot in proteomes
            for h in BlastHitter.parse_fasta(prot).keys()
        }

        all_species = []
        for cluster in cluster_dict.values():
            species = tuple([
                list(dic.values())[list(dic.keys()).index(accession)]
                for accession in cluster
            ])
            all_species.append(species)

        return dict(zip(range(1, len(cluster_dict) + 1), all_species))

    @staticmethod
    def max_one_species_per_cluster(cluster_species, cluster_dict):

        filtered = {
            cid: cluster
            for cid, cluster in cluster_species.items()
            if (len(cluster) - len(set(cluster))) == 0
        }

        return {
            cid: cluster
            for cid, cluster in cluster_dict.items()
            if (cid in filtered.keys())
        }, filtered

    @staticmethod
    def cluster_from_proteome(cluster, proteomes, out):

        all_fasta = dict()
        for proteome in proteomes:
            all_fasta.update(BlastHitter.parse_fasta(proteome))

        fasta_cls = {h: s for h, s in all_fasta.items() if h[1:15] in cluster}

        with open(out, 'w') as cluster_fasta:
            for header, sequence in fasta_cls.items():
                cluster_fasta.write('%s\n%s\n' % (header, sequence))

    @staticmethod
    def muscle(cluster_dict, proteomes):

        afasta_files = []
        fa_dir = '../data/clusters/cluster%s'
        afa_dir = '../data/multiple_alignements/cluster%s'

        for cid, cluster in cluster_dict.items():
            fasta, afasta = '%s.fa' % cid, '%s.afa' % cid

            afasta_file = afa_dir % afasta
            Clusterizer.cluster_from_proteome(cluster, proteomes,
                                              fa_dir % fasta)

            multialign = subprocess.run(['muscle', '-in', fa_dir % fasta],
                                        capture_output=True)
            with open(afasta_file, 'wb') as afa:
                afa.write(multialign.stdout)

            afasta_files.append(afasta_file)

        return afasta_files

    @staticmethod
    def super_alignement(cluster_dict, cluster_species, maligns, out):

        acc_species = {
            clus: spec
            for clus, spec in zip(cluster_dict[1], cluster_species[1])
        }

        acc_aseq = {
            h[1:15]: aseq
            for h, aseq in BlastHitter.parse_fasta(maligns[0]).items()
        }

        concat = {acc_species[acc]: aseq for acc, aseq in acc_aseq.items()}

        for afa, cid in zip(maligns[1:], list(cluster_dict.keys())[1:]):

            acc_species_2 = {
                clus: spec
                for clus, spec in zip(cluster_dict[cid], cluster_species[cid])
            }

            acc_aseq_2 = {
                h[1:15]: aseq
                for h, aseq in BlastHitter.parse_fasta(afa).items()
            }

            for acc, aseq in acc_aseq_2.items():
                if acc_species_2[acc] in concat.keys():
                    concat[acc_species_2[acc]] += aseq

            other_species = [
                spec for spec in concat.keys()
                if spec not in acc_species_2.values()
            ]
            for spec in other_species:
                concat[spec] += '-' * len(list(acc_aseq_2.values())[0])

        with open(out, 'w') as super_align:
            for header, sequence in concat.items():
                super_align.write('>%s\n%s\n' % (header, sequence))

        return concat

    @staticmethod
    def tree_generator(super_alignement):
        os.chdir('../data/phylogeny')
        subprocess.run([
            'raxmlHPC', '-s',
            super_alignement.rsplit('/')[-1], '-n', 'tree.newick', '-m',
            'PROTCATBLOSUM62', '-p', '52341'
        ])