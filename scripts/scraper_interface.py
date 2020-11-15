#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import refseq_scraper as rs


if __name__ == "__main__" : 
    
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_dir = os.path.dirname(script_dir)
    os.chdir(project_dir) # cd to project directory    
    
    S = RefSeqScraper()
    S.mine_species()
    S.download_genome()
