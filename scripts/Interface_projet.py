#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import os

class window(Tk) :

    def __init__(self):
        Tk.__init__(self)
        self.geometry('800x400')
        self.createMenuBar()
        self.title("Projet M1 DLAD 2020")
    
    def createMenuBar(self):
        menuBar = Menu(self)
        
        menuProteomes_in_disk = Menu(menuBar, tearoff=0)
        menuProteomes_in_disk.add_command(label="view and/or select proteomes", font=("courier", 15),command=self.proteomes_in_disk)
        menuBar.add_cascade(label="Proteomes in disk", font=("courier", 15), menu=menuProteomes_in_disk)

        menuDownload = Menu(menuBar, tearoff=0)
        menuDownload.add_command(label="Download proteome", font=("courier", 15))
        menuBar.add_cascade(label="Download", font=("courier", 15), menu=menuDownload)

        menuExit = Menu(menuBar, tearoff=0)
        menuExit.add_command(label="Exit", font=("courier", 15), command=self.quit)
        menuBar.add_cascade(label="Exit", font=("courier", 15), menu=menuExit)

        self.config(menu = menuBar) 

    def reset(self) :
        for widget in self.winfo_children() :
            if "listbox" in str(widget) :
                widget.destroy()

    def proteomes_in_disk(self) :
        self.reset()
        p_presents = Listbox(self ,selectmode=MULTIPLE, height=15, width=80, bg='white', font=("courier", 15), selectbackground='pink')
        p_presents.delete(0,END)
        list_proteomes = os.listdir("../data/genomes/")
        i=0
        for p in list_proteomes :
            p_presents.insert(i, p)
            i+=1
        p_presents.pack()
        
        B_validate = Button(self, text="Validate selection", height=2, width=20, font=("courier", 15))
        B_validate.pack()

    def validate_proteome_selection(self) :
        prot_select = p_presents.curselection()

if __name__ == '__main__':
    app = window()
    app.mainloop()
