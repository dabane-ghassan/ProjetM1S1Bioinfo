#!/usr/bin/env python3
#-*-coding: UTF-8-*-

import os

class BlastHitter : 
    
    def __init__(self, query, subject) : 
        
        self.query_path = query
        self.query_name = query.rsplit( # extraire le nom sans l'extension
            '/')[-1][0: query.rsplit('/')[-1].find('_protein.faa')]

        self.subject_path = subject
        self.subject_name = subject.rsplit( 
            '/')[-1][0: subject.rsplit('/')[-1].find('_protein.faa')]
        
        self.results_dir = "../data/results_blast"
        self.genomes_dir = "../data/genomes"
    
    def __str__(self):
        return "Hello There ! I'm a BlastHitter Object ! My goal is to find the reciprocal best hits between %s and %s" % (
            self.query_name, self.subject_name)
    
    @staticmethod
    def parse_fasta(proteome):
    
        list_seqs = open(proteome, 'r').read().split('>')[1:]  # split the file
        seqdic = {}
    
        for seq in list_seqs:
            seq = seq.strip().split(
                '\n')  # strip each sequence from spaces then split it
            seqdic['>' + seq[0]] = ''.join(seq[1:])
        return seqdic
    
    @staticmethod
    def seqkit_stats(proteome):

        seqdic = BlastHitter.parse_fasta(proteome)   
        length_seq = [len(seq) for seq in seqdic.values()
                      ]  # to facilitate calculating min, max, sum and average
    
        print(
            " name : %s \n num_seq : %s \n sum_len : %s \n min_len : %s \n avg_len : %s \n max_len : %s"
            % (proteome.rsplit('/')[-1], len(
                seqdic.keys()), sum(length_seq), min(length_seq),
               sum(length_seq) / len(seqdic.keys()), max(length_seq)))
    
    @staticmethod
    def universal_blast(query, subject, out, outfmt=6, typ="p"):
      
        return "blast%s -query %s -subject %s -outfmt %s > %s" % (
            typ, query, subject, outfmt, out)
    
    @staticmethod
    def best_hits_from_blast(blastp_file) : 
        
        besthits_dict = {}

        with open(blastp_file, 'r') as bp: 
            for line in bp : 
                query = line.split('\t')[0]
                if query not in besthits_dict.keys() : 
                    besthits_dict[query] = line.split('\t')[1]
        return besthits_dict
    
    
    @staticmethod       
    def bidir_best_hits(blastp1, blastp2, out) :
        
        bh_dict1, bh_dict2 = BlastHitter.best_hits_from_blast(
            blastp1), BlastHitter.best_hits_from_blast(blastp2)
        
        bidir_bh = list(set([(s, q) for q, s in bh_dict2.items()]) & set(
            [(s, q) for s, q in bh_dict1.items()]))

        
        with open(blastp1, 'r') as bf, open(out, 'w') as rbh_file :
                 
            rbh_file.writelines([line for line in bf if (
                line.split('\t')[0], line.split('\t')[1]) in bidir_bh])
            
    @staticmethod
    def best_hits_extractor(blastp_file, proteome, out, evalue=1e-20):
   
        with open(blastp_file, 'r') as bfile :
            bh_ids = [line.split('\t')[1] for line in bfile if float(
                line.split('\t')[10]) <= evalue]
        
        best_hits = {h:seq for h, seq in BlastHitter.parse_fasta(
            proteome).items() if h[1:15] in bh_ids}
        
        with open(out, 'w') as bh_proteome : 
            for header, sequence in best_hits.items() : 
                bh_proteome.write('%s\n%s\n'%(header,sequence))
                
    
    def blast_them(self) : 
        
        out_firstblast = "%s/%s_vs_%s.blastp" % (
            self.results_dir, self.query_name, self.subject_name)
        
        first_blastcmd = BlastHitter.universal_blast(
            self.query_path, self.subject_path, out_firstblast)
        
        out_secondblast = "%s/%s_vs_%s.blastp" % (
            self.results_dir, self.subject_name, self.query_name)
               
        second_blastcmd = BlastHitter.universal_blast(
            self.subject_path, self.query_path, out_secondblast)
        
        os.system("%s && %s" % (first_blastcmd, second_blastcmd))
        
        self.first_blastp = out_firstblast
        self.second_blastp = out_secondblast        

        return self.first_blastp, self.second_blastp
    
    
    def cluster_them(self) : 
         
        out_path = "%s/RBH_%s_%s.blastp" %(self.results_dir, self.query_name,
                                           self.subject_name)
        
        BlastHitter.bidir_best_hits(
            self.first_blastp, self.second_blastp, out_path)
        
        self.rbh = out_path
        return out_path
        
    
    


