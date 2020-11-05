#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def proteome_in_disk() :
    list_proteomes = os.listdir(/Users/megane/Documents/GitHub/ProjetM1S1Bioinfo/data/genomes)
    for p in list_proteomes :
        print p


from tkinter import *
import os

window = Tk()

# Dans la principal interface de départ :
    # Affichage des protéomes présents dans le disque avec systeme de cochage

Label(text=proteome_in_disk)

# En bas de l'interface :
    # Bouton pour aller sélectionner des protéomes à télécharger
    # Bouton pour revenir à l'interface principale

window.mainloop()