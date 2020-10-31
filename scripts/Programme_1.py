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

# Blast
blastn_g1_g2 = 'blastn -query ../data/genomes/"GCF_000007865.1_ASM786v1_genomic.fna" -subject ../data/genomes/"GCF_000009445.1_ASM944v1_genomic.fna" -outfmt 6 > ../data/results_blast/blastp_g1_g2.blastn'
os.system(blastn_g1_g2)