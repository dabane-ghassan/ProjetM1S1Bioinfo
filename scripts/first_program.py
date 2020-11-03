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


"""
os.chdir("../data")
# Blast des 2 protéomes (a)
blast1 = blast("Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa","Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa")
os.system(blast1)

# best hits du blast1 (b)
best_hits("blast_Yersinia_Aliivibrio.blast")

# Blast réciproque des 2 protéomes (c)
blast2 = blast("Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa", "Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa")
os.system(blast2)

# best hits du blast2 (b)
best_hits("blast_Aliivibrio_Yersinia.blast")


# Récupération des hits biderectionnels (c)
    # Mise en dictionnaire des n°accessions des best hits de chaque blast
    # Pour chaque dictionnaire, la key est le n°accession de la protéine dans la query, et la value est le n°accession de la protéine dans le subject
dict_blast1 = dict()
f_blast1 = open("results_blast/best_hits_blast_Yersinia_Aliivibrio.blast")
reader = csv.reader(f_blast1, delimiter='\t')
for line in reader :
    dict_blast1.update({line[1-1]:line[2-1]})
f_blast1.close()
print(dict_blast1)
dict_blast2 = dict()
f_blast2 = open("results_blast/best_hits_blast_Aliivibrio_Yersinia.blast")
reader = csv.reader(f_blast2, delimiter='\t')
for line in reader :
    dict_blast2.update({line[1-1]:line[2-1]})
f_blast2.close()

    # Vérification si hit est bidirectionnel
    # Si oui, ajout des n°accessions dans un fichier
f_hits_bidir = open("results_blast/best_hits_bidir_Yersinia_Aliivibrio.txt", "w")
for key, value in dict_blast1.items() :
    if key in dict_blast2 and value in dict_blast1 :
        print(essai)

f_hits_bidir.close()
"""
