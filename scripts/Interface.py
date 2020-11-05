#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def proteome_in_disk() :
    list_proteomes = os.listdir(Users/megane/Documents/GitHub/ProjetM1S1Bioinfo/data/genomes)
    v = IntVar
    i=0
    for p in list_proteomes :
        case = Checkbutton(variable=v, value=i, text=p)
        i+=1

def proteome_select() :
    case.select()
    case.deselect()
    return v.get()

from tkinter import *
import os

window = Tk()

# Création d'un canvas
top = Canvas(window, bg='ivory')
top.pack(side= TOP, padx=5, pady=5)

# Dans la principal interface de départ :
    # Affichage des protéomes présents dans le disque avec systeme de cochage
affichage_l_prot_in_disk = Label(text=proteome_in_disk)

# En bas de l'interface :
    # Bouton pour aller sélectionner des protéomes à télécharger
B_Download = Button(text="Download proteome")
B_Download.pack(side= LEFT, padx=15)

    # Bouton pour revenir à l'interface principale
B_interface_principale = Button(text="Back to main interface")
B_interface_principale.pack(side= RIGHT, padx=30)

window.mainloop()