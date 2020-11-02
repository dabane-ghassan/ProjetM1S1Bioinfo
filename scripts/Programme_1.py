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
from seqkit_stats import stats

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
    acces_f = "results_blast/"+name_results_blast
    f = open(acces_f)
    pos_sep_between_p1_p2 = name_results_blast.find("_", 6)
    pos_point = name_results_blast.find(".")
    name_p1 = name_results_blast[6:pos_sep_between_p1_p2]
    name_p2 = name_results_blast[pos_sep_between_p1_p2+1:pos_point]
    acces_f_r = "results_blast/best_hits_blast_"+name_p1+"_"+name_p2+".blast"
    f_r = open(acces_f_r, "w")
    reader = csv.reader(f, delimiter='\t')
    for line in reader :
        e = float(line[11-1])
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

""" Option qui sera proposé si l'utilisateur souhaite changer l'evalue
# Exposition des stats des fichiers des protéomes pour choisir l'evalue la plus adapter
stats_1 = 'seqkit stats genomes/"Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa"'
stats_2 = 'seqkit stats genomes/"Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa"'
print("Voici les stats du proteome 1 : ")
os.system(stats_1)
print("Voici les stats du protéome 2 : ")
os.system(stats_2)
"""

# best hits du blast1 (b)
best_hits("blast_Yersinia_Aliivibrio.blast")

# Blast réciproque des 2 protéomes (c)
blast2 = blast("Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa", "Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa")
os.system(blast2)

# best hits du blast2 (b)
best_hits("blast_Aliivibrio_Yersinia.blast")

# Récupération des hits biderectionnels (c)
    # Mise en dictionnaire des n°accessions des best hits de chaque blast
    # premier numéro : numéro du blast ; deuxième numéro : numéro de la colonne contenant le n°accession
s1.1, s1.2, s2.1, s2.2 = set(), set(), set(), set()

f_blast1 = open("blast_Yersinia_Aliivibrio.blast")
f_blast2 = open("blast_Aliivibrio_Yersinia.blast")
reader = csv.reader(f, delimiter='\t')
for line in reader :
    