#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
import os
from blast_hitter import BlastHitter
from clusterizer import Clusterizer
from refseq_scraper import RefSeqScraper

class window(Tk) :
    """ This is a class to have a graphical interface which offer different 
    functionalities of the project.
    
    This class has 5 properties : 
        Make_a_Tree : 
            feature that allows to make a phylogenetic tree from BLAST.
        Download : 
            feature that allows to download proteomes.
        E-values : 
            feature that allows to see distribution of e-values from a BLAST.
        Statistics : 
            feature that allows to see statistics of a proteome. 
        Exit : 
            Button in the menu for exit the graphical interface.
    """

    def __init__(self):
        """ The class constructors. It initialize the main window of the 
        graphical interface.
        """

        Tk.__init__(self)
        self.geometry('1100x400')
        self.createMenuBar()
        self.title("Projet M1 DLAD 2020")
    
    def createMenuBar(self):
        """ This function create a menu bar that contains several tabs.
        Each tab gives access to a feature.
        """

        menuBar = Menu(self)
        
        menuTree = Menu(menuBar, tearoff=0)
        menuTree.add_command(label="Blast to Tree", font=("courier", 15),command=self.proteomes_in_disk)
        menuBar.add_cascade(label="Make_a_Tree", font=("courier", 15), menu=menuTree)

        menuDownload = Menu(menuBar, tearoff=0)
        menuDownload.add_command(label="Download proteome", font=("courier", 15), command=self.Search_Download_proteome)
        menuBar.add_cascade(label="Download", font=("courier", 15), menu=menuDownload)

        menuEvalues = Menu(menuBar, tearoff=0)
        menuEvalues.add_command(label="Distributions of e-values", font=("courier", 15), command=self.distributions_of_evalues)
        menuBar.add_cascade(label="E-values", font=("courier", 15), menu=menuEvalues)

        menuStats = Menu(menuBar, tearoff=0)
        menuStats.add_command(label="See proteome statistics", font=("courier", 15), command=self.stats)
        menuBar.add_cascade(label="Statistics", font=("courier", 15), menu=menuStats)

        menuExit = Menu(menuBar, tearoff=0)
        menuExit.add_command(label="Exit", font=("courier", 15), command=self.quit)
        menuBar.add_cascade(label="Exit", font=("courier", 15), menu=menuExit)

        self.config(menu = menuBar) 

    def reset(self) :
        """ This function allows to make widget reset, exept the widget 
        of the menu bar.
        This function is particularly useful when user change tabs, 
        or also if user click on the tab again.
        """

        for widget in self.winfo_children() :
            if "listbox" in str(widget) :
                widget.destroy()
            if "button" in str(widget) :
                widget.destroy()
            if "label" in str(widget) :
                widget.destroy()
            if "entry" in str(widget) :
                widget.destroy()
            if "combobox" in str(widget) :
                widget.destroy()

    def proteomes_in_disk(self) :
        """ This function is called by the "Make_a_Tree" feature.
        It displays list of all proteomes that are available in the disk.

        Returns
        -------
        p_presents : TYPE list
            DESCRIPTION. list that contains all names of proteomes available 
                         in the disk.
        """

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
        """ This function is called when user have validate the proteomes 
        selection whose he wants to get a phylogenetic tree.

        Parameters
        ----------
        p_presents : TYPE list
            DESCRIPTION. list that contains all names of proteomes available 
                         in the disk.

        Returns
        -------
            DESCRIPTION. open a new window with the phylogenetic tree.
        """

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
            tkinter.messagebox.showinfo(title="Good things come to those who wait", message="BLAST and RBH job are finish. Please, wait that the full job is over.")
            clust = Clusterizer(bhitters, proteomes)
            clust.cluster_them()
            clust.one_align_to_rule_them_all()
            clust.draw_tree()

    def Search_Download_proteome(self) :
        """ This function is called by the "Download" feature.
        It asks user to write a few letters for search this pattern in the list 
        of all proteomes available in RefSeq database.

        Returns
        -------
        pattern : TYPE str
            DESCRIPTION. pattern that contains a few letters write by user.
        """

        self.reset()
        text = Label(text="Give me a few letters so i can search for you", font=("courier", 18))
        text.pack(pady=40)

        pattern = Entry(self, width=40, font=("courier", 16))
        pattern.pack()
        pattern.bind("<Return>", lambda x=None: self.Select_Download_proteome(pattern))
    
    def Select_Download_proteome(self, pattern) :
        """ This function is called when user presses enter on his keyboard.
        It display dropdown list of all proteomes, that contains pattern write 
        by user, available in RefSeq database.

        Parameters
        ----------
        pattern : TYPE str
            DESCRIPTION. pattern that contains a few letters write by user.

        Returns
        -------
        dropdown_list : TYPE list
            DESCRIPTION. list that contains all names of proteomes available in 
                         RefSeq database which contains pattern write by user.
        """

        pattern = pattern.get()

        library = RefSeqScraper()
        elements_with_pattern = library.data.loc[(library.data['readable'].str.contains(pattern)),'readable']
        list_elements = list(set(elements_with_pattern))
        list_elements = sorted(list_elements)

        dropdown_list = Combobox(self, values=list_elements, font=("courier", 16), width=50)
        dropdown_list.pack(pady=40)
        
        dropdown_list.bind("<<ComboboxSelected>>", lambda x=None: self.Download_proteome(dropdown_list))

    def Download_proteome(self, dropdown_list) :
        """ This function is called when user has chosen, therefore has selected, the proteome that he want download.
        It download the proteome, chosen by user, from RefSeq database to the disk.

        Parameters
        ----------
        dropdown_list : TYPE list
            DESCRIPTION. list that contains all names of proteomes available in 
                         RefSeq database which contains pattern write by user.
        """

        tkinter.messagebox.showinfo(title="Loading ...", message="Please, wait that the job is over.")
        name_proteome = dropdown_list.get()
        library = RefSeqScraper()
        library.add_to_cart(species=name_proteome)
        library.download_genome()
        unzip = "gzip -d ../data/genomes/"+name_proteome.replace(' ', '_')+"_protein.faa.gz"
        os.system(unzip)
        tkinter.messagebox.showinfo(title="It's Good ! :)", message="The download is over.")

    def distributions_of_evalues(self) :
        """ This function is called by the "E-values" feature.
        It displays list of all BLAST that are available in the disk.

        Returns
        -------
        blast_presents : TYPE list
            DESCRIPTION. list of BLAST available in the disk.
        """

        self.reset()
        blast_presents = Listbox(self, height=15, width=1100, bg='white', font=("courier", 15), selectbackground='pink')
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
        """ This function is called when user has selected the BLAST whose he want 
        see the distribution of e-values.
        It display a new window with a histogram of the distribution of e-value. 

        Parameters
        ----------
        blast_presents : TYPE list
            DESCRIPTION. list of BLAST available in the disk.

        Returns
        -------
            DESCRIPTION. open a new window with a histogram of the distribution 
                         of e-value of BLAST chosen by user.
        """

        blast_select = blast_presents.curselection()
        histo = blast_presents.get(blast_select)
        BlastHitter.evalue_dist(histo)
        title = "../data/figures/"+histo[:histo.find('_strain')]+histo[histo.find('_vs_'):histo.find('_strain', histo.find('_vs_'))]+".png"
        secondary_window = Tk()
        secondary_window.title("Histogramme")
        secondary_window.geometry('640x480')
        canvas = Canvas(secondary_window, width=640, height=480)
        img_histo = PhotoImage(master=canvas, file=title)
        canvas.create_image(0, 0, anchor=NW, image=img_histo)
        canvas.pack(expand=YES)
        secondary_window.mainloop()

    def stats(self) :
        """ This function is called by the "Statistics" feature.
        It displays list of all proteomes that are available in the disk.

        Returns
        -------
        prot_presents : TYPE list
            DESCRIPTION. list of all proteomes available in the disk.
        """
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
        """ This function is called when user has selected the proteome whose 
        he want see statistics that characterizes him.
        It display a new window with the statistics of proteome that user has 
        selected. 

        Parameters
        ----------
        prot_presents : TYPE list
            DESCRIPTION. list of all proteomes available in the disk.

        Returns
        -------
            DESCRIPTION. open a new window with statistics of proteome that 
                         user has chosen. 
        """

        prot_select = prot_presents.curselection()
        name_prot_select = "../data/genomes/"+prot_presents.get(prot_select)
        stats_prot = BlastHitter.seqkit_stat(name_prot_select)
        secondary_window = Tk()
        secondary_window.title("Statistics of the selected proteome")
        secondary_window.geometry('800x200')
        display_stats = Label(secondary_window, text=stats_prot, font=("courier", 15))
        display_stats.pack(pady=40)


if __name__ == '__main__':
    app = window()
    app.mainloop()
