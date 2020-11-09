# ProjetM1S1Bioinfo

![Logo](data/photos/logo.png)

***Master Bioinformatique : Développement de logiciels et Analyse de données - Projet dans le cadre de l'UE : Introduction à l'informatique et à la programmation***

## Description de l’application

### Premier programme

Ecrire un programme qui : <br>
1.	lance une recherche BLAST d’un génome requête contre un autre génome cible (paramètres)<br>
2.	lit le fichier résultat afin d’en récupérer la liste des meilleurs hits pour chaque protéine.<br>
3.	lance la recherche BLAST réciproque afin d’en déduire la liste des hits bidirectionnels.<br>

*Etape optionnelle/parallèle : écrire un programme qui interroge une source de génomes sur le web pour en proposer la liste/le choix à l’utilisateur, et les télécharger alors sur le disque.*

### Deuxième programme
Ecrire un programme qui lancera le programme précédent pour un ensemble de génomes (>2), afin de les comparer tous les uns aux autres.<br>
Le programme regroupera les protéines ayant un hit bidirectionnel commun à travers ces différent génomes en clusters d’orthologues.<br>

*Etape optionnelle/parallèle 1 : développer une interface graphique pour sélectionner les génomes parmi ceux présent sur le disque et lancer le programme via cette interface. Une interface graphique de l’étape optionelle précédente peut être aussi envisagée.* <br>

*Etape optionnelle/parallèle 2 : Créer une base de données composée de trois tables [GENOMES(id, name), PROTEIN(id, genome_id, cluster_id), BLAST(prot1_id, prot2_id, e-value, coverage] pour stocker les données générées.*<br>

*Etape optionnelle/parallèle 3 : Proposer une interface permettant de visualiser la distribution des e-valeurs à l’intérieur d’un cluster.*<br>

### Troisième programme
Ecrire un programme qui : <br>
1.	sélectionne les clusters n’ayant pas plus d’une protéine par organisme<br>
2.	génère un alignement multiple de chaque cluster<br>
3.	concatène les différents alignement en un super-alignement<br>
4.	lance la phylogénie des espèces à partir du super-alignement<br>

*Etape optionnelle/parallèle 1 : proposer une visualisation/analyse des clusters pour ne sélectionner qu’une protéine par organisme (si plusieurs dans le cluster).<br>
Proposer un moyen de stocker cette information (sur le disque ou la base de données si créée à l’étape précédente).<br>
Inclure ces clusters additionnels dans la procédure (étapes b à d).*<br>
*Etape optionnelle/parallèle 2 : En supposant présentes sur le disque local les séquences ADN qui encodent ces protéines, écrire un programme pour générer le super-alignement nucléotidique correspondant.*<br>


### Bonnes pratiques en programmation : 
Voici une liste non-exhaustive d’éléments sur lesquels nous portera notre attention : <br>
- Prohibition de la langue de Molière<br>
-	Factorisation du code par des fonctions<br>
-	Utilisation de structures de données adaptées<br>
-	Dose et forme (Docstring) judicieuses des commentaires du code<br>
-	Pertinence du nommage des variables, fonctions, fichiers, classes, etc.<br>

## Dependencies
If you're on Ubuntu/Debian, please run blast_setup.py in order to install ncbi-blast+ : 
```console
python3 blast_setup.py
```

## Ressources (05/10/2020) :
[BLAST® Command Line Applications User Manual](https://www.ncbi.nlm.nih.gov/books/NBK279690/) <br>
[Téléchargement Blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) <br>

