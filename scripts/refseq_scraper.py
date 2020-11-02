# -*- coding: utf-8 -*-
"""
@author: ghassan
@title: refseq genomes scraper

based on refseq's assembly summary file : 
ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt

a new column "readable" will be created with pandas to make it easier
for the user to choose a certain genome.
"""
import os
import pandas as pd
from ftplib import FTP


class RefSeqScraper : 
    
    def __init__(self) :
        """This function is used for instantiating RefSeqScraper objects,
        it will scan refseq summary assembly dataframe, pick only latest and 
        complete genomes and then will create a new column 'readable' that is
        the combination of organism and infraspecific name columns.
        This class has 2 properties : 
            data : a pandas dataframe that contains all refseq genomes.
            cart : a list of species names to download their genomes.
        """
        
        __summary = pd.read_table('data/list_genomes_refseq.txt', header=1)
        __summary = __summary.fillna('')
        __summary = __summary[(__summary['assembly_level'] == "Complete Genome")
                              & (__summary['version_status'] == 'latest')]
        __summary['readable'] = __summary['organism_name'] + ' ' + \
                                __summary['infraspecific_name']
        __summary = __summary[['readable','ftp_path']]                               
        self.data = __summary
        self.cart = []
        
    def __str__(self) :
        """Returns a string representation of the object's cart, empty 
        otherwise.
        """
        
        return "Your cart is empty" if len(
            self.cart) == 0 else "Your cart contains %s" % self.cart 


    def add_to_cart(self, species) : 
        """ this function adds a species to the object's cart.

        Parameters
        ----------
        species : TYPE str
            DESCRIPTION. the name of the species to be downloaded,
                        should match, records in the dataframe.

        Returns
        -------
        TYPE str
            DESCRIPTION. a sentence that confirms the addition of a given
                        species to the cart.
        """
        
        self.cart.append(species)
        return "added %s to cart" % (species)    
       
    def mine_species(self) :
        """Asks the user to give a few letters and finds a few records in the
        dataframe that correspond to the input pattern, if the user would like
        to add something that he sees, it does it.
        """
                
        searching = True
        while searching : 
            pattern = input('Give me a few letters so i can search for you.\n')
            print(self.data.loc[(self.data['readable'].str.contains(pattern)),
                          'readable'].to_string())
            question = input("Did you find what you're looking for? (yes/no)\n")
            if  question == "yes" : 
                searching = False
                answer = input("which of them would you like to add? \n")
                self.add_to_cart(answer)


        
    def mine_ftps(self) : 
        """This function searches the dataframe and extracts the ftps that 
        correspond to species in the cart.
        

        Returns
        -------
        TYPE list
            DESCRIPTION. a list of ftp paths

        """

        return self.data.loc[(self.data['readable'].str.contains('|'.join(self.cart))),
                           'ftp_path'].values


    def download_genome(self) : 
        """Downloads all genomes from the ftps paths in the cart and saves 
        them to data/genomes directory.   
        """

        
        for name, ftp_path in zip(self.cart, self.mine_ftps()) : 

            with FTP('ftp.ncbi.nlm.nih.gov') as conn : 
                conn.login()
                conn.cwd(ftp_path[27:])
                           
                try :  
                    genome = '%s_protein.faa.gz' %(ftp_path.rsplit('/')[-1])
                    local_save = os.path.join(os.getcwd(),'data/genomes/%s_protein.faa.gz'%(name.replace(' ', '_')))
                    
                    with open(local_save, 'wb') as fp :
                        conn.retrbinary('RETR %s' %genome, fp.write)
                except : 
                    print('Error has occured while downloading this genome file')


