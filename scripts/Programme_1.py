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
    return "blast%s -query genomes/%s -subject genomes/%s -outfmt %s > results_blast/blast%s_%s_%s.blast" % (
        typ, query, subject, outfmt, typ, query, subject)


import os
import csv

os.chdir("../data")

# Blastn des 2 génomes (a)
blastn_g1_g2 = 'blastn -query genomes/"GCF_000007865.1_ASM786v1_genomic.fna" -subject genomes/"GCF_000009445.1_ASM944v1_genomic.fna" -outfmt 6 > results_blast/blastn_g1_g2.blastn'
os.system(blastn_g1_g2)

"""
blast1 = blast(proteome1, proteome2)
os.system(blast1)
"""

# Exposition des stats des fichiers des génomes pour choisir l'evalue la plus adapter
stats_g1 = 'seqkit stats genomes/"GCF_000007865.1_ASM786v1_genomic.fna"'
stats_g2 = 'seqkit stats genomes/"GCF_000009445.1_ASM944v1_genomic.fna"'
print("Voici les stats du génome 1 : ")
os.system(stats_g1)
print("Voici les stats du génome 2 : ")
os.system(stats_g2)

# Choix evalue pour recuperer les meilleurs hits
e = input("Entrer l'evalue souhaitée pour récupérer les meilleurs hits : ")

# Lecture du fichier résultat du blastn g1 -> g2, et récupération de la liste des meilleurs hits
f = open("results_blast/blastn_g1_g2.blastn")
f_r = open("results_blast/best_hits_blastn_g1_g2", "w")
reader = csv.reader(f, delimiter='\t')
for line in reader :
    evalue = line[11-1]
    if evalue < e :
        for element in line :
            f_r.write(element + "\t")
        f_r.write("\n")

f.close()
f_r.close()

# Blastn réciproque des 2 génomes (c)
blastn_g2_g1 = 'blastn -query genomes/"GCF_000009445.1_ASM944v1_genomic.fna" -subject genomes/"GCF_000007865.1_ASM786v1_genomic.fna" -outfmt 6 > results_blast/blastn_g2_g1.blastn'
os.system(blastn_g2_g1)

"""
blast2 = blast(proteome2, proteome1)
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
