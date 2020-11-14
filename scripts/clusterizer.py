#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from ete3 import Tree, TreeStyle, NodeStyle
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
        A list of all proteome paths present in a given analysis.
    working_cluster : dictionary
        A collection of clusters (protein accession numbers) present among 
        the given RBH files, filtering was applied to only get a maximum of
        one protein per species inside a cluster (no paralogues). 
        Dictionary values correspond to cluster IDs which are auto-incremented
        int values.         
    corr_species_cluster : dictionary 
        The corresponding species cluster for the given working cluster 
        dictionary, it's the same data structure as the working cluster except
        the fact that protein accession numbers are replaced with Species 
        of origin name.
    super_alignement : str
        the file path of the calculated super-alignement in aligned fasta 
        format (.afa).
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
        """Writes a cluster dictionary to a text file, each line corresponds
        to a cluster of orthologue proteins.
        

        Parameters
        ----------
        cluster_dict : dict
            a dictionary of cluster ids and cluster accessions.
        out : str
            the output text file path.

        Returns
        -------
        None.

        """

        with open(out, 'w') as cluster_file:
            for cluster in cluster_dict.values():
                cluster_file.write('\t'.join(map(str, cluster)) + '\n')

    @staticmethod
    def species_cluster(cluster_dict, proteomes):
        """This function generates a species cluster from an accession
        cluster, keys are cluster ids (auto incremented int values) and values
        are clusters of species names for every protein in the cluster.
        First it parses all proteome files and every header in each proteome,
        afterwords, it scans the already generated cluster dictionary to
        generate a replica of it swapping the accession number by the species
        of origin.
        

        Parameters
        ----------
        cluster_dict : dict
            The cluster dictionary (with accessions).
        proteomes : list
            A list of proteomes file paths.

        Returns
        -------
        dict
            The corresponding species dictionary to a given cluster accession
            dictionary.

        """

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
        """Filters cluster dictionaries to only one protein per species.
        It scans the cluster species dictionary and sends back the subset of it
        for which we only have one protein per species, then in filters the
        cluster accession dictionary with the ids of the filtered one.
        

        Parameters
        ----------
        cluster_species : dict

        cluster_dict : dict
        
        Returns
        -------
        dict
            The filtered cluster accession dicionary.
        filtered : dict
            the filtered cluster species dictionary.

        """

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
        """Extracts a fasta file for a given cluster, it firsts parses all 
        proteome files to generate one big dictionary, it then filters it
        to take only the headers and the sequence that correspond to accession
        numbers found in a cluster.
        

        Parameters
        ----------
        cluster : tuple
            A tuple of protein accession numbers found in a cluster.
            
        proteomes : list
            A list of all proteomes file path
            
        out : str
            The output file path.

        """

        all_fasta = dict()
        for proteome in proteomes:
            all_fasta.update(BlastHitter.parse_fasta(proteome))

        fasta_cls = {h: s for h, s in all_fasta.items() if h[1:15] in cluster}

        with open(out, 'w') as cluster_fasta:
            for header, sequence in fasta_cls.items():
                cluster_fasta.write('%s\n%s\n' % (header, sequence))

    @staticmethod
    def muscle(cluster_dict, proteomes):
        """Creates fasta files for each cluster, and then aligns each of them
        using MUSCLE.
        
        Parameters
        ----------
        cluster_dict : dict

        proteomes : list

        Returns
        -------
        afasta_files : list
            A list of all the generated aligned fasta file paths (.afa).

        """

        afasta_files = []
        fa_dir = '../data/clusters/cluster%s'  #fasta output
        afa_dir = '../data/multiple_alignements/cluster%s'  # afasta output

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
        """This function concatenates all the multiple alignement files into
        one super-alignement fasta file, each header is the name of the species
        studied and the sequence corresponds to the concatenation of all the
        clusters. It first creates a seed dictionary of the first cluster i.e;
        with keys as species' name and values as the aligned sequences. 
        Afterwards, and for each cluster, it appends the aligned sequence into
        the species name if the cluster has a protein from a given species, 
        otherwise it fills it with gaps that has the same length as the multi-
        ple alignement inside a cluster.        

        Parameters
        ----------
        cluster_dict : dict

        cluster_species : dict

        maligns : list
            A list of all multiple alignement files paths.
        out : str
            The super-alignement output file path.

        """

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
                super_align.write(
                    '>%s\n%s\n' %
                    (header[:header.find('strain') - 1], sequence))

    @staticmethod
    def tree_generator(super_alignement, bootstrap):
        """Generates a newick tree from a given super-alignement. it uses
        RAxML's maximum likelihood algorithm.
        

        Parameters
        ----------
        super_alignement : str
            The super-alignement file path.
        bootstrap : int
            Number of repetitions for bootstrap.

        Returns
        -------
        tree_name : str
            The newick tree to be visualized (the file path).

        """
        output_dir = os.path.dirname(os.getcwd()) + '/data/phylogeny/'
        pid = super_alignement.rsplit('/')[-1]
        tree_name = 'RAxML_bipartitions.species'

        subprocess.run([
            'raxmlHPC', '-w', output_dir, '-f', 'a', '-x', '12353', '-N',
            str(bootstrap), '-s', output_dir + pid, '-n', 'species', '-m',
            'PROTCATBLOSUM62', '-p', '52341'
        ])

        return tree_name

    def cluster_them(self):
        """This method is used for generalizing the clustering workflow,
        First, clusters from rbh files and write them out to a text. Second,
        generate the species cluste, third, filter the dictionaries to only
        one protein per orgranism inside a cluster and lastly, write out the
        filtered clusters to a file and set the two dictionaries as class 
        properties so they can be used elsewise.

        """

        all_clusters = '../data/clusters/all_clusters.txt'
        all_clusters_max_one = '../data/clusters/one_species_per_cluster.txt'

        clus_dict = Clusterizer.clustering(self.rbh_files)
        Clusterizer.clusters_to_txt(clus_dict, all_clusters)

        species_dict = Clusterizer.species_cluster(clus_dict, self.proteomes)
        max_one_clusters, max_one_species = Clusterizer.max_one_species_per_cluster(
            species_dict, clus_dict)
        Clusterizer.clusters_to_txt(max_one_clusters, all_clusters_max_one)

        self.working_cluster = max_one_clusters
        self.corr_species_cluster = max_one_species

    def one_align_to_rule_them_all(self):
        """Generating the super alignement file for the analyzed species of 
        interest, it firsts generates MSAs for all clusters using MUSCLE,
        and then it concatenates them. all results will be saved to respective
        directories. It alse sent the super alignement file path as a class
        property.

        """

        all_species_names = '_'.join([
            prot.rsplit('/')[-1][0:prot.rsplit('/')[-1].find('_protein.faa')]
            for prot in self.proteomes
        ])

        out = '../data/phylogeny/super_align_%s.afa' % all_species_names

        all_multialigns = Clusterizer.muscle(self.working_cluster,
                                             self.proteomes)

        Clusterizer.super_alignement(self.working_cluster,
                                     self.corr_species_cluster,
                                     all_multialigns, out)
        self.super_alignement = out

    def draw_tree(self, iters=10):
        """This method generates an interactive phylogenetic tree from a
        super alignement file. It calculates a newick tree with RAxML and then
        visualizes it using ETEtoolkit.
        
        Parameters
        ----------

        iters : int, optional
            Number of repetitions for bootstrap. The default is 10.
        
        """

        bootstrap_tree = Clusterizer.tree_generator(self.super_alignement,
                                                    bootstrap=iters)
        t = Tree('../data/phylogeny/%s' % bootstrap_tree)

        ts = TreeStyle()
        ts.show_leaf_name = True

        nstyle = NodeStyle()
        nstyle["shape"] = "sphere"
        nstyle["size"] = 10
        nstyle["fgcolor"] = "darkred"

        nstyle["hz_line_type"] = 1
        nstyle["hz_line_color"] = "#cccccc"

        for n in t.traverse():
            n.set_style(nstyle)

        t.show(tree_style=ts)