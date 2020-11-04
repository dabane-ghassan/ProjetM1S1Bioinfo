#!/usr/bin/env python3
#-*-coding: UTF-8-*-

def parse_fasta(proteome):
    """This function parses proteome fasta files.

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


def seqkit_stats(proteome):
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
    seqdic = parse_fasta(proteome)  # parsing proteome to get a dictionary
    length_seq = [len(seq) for seq in seqdic.values()
                  ]  # to facilitate calculating min, max, sum and average

    print(
        " name : %s \n num_seq : %s \n sum_len : %s \n min_len : %s \n avg_len : %s \n max_len : %s"
        % (proteome.rsplit('/')[-1], len(
            seqdic.keys()), sum(length_seq), min(length_seq),
           sum(length_seq) / len(seqdic.keys()), max(length_seq)))


def blast(query, subject, outfmt=6, typ="p"):
    """This function generates the blast command to be run given certain 
        parameters. the output file is saved to data/results_blast
    
    Parameters
    ----------
    query : TYPE str
        the name of the query genome file.
    subject : TYPE str
        the name of the subject genome file.
    out : TYPE str
        the name of the output file.
    outfmt : TYPE int, optional
        blast results output format, The default is 6.
    typ : TYPE str, optional
        The type of blast to be executed (blastp, blastn, ....),
        default is "p".

    Returns
    -------
    TYPE tuple
        blast command to be executed and the name of the output file  
    """
    query_name = query.rsplit('/')[-1]
    query_name = query_name[0:query_name.find('_')]
    subject_name = subject.rsplit('/')[-1]
    subject_name = subject_name[0:subject_name.find('_')]
    out = "../data/results_blast/blast_%s_%s.blastp" % (query_name,
                                                        subject_name)

    return "blast%s -query %s -subject %s -outfmt %s > %s" % (
        typ, query, subject, outfmt, out), out


def best_hits(blast_out, evalue=1e-20):
    """This function filters the blast output file into another best hits file
        based on a given evalue.
    
    Parameters
    ----------
    blast_out : TYPE str
        DESCRIPTION. the blast output file .blastp path
    evalue : TYPE int, optional
        DESCRIPTION. the evalue to consider while filtering,
                    The default is 1e-20.

    Returns
    -------
    bhits_out : TYPE str
        DESCRIPTION. the best hits blast file path

    """

    bhits_out = "../data/results_blast/best_hits_%s" % blast_out.rsplit(
        '/')[-1]
    with open(blast_out, 'r') as bfile, open(bhits_out, 'w') as bhits:
        bhits.writelines(
            [line for line in bfile if float(line.split('\t')[10]) <= evalue])
    return bhits_out 

def extract_best_hits(proteome, bhits_out) : 
    
    extract_bh_out = "../data/genomes/best_hits_%s"%(proteome.rsplit(
        '/')[-1])

    with open(bhits_out , 'r') as bhits : 
        bh_ids = [line.split('\t')[1] for line in bhits]
    
    best_hits = {h:seq for h, seq in parse_fasta(proteome).items() if h[1:15] in bh_ids}
    
    with open(extract_bh_out, 'w') as bh_proteome : 
        for header, sequence in best_hits.items() : 
            bh_proteome.write('%s\n%s\n'%(header,sequence))
    
    return extract_bh_out


def bidir_best_hits(bhits_out1, bhits_out2) :
    
    
    with open(bhits_out1, 'r') as first_blast, open(
        bhits_out2, 'r') as second_blast, open(
            '../data/results_blast/rbh.txt', 'w') as rbh_file :
    
        hsps = [(line.split('\t')[1], line.split('\t')[0])
                 for line in second_blast]

        rbh_file.writelines(['%s %s\n' % couple for couple in rbh])

        rbh_file.writelines([line for line in first_blast if (
            line.split('\t')[0], line.split('\t')[1]) in hsps])
