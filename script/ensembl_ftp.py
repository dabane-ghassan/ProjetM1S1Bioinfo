# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:23:56 2020

@author: KugelBlitZZZ
"""


from ftplib import FTP

conn = FTP("ftp.ensemblgenomes.org")
conn.login()
conn.cwd('pub/release-48/bacteria/fasta/bacteria_0_collection/bordetella_pertussis_tohama_i/dna/')
conn.dir()

try :  
    file = 'Bordetella_pertussis_tohama_i.ASM19571v1.dna.chromosome.Chromosome.fa.gz'
    with open(file, 'wb') as fp :
        conn.retrbinary('RETR %s' %file, fp.write)
except : 
    print('error')
    

# conn.nlst() pour avoir la liste des fichiers disponibles
