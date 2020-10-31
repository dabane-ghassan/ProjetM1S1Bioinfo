# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 11:23:56 2020
@author: ghassan 
"""

import os
import sys
import pandas as pd
from ftplib import FTP

def list_genomes() : 
    genomes = pd.read_table('data/list_genomes_refseq.txt', header=1)
    genomes = genomes.fillna('')
    genomes['readable'] = genomes['organism_name'] + ' ' + genomes['infraspecific_name']
    
    inp = input('Please provide a pattern to find if a genome exists in refseq \n')
    pattern = '%s' % (inp)
    pattern
    return genomes


def extract_ftp(genomes, pattern) : 
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
    
    return genomes.loc[(genomes['readable'].str.contains(pattern)==True),
                       'ftp_path'].values


def download_genome(ftp_path) : 
    """This function downloads a FTP genome file given a specific ftp address
    and saves it to /data/genomes directory.
    
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
    
    
    
    


