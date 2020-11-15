#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox
import os
from blast_hitter import BlastHitter
from clusterizer import Clusterizer
from refseq_scraper import RefSeqScraper

class window(Tk) :

    def __init__(self):
        Tk.__init__(self)
        self.geometry('1100x400')
        self.createMenuBar()
        self.title("Projet M1 DLAD 2020")
    
    def createMenuBar(self):
        menuBar = Menu(self)
        
        menuBLAST = Menu(menuBar, tearoff=0)
        menuBLAST.add_command(label="BLAST", font=("courier", 15),command=self.proteomes_in_disk)
        menuBar.add_cascade(label="BLAST", font=("courier", 15), menu=menuBLAST)

        menuDownload = Menu(menuBar, tearoff=0)
        menuDownload.add_command(label="Download proteome", font=("courier", 15), command=self.Search_Download_proteome)
        menuBar.add_cascade(label="Download", font=("courier", 15), menu=menuDownload)

        menuEvalues = Menu(menuBar, tearoff=0)
        menuEvalues.add_command(label="Distributions of e-values", font=("courier", 15), command=self.distributions_of_evalues)
        menuBar.add_cascade(label="E-values", font=("courier", 15), menu=menuEvalues)

        menuStats = Menu(menuBar, tearoff=0)
        menuStats.add_command(label="See proteome statistics", font=("courier", 15), command=self.stats)
        menuBar.add_cascade(label="Statistics", font=("courier", 15), menu=menuStats)

        menuHelp = Menu(menuBar, tearoff=0)
        menuHelp.add_command(label="BLAST", font=("courier", 15))
        menuHelp.add_command(label="Download", font=("courier", 15))
        menuHelp.add_command(label="E-values", font=("courier", 15))
        menuBar.add_cascade(label="Help", font=("courier", 15), menu=menuHelp)

        menuExit = Menu(menuBar, tearoff=0)
        menuExit.add_command(label="Exit", font=("courier", 15), command=self.quit)
        menuBar.add_cascade(label="Exit", font=("courier", 15), menu=menuExit)

        self.config(menu = menuBar) 

    def reset(self) :
        for widget in self.winfo_children() :
            if "listbox" in str(widget) :
                widget.destroy()
            if "button" in str(widget) :
                widget.destroy()
            if "label" in str(widget) :
                widget.destroy()
            if "entry" in str(widget) :
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
        p_presents.pack(pady=15)
        
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
            bhitters = BlastHitter.from_list(proteomes) 
            for bh in bhitters :
                bh.blast_them()
                bh.rbh_them()
            tkinter.messagebox.showinfo(title="Good things come to those who wait for", message="BLAST and RBH job are finish. Please, wait that the full job is over.")
            clust = Clusterizer(bhitters, proteomes)
            clust.cluster_them()
            clust.one_align_to_rule_them_all()
            clust.draw_tree()

    def Search_Download_proteome(self) :
        self.reset()
        text = Label(text="Give me a few letters so i can search for you", font=("courier", 18))
        text.pack(pady=50)

        pattern = Entry(self, width=40, font=("courier", 15))
        pattern.pack()
        pattern.bind("<Return>", lambda x=None: self.Download_proteome(pattern))
    
    def Download_proteome(self, pattern) :
        print(pattern.get())

    def distributions_of_evalues(self) :
        self.reset()
        blast_presents = Listbox(self, height=15, width=110, bg='white', font=("courier", 15), selectbackground='pink')
        blast_presents.delete(0,END)
        list_blast = os.listdir("../data/results_blast/")
        for p in list_blast :
            start = p[0:3]
            i = 0
            if start != "RBH" :
                blast_presents.insert(i, p)
                i+=1
        blast_presents.pack(pady=15)

        B_validate = Button(self, text="Validate selection", height=2, width=20, font=("courier", 15), command=lambda: self.validate_blast_selection(blast_presents))
        B_validate.pack()

    def validate_blast_selection(self, blast_presents) :
        blast_select = blast_presents.curselection()
        histo = blast_presents.get(blast_select)
        BlastHitter.evalue_dist(histo)

    def stats(self) :
        self.reset()
        prot_presents = Listbox(self, height=15, width=80, bg='white', font=("courier", 15), selectbackground='pink')
        prot_presents.delete(0,END)
        list_prot = os.listdir("../data/genomes/")
        i=0
        for prot in list_prot :
            prot_presents.insert(i, prot)
            i+=1
        prot_presents.pack(pady=15)
        
        B_validate = Button(self, text="Validate selection", height=2, width=20, font=("courier", 15), command=lambda: self.validate_prot_select(prot_presents))
        B_validate.pack()

    def validate_prot_select(self, prot_presents) :
        prot_select = prot_presents.curselection()
        s = "../data/genomes/"+prot_presents.get(prot_select)
        BlastHitter.seqkit_stats(s) # voir pour couper la fonction seqkit ici et l'adapter en nouvelle fenetre qui s'ouvre

if __name__ == '__main__':
    app = window()
    app.mainloop()
