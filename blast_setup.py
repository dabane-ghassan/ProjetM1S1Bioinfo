#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 09:17:12 2020

@author: ghassan
"""

import os
import getpass

msg = "Welcome ! Please provide your machine's sudo password to install blast locally \n \n"
sudopass = getpass.getpass(msg)

install = 'apt-get install ncbi-blast+'

os.system('echo %s|sudo -S %s' % (sudopass, install))


