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
import operator

os.chdir("../data")

# Blastn des 2 génomes (a)
blastn_g1_g2 = 'blastn -query genomes/"GCF_000007865.1_ASM786v1_genomic.fna" -subject genomes/"GCF_000009445.1_ASM944v1_genomic.fna" -outfmt 6 > results_blast/blastn_g1_g2.blastn'
os.system(blastn_g1_g2)

# Exposition des stats des fichiers des génomes pour choisir l'evalue la plus adapter
stats_g1 = 'seqkit stats genomes/"GCF_000007865.1_ASM786v1_genomic.fna"'
stats_g2 = 'seqkit stats genomes/"GCF_000009445.1_ASM944v1_genomic.fna"'
print("Voici les stats du génome 1 : ")
os.system(stats_g1)
print("Voici les stats du génome 2 : ")
os.system(stats_g2)

# Choix evalue pour recuperer les meilleurs hits
e = input("Entrer l'evalue souhaitée pour récupérer les meilleurs hits : ")

# Lecture du fichier, et récupération de la liste des meilleurs hits
f = open("results_blast/blastn_g1_g2.blastn")
reader = csv.reader(f, delimiter='\t')
f_r = open("results_blast/best_hits_blastn_g1_g2", "w")



f.close()
f_r.close()

# Blastn réciproque des 2 génomes (c)
blastn_g2_g1 = 'blastn -query genomes/"GCF_000009445.1_ASM944v1_genomic.fna" -subject genomes/"GCF_000007865.1_ASM786v1_genomic.fna" -outfmt 6 > results_blast/blastn_g2_g1.blastn'
os.system(blastn_g2_g1)