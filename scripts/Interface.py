#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def proteome_in_disk() :
    list_proteomes = os.listdir("../data/genomes/")
    i=0
    for p in list_proteomes :
        p_presents.insert(i, p)
        i+=1

from tkinter import *
import os

window = Tk()

# Création d'un canvas
top = Canvas(window, bg='ivory')
top.pack(side= TOP, padx=5, pady=5)

# Main interface :
    # Affichage des protéomes présents dans le disque avec systeme de sélection
p_presents = Listbox(top ,selectmode=MULTIPLE)
p_presents.insert(1,"Bonjour")
proteome_in_disk()

prot_select = p_presents.curselection()

# En bas de l'interface :
    # Bouton pour aller sélectionner des protéomes à télécharger
B_Download = Button(text="Download proteome")
B_Download.pack(side= LEFT, padx=15)

    # Bouton pour revenir à l'interface principale
B_interface_principale = Button(text="Back to main interface", command=proteome_in_disk)
B_interface_principale.pack(side= RIGHT, padx=30)

window.mainloop()