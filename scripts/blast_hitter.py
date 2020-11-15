#!/usr/bin/env python3
#-*-coding: UTF-8-*-

import os
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

class BlastHitter:
    """This is a class for BLASTing two genomes against each other and
    for deducing reciprocal best hits that are common between the two 
    blastp results files.
    
    Attributes
    ----------
    query_path : str
        the relative path for the query genome file on the disk.        
    query_name : str
        the name of the query genome.
    subject_path : str
        the relative path for the subject genome file on the disk.
    query_name : str
        the name of the subject genome.
    results_dir : str
        the relative path of the results repository for saving output files.
    genomes_dir : str
        the relative path of the genomes repository.       
    first_blastp : str
        the path of the first .blastp file (query vs. subject blast).
    second_blastp : str
        the path of the second .blastp file (subject vs. query blast).
    rbh : str
        the path of the reciprocal best hits file (.blastp tabulated format).
    """
    def __init__(self, query, subject):
        """The class constructor, only specifying the query and subject
        path on the disk is sufficient for deducing other object attributes.
        
        Parameters
        ----------
        query : str
            the relative path for the query genome file on the disk.
        subject : str
            the relative path for the subject genome file on the disk.

        Returns
        -------
        Class object.
        """

        self.query_path = query
        self.query_name = query.rsplit(
            '/')[-1][0:query.rsplit('/')[-1].find('_protein.faa')]

        self.subject_path = subject
        self.subject_name = subject.rsplit(
            '/')[-1][0:subject.rsplit('/')[-1].find('_protein.faa')]

        self.results_dir = "../data/results_blast"
        self.genomes_dir = "../data/genomes"

    def __str__(self):
        """A Method for printing the object inside python's print function.
        
        Returns
        -------
        str
            a message representing the two genomes that the object is working 
            on.
        """
        return "Hello There ! I'm a BlastHitter Object ! " + \
            "My goal is to find the reciprocal best hits between %s and %s" % (
            self.query_name, self.subject_name)

    @staticmethod
    def parse_fasta(proteome):
        """This function parses a genome/proteome a file.

        Parameters
        ----------
        proteome : str
            the path of the genome/proteome file.

        Returns
        -------
        seqdic : dict             
            dictionary with protein accessions as keys and the corresponding
            fasta sequences as values.
        """

        list_seqs = open(proteome, 'r').read().split('>')[1:] # split the file
        seqdic = {}

        for seq in list_seqs:
            seq = seq.strip().split(
                '\n')  # strip each sequence from spaces then split it
            seqdic['>' + seq[0]] = ''.join(seq[1:])
        return seqdic

    @staticmethod
    def seqkit_stat(proteome):
        """This function prints important information about the proteome
        that will be analyzed. It parses the genome first then prints the 
        number of sequences, cumulated length, minimum, average and maximum 
        length. It mimics seqkit stats output.
        
        Parameters
        ----------
        proteome : str
            the path of the proteome file.

        Returns
        -------
        None.

        """

        seqdic = BlastHitter.parse_fasta(proteome)
        length_seq = [len(seq) for seq in seqdic.values()
                      ]  # to facilitate calculating min, max, sum and average

        return " name : %s \n num_seq : %s \n sum_len : %s \n min_len : %s \n avg_len : %s \n max_len : %s" % (
                proteome.rsplit('/')[-1], len(
                seqdic.keys()), sum(length_seq), min(length_seq),
                sum(length_seq) / len(seqdic.keys()), max(length_seq))
        
    @staticmethod
    def evalue_dist(blastp):
        """Generates an evalue distribution plot from a given blastp file.
        
        Parameters
        ----------
        blastp : str
            The blast file path to be analyzed.

        """
        
        evals = np.array([line.split('\t')[10] for line in open(
            '../data/results_blast/%s' % blastp, 'r')], dtype=float)
        
        bp = blastp[:blastp.find('.blastp')].rsplit('/')[-1]
        
        title = bp[:bp.find('_strain')] + bp[
            bp.find('_vs_'):bp.find('_strain', bp.find('_vs_'))]

        fig, ax = plt.subplots(1, 1, dpi=300)
        ax.hist(evals, bins=100, color="fuchsia")
        ax.set_xticks(np.arange(0,11))
        ax.set_xlabel('e-value')
        ax.set_ylabel('Nomber of hits')
        fig.suptitle(title)
        fig.savefig('../data/figures/%s.png' % title)


    @staticmethod
    def universal_blast(query, subject, out, outfmt=6, typ="p"):
        """Returns the blast command to be executed in the terminal.    

        Parameters
        ----------
        query : str
            query proteome file path.
        subject : str
            subject proteome file path.
        out : str
            blast output file path.
        outfmt : int, optional
            blast results format. The default tabulated without headers = 6.
        typ : str, optional
            type of blast to run. The default is blastp.

        Returns
        -------
        str
        """

        return "blast%s -query %s -subject %s -outfmt %s > %s" % (
            typ, query, subject, outfmt, out)

    @staticmethod
    def best_hits_from_blast(blastp_file):
        """Returns the best hit for every protein based on the blast output
        file. The algorithm is simple, take the first appearance of the 
        protein as the best hit because BLAST sends back the best hits in
        descending order of quality.
        

        Parameters
        ----------
        blastp_file : str
            The blast output file with a tabulated format (outfmt = 6).

        Returns
        -------
        besthits_dict : dict
            a dictionary that contains all protein queries of a given genome,
            with our query as a key, and the corresponding best hit as a value.

        """

        besthits_dict = {}

        with open(blastp_file, 'r') as bp:
            for line in bp:
                query = line.split('\t')[0]
                if query not in besthits_dict.keys():
                    besthits_dict[query] = line.split('\t')[1]
        return besthits_dict

    @staticmethod
    def bidir_best_hits(blastp1, blastp2, out):
        """This function determines the reciprocal best hits between two blast
        files, it calls the class's best_hits_from_blast static method to 
        determine the best hits for every blast file, creates two sets of 
        tuples; query and best hit for the first blast, best hit and query
        for the second blast (inverses the second blast file). it then 
        proceeds with the intersection between our two sets in order to
        establish the reciprocal best hits (RBH).
        

        Parameters
        ----------
        blastp1 : str
            The First blast file path.
        blastp2 : str
            The second blast file path.
        out : str
            The reciprocal best hits output file path, tabulated (outfmt = 6).

        Returns
        -------
        None.
        Creates an out RBH file based on the first blast file after 
        calculating the reciprocal best hits.

        """

        bh_dict1, bh_dict2 = BlastHitter.best_hits_from_blast(
            blastp1), BlastHitter.best_hits_from_blast(blastp2)

        bidir_bh = list(
            set([(s, q) for q, s in bh_dict2.items()])
            & set([(q, s) for q, s in bh_dict1.items()]))

        with open(blastp1, 'r') as bf, open(out, 'w') as rbh_file:

            rbh_file.writelines([
                line for line in bf
                if (line.split('\t')[0], line.split('\t')[1]) in bidir_bh
            ])
    
    @classmethod
    def from_list(cls, prots_list):
        """This class method instantiates BlastHitter objects from a list of
        proteomes/genomes.
        
        
        Parameters
        ----------
        prots_list : list
            a list of genomes/proteoms file paths.

        Returns
        -------
        list
            a list of BlastHitter objects.

        """
        return [cls(couple[0], couple[1]) for couple in list(
            combinations(prots_list, 2))]

    def blast_them(self):
        """This method launches two BLASTs, our two genomes against each other.
        it uses the class's static methods defind earlier.
        
        Returns
        -------
        str
            The first blast output file path.
        str
            The second blast output file path.

        """

        out_firstblast = "%s/%s_vs_%s.blastp" % (
            self.results_dir, self.query_name, self.subject_name)

        first_blastcmd = BlastHitter.universal_blast(self.query_path,
                                                     self.subject_path,
                                                     out_firstblast)

        out_secondblast = "%s/%s_vs_%s.blastp" % (
            self.results_dir, self.subject_name, self.query_name)

        second_blastcmd = BlastHitter.universal_blast(self.subject_path,
                                                      self.query_path,
                                                      out_secondblast)

        os.system("%s && %s" % (first_blastcmd, second_blastcmd))

        self.first_blastp = out_firstblast
        self.second_blastp = out_secondblast

        return self.first_blastp, self.second_blastp

    def rbh_them(self):
        """ This method calculates the reciprocal best hits between our two 
        genomes after BLASTing them, it creates the RBH file.
        
        Returns
        -------
        str
            The RBH output file path.

        """

        out_path = "%s/RBH_%s_%s.blastp" % (self.results_dir, self.query_name,
                                            self.subject_name)

        BlastHitter.bidir_best_hits(self.first_blastp, self.second_blastp,
                                    out_path)

        self.rbh = out_path
        return out_path
    
    def getRbh(self):
        """The getter of the RBH file path for a certain blasthitter object.

        Returns
        -------
        str
            RBH file path.

        """       
        return self.rbh

    
    
    
    
    
    
    
