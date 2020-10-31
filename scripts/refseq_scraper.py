# -*- coding: utf-8 -*-
"""
@author: Ghassan Dabane
@title: refseq genomes scraper

based on refseq's assembly summary file : 
ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt

this file was downloaded and cleaned (with bash cut) by leaving out only 
Column  8: "organism_name"
Column  9: "infraspecific_name"
Column 20: "ftp_path"
(cutting its size significantly from ~64 Mb -> ~20 Mb)

a new column "readable" will be created with pandas to make it easier
for the user to choose a certain genome.
"""

import os
import sys
import pandas as pd
from ftplib import FTP

class RefSeqScraper : 
    
    def __init__(self) :
        __summary = pd.read_table('data/list_genomes_refseq.txt', header=1)
        __summary = __summary.fillna('')
        __summary['readable'] = __summary['organism_name'] + ' ' + \
                                __summary['infraspecific_name']
        self.data = __summary
        self.cart = []
        
    def __str__(self):
        return "Your cart is empty" if len(
            self.cart) == 0 else "Your cart contains %s" % self.cart    

    def extract_ftps(self, pattern) : 
        """Extracts ftp path from genomes given a user input pattern.
        
        Parameters
        ----------
        genomes : TYPE DataFrame
            refseq based DataFrame with 4 columns.
        pattern : TYPE str
            a regex pattern to find in the DataFrame.
    
        Returns
        -------
        TYPE array
            DESCRIPTION.
    
        """
        
        return self.data.loc[(self.data['readable'].str.contains(pattern)==True),
                           ['readable','ftp_path']]

    @staticmethod
    def download_genome(ftp_path) : 
        """This function downloads a FTP genome file given a specific ftp 
        address and saves it to /data/genomes directory.
        
        Parameters
        ----------
        ftp_path : TYPE str
            DESCRIPTION.
    
        Returns
        -------
        None.
        
        """
        with FTP('ftp.ncbi.nlm.nih.gov') as conn : 
            conn.login()
            conn.cwd(ftp_path[27:])
            conn.dir()
                       
            try :  
                genome = '%s_genomic.fna.gz' %(ftp_path.rsplit('/')[-1])
                local_save = os.path.join(os.getcwd(),'data/genomes/%s'%genome)
                
                with open(local_save, 'wb') as fp :
                    conn.retrbinary('RETR %s' %genome, fp.write)
            except : 
                print('error, cannot download genome file')


if __name__ == "__main__" : 
    
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir) # cd to project directory
    
    
    
    
S = RefSeqScraper()

print(S)
    
inp = input('Please provide a pattern to find if a genome exists in refseq \n')
pattern = '%s' % (inp)
pattern

S.extract_ftps(pattern)['ftp_path'].values

RefSeqScraper.download_genome(S.extract_ftps(pattern)[0])
