#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector

mydb = mysql.connector.connect(
    host="martinnas.myds.me",
    port=3307,
    user="ProjetM1DLAD",
    password="p@M_@G_#2020",
    database="Projet_M1_DLAD"
    )

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE IF NOT EXISTS GENOMES (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)) 
    ENGINE=INNODB;""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS PROTEIN (
    id INT NOT NULL,
    genome_id INT NOT NULL,
    cluster_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (genome_id) REFERENCES GENOMES(id) ON UPDATE CASCADE ON DELETE RESTRICT)
    ENGINE=INNODB;""")

mycursor.execute(""" CREATE TABLE IF NOT EXISTS BLAST (
    prot1_id INT NOT NULL,
    prot2_id INT NOT NULL,
    e_value FLOAT NOT NULL,
    coverage INT NOT NULL,
    FOREIGN KEY (prot1_id) REFERENCES PROTEIN(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (prot2_id) REFERENCES PROTEIN(id) ON UPDATE CASCADE ON DELETE RESTRICT)
    ENGINE=INNODB;""")