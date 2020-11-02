#!/usr/bin/env python3
#-*-coding: UTF-8-*-
"""
    Auteur : Mégane Boujeant
    Date : 31 Octobre 2020
    But : 
    	a. lance une recherche BLAST d'un génome requête contre un autre génome cible (paramètres)
    	b. lit le fichier résultat afin d'en récupérer la liste des meilleurs hits pour chaque protéine
    	c. lance la recherche BLAST réciproque afin d'en déduire la liste des hits bidirectionnels
"""

import os
import csv

def blast(query, subject, outfmt=6, typ="p") :
    """This function generates the blast command to be run given certain 
        parameters.
    
    Parameters
    ----------
    query : TYPE str
        the name of the query genome file.
    subject : TYPE str
        the name of the subject genome file.
    outfmt : TYPE int, optional
        blast results output format, The default is 6.
    typ : TYPE str, optional
        The type of blast to be executed (blastp, blastn, ....),
        default is "p".

    Returns
    -------
    TYPE str
        blast command to be executed.   
    """
    tiret_q = query.find('_')
    nom_query = query[0:tiret_q]
    tiret_s = subject.find('_')
    nom_subject = subject[0:tiret_s]
    return "blast%s -query genomes/%s -subject genomes/%s -outfmt %s > results_blast/blast_%s_%s.blast" % (
        typ, query, subject, outfmt, nom_query, nom_subject)

def best_hits(name_results_blast, evalue=1e-20) :
    f = open("results_blast/%s")%(name_results_blast)
    name_p1 = name_results_blast.find("_", )
    name_p2 = 
    f_r = open("results_blast/best_hits_blast_%s_%s", "w")%(name_p1, name_p2)
    reader = csv.reader(f, delimiter='\t')
    for line in reader :
        e = line[11-1]
        if e < evalue :
            for element in line :
                f_r.write(element + "\t")
            f_r.write("\n")
    f.close()
    f_r.close()

os.chdir("../data")

# Blast des 2 protéomes (a)
blast1 = blast("Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa","Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa")
os.system(blast1)

# Exposition des stats des fichiers des protéomes pour choisir l'evalue la plus adapter
stats_1 = 'seqkit stats genomes/"Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa"'
stats_2 = 'seqkit stats genomes/"Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa"'
print("Voici les stats du proteome 1 : ")
os.system(stats_1)
print("Voici les stats du protéome 2 : ")
os.system(stats_2)

# best hits du blast1 (b)
best_hits("blast_Yersinia_Aliivibrio.blast")

# Blast réciproque des 2 protéomes (c)
blast2 = blast("Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa", "Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa")
os.system(blast2)

# best hits du blast2 (b)
best_hits("blast_Aliivibrio_Yersinia.blast")

# Récupération des hits biderectionnels (c)
