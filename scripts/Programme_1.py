#!/usr/bin/env python3
#-*-coding: UTF-8-*-
"""
    Auteur : Mégane Boujeant
    Date : 31 Octobre 2020
    But : 
    	a. lance une recherche BLAST d'un génome requête contre un autre génome cible (paramètres)
    	b. lit le fichier résultat afin d'en récupérer la liste des meilleurs hits pour chaque protéine
    	c. lance la recherche BLAST réciproque afin d'en déduire la liste des hits bidirectionnels

peut être utiliser subprocess pour accueillir l'output de blast dans un variable python direct???
proposition des fonctions

1. fonction blast : 
    
test : 
blast1 = blast("GCF_000007865.1_ASM786v1_genomic.fna","GCF_000009445.1_ASM944v1_genomic.fna", typ="n")
os.system(blast1)
    
2. fonction best hit

"""

def blast(query, subject, evalue=1e-20, outfmt=6, typ="p") :
    """This function generates the blast command to be run given certain 
        parameters.
    
    Parameters
    ----------
    query : TYPE str
        the name of the query genome file.
    subject : TYPE str
        the name of the subject genome file.
    evalue : TYPE int, optional
        the evalue threshhold for the blast, The default is 1e-20.
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


import os
import csv

os.chdir("../data")

# Blastn des 2 génomes (a)
blast1 = blast("Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa","Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa")
os.system(blast1)

# Exposition des stats des fichiers des génomes pour choisir l'evalue la plus adapter
stats_1 = 'seqkit stats genomes/"Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa"'
stats_2 = 'seqkit stats genomes/"Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa"'
print("Voici les stats du proteome 1 : ")
os.system(stats_1)
print("Voici les stats du protéome 2 : ")
os.system(stats_2)

"""
# Choix evalue pour recuperer les meilleurs hits
e = input("Entrer l'evalue souhaitée pour récupérer les meilleurs hits : ")

# Lecture du fichier résultat du blastn g1 -> g2, et récupération de la liste des meilleurs hits
f = open("results_blast/blastp_Yersinia pestis strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa_Aliivibrio salmonicida LFI1238 strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa.blast"")
f_r = open("results_blast/best_hits_blastn_1_2", "w")
reader = csv.reader(f, delimiter='\t')
for line in reader :
    evalue = line[11-1]
    if evalue < e :
        for element in line :
            f_r.write(element + "\t")
        f_r.write("\n")

f.close()
f_r.close()
"""

# Blastn réciproque des 2 génomes (c)
blast2 = blast("Aliivibrio_salmonicida_LFI1238_strain=LFI1238GCF_000196495.1_ASM19649v1_protein.faa", "Yersinia_pestis_strain=FDAARGOS_603GCF_003798205.1_ASM379820v1_protein.faa")
os.system(blast2)

"""
# Lecture du fichier résultat du blastn g2 -> g2, et récupération de la liste des meilleurs hits
f2 = open("results_blast/blastn_g2_g1.blastn")
f_r2 = open("results_blast/best_hits_blastn_g2_g1", "w")
reader2 = csv.reader(f2, delimiter='\t')
for line in reader2 :
    evalue = line[11-1]
    if evalue < e :
        for element in line :
            f_r2.write(element + "\t")
        f_r2.write("\n")

f2.close()
f_r2.close()

# Récupération des hits biderectionnels
"""