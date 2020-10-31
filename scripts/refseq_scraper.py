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
        __summary = __summary[['readable','ftp_path']]                               
        self.data = __summary
        self.cart = []
        
    def __str__(self) :
        
        return "Your cart is empty" if len(
            self.cart) == 0 else "Your cart contains %s" % self.cart 


    def add_to_cart(self, species) : 
        
        self.cart.append(species)
        return "added %s to cart" % (species)    
       
    def mine_species(self) :
        
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        searching = True
        while searching : 
            pattern = input('Give me a few letters so i can search for you.\n')
            print(self.data.loc[(self.data['readable'].str.contains(pattern)),
                          'readable'])
            if input("Did you find what you're looking for? (yes/no) \n ") == "yes" : 
                searching = False
                answer = input("which of them would you like to add? \n")
                self.add_to_cart(answer)

        
    def mine_ftps(self) : 

        return self.data.loc[(self.data['readable'].str.contains('|'.join(self.cart))),
                           'ftp_path'].values


    def download_genome(self) : 
        
        for name, ftp_path in zip(self.cart, self.mine_ftps()) : 

            with FTP('ftp.ncbi.nlm.nih.gov') as conn : 
                conn.login()
                conn.cwd(ftp_path[27:])
                           
                try :  
                    genome = '%s_genomic.fna.gz' %(ftp_path.rsplit('/')[-1])
                    local_save = os.path.join(os.getcwd(),'data/genomes/%s%s'%(name,genome))
                    
                    with open(local_save, 'wb') as fp :
                        conn.retrbinary('RETR %s' %genome, fp.write)
                except : 
                    print('Error has occured while downloading this genome file')


if __name__ == "__main__" : 
    
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir) # cd to project directory    
    
    S = RefSeqScraper()
    print(S)

    S.mine_species()
    S.download_genome()



