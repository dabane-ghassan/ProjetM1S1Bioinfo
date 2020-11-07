#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox
import os
from blast_hitter import BlastHitter
from clusterizer import Clusterizer

class window(Tk) :

    def __init__(self):
        Tk.__init__(self)
        self.geometry('800x400')
        self.createMenuBar()
        self.title("Projet M1 DLAD 2020")
    
    def createMenuBar(self):
        menuBar = Menu(self)
        
        menuBLAST = Menu(menuBar, tearoff=0)
        menuBLAST.add_command(label="BLAST", font=("courier", 15),command=self.proteomes_in_disk)
        menuBar.add_cascade(label="BLAST", font=("courier", 15), menu=menuBLAST)

        menuDownload = Menu(menuBar, tearoff=0)
        menuDownload.add_command(label="Download proteome", font=("courier", 15))
        menuBar.add_cascade(label="Download", font=("courier", 15), menu=menuDownload)

        menuHelp = Menu(menuBar, tearoff=0)
        menuHelp.add_command(label="Help", font=("courier", 15))
        menuBar.add_cascade(label="Help", font=("courier", 15), menu=menuHelp)

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
        
        B_validate = Button(self, text="Validate selection", height=2, width=20, font=("courier", 15), command=lambda: self.validate_proteome_selection(p_presents))
        B_validate.pack()

    def validate_proteome_selection(self,p_presents) :
        prot_select = p_presents.curselection()
        if len(prot_select) < 2 :
            tkinter.messagebox.showinfo(title=None, message="Please, select two or more proteomes")
        else:
            tkinter.messagebox.showinfo(title="loading", message="Please, wait for the job to finish. Do not exit the application.")
            proteomes=[]
            for p in prot_select:
                proteomes.append("../data/genomes/"+p_presents.get(p))
            for bh in BlastHitter.from_list(proteomes) : 
                bh.blast_them()
                bh.rbh_them()
            more = tkinter.messagebox.askyesno(title="BLAST", message="The BLAST is finish. Do you want to see more ?")


if __name__ == '__main__':
    app = window()
    app.mainloop()
