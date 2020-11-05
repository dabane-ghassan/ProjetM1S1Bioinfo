#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import os

class window(Tk) :

    def __init__(self):
        Tk.__init__(self)
        self.createMenuBar()
        self.title("Projet M1 DLAD 2020")
    
    def createMenuBar(self):
        menuBar = Menu(self)
        
        menuProteomes_in_disk = Menu(menuBar, tearoff=0)
        menuProteomes_in_disk.add_command(label="view and/or select proteomes", command=self.proteomes_in_disk)
        menuBar.add_cascade(label="Proteomes in disk", menu=menuProteomes_in_disk)

        menuExit = Menu(menuBar, tearoff=0)
        menuExit.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="Exit", menu=menuExit)

        self.config(menu = menuBar) 

    def proteomes_in_disk(self) :
        p_presents = Listbox(window ,selectmode=MULTIPLE, width=80, bg='white', selectbackground='pink')
        p_presents.delete(0,END)
        list_proteomes = os.listdir("../data/genomes/")
        i=0
        for p in list_proteomes :
            p_presents.insert(i, p)
            i+=1
        p_presents.pack()



window = window()
window.mainloop()
