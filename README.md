# ProjetM1S1Bioinfo

![Logo](data/photos/logo.png)

***Master Bioinformatique : Développement de logiciels et Analyse de données - Projet dans le cadre de l'UE : Introduction à l'informatique et à la programmation***

## GUIless Demo 
- Let's import our two classes : 
```python
from blast_hitter import BlastHitter
from clusterizer import Clusterizer
```
- Proteomes can be downloaded with RefSeqScraper script, or manually savec to data/genomes repository.
A list of all paths should be initalised, so that we can use BlastHitter's factory method to create a bunch of blasthitter objects of all possible permutations.
```python
proteomes = ["../data/genomes/Rickettsia_rickettsii_str._Arizona_strain=Arizona_protein.faa",            
"../data/genomes/Streptococcus_pneumoniae_R6_strain=R6_protein.faa",
"../data/genomes/Streptococcus_pyogenes_strain=NCTC8232_protein.faa",
"../data/genomes/Streptococcus_thermophilus_LMD-9_strain=LMD-9_protein.faa",
"../data/genomes/Piscirickettsia_salmonis_strain=Psal-158_protein.faa"]

bhitters = BlastHitter.from_list(proteomes)
```
- We can blast them and accumulate the reciprocal best hits with a for loop : 
```python
for bh in bhitters  : 
    bh.blast_them()
    bh.rbh_them()
```

```python
clust = Clusterizer(bhitters, proteomes)
```

```python
clust.cluster_them()
clust.one_align_to_rule_them_all()
clust.draw_tree()
```

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

*Etape optionnelle/parallèle 3 : Proposer un graphique permettant de visualiser par exemple la distribution des e-valeurs à l’intérieur d’un cluster ou génome.*<br>

### Troisième programme
Ecrire un programme qui : <br>
1.	sélectionne les clusters n’ayant pas plus d’une protéine par organisme<br>
2.	génère un alignement multiple de chaque cluster<br>
3.	concatène les différents alignement en un super-alignement<br>
4.	lance la phylogénie des espèces à partir du super-alignement<br>

*Etape optionnelle/parallèle 1 : proposer une visualisation/analyse des clusters pour ne sélectionner qu’une protéine par organisme (si plusieurs dans le cluster). Proposer un moyen de stocker cette information (sur le disque ou la base de données si créée à l’étape précédente). Inclure ces clusters additionnels dans la procédure (étapes b à d).*<br>

*Etape optionnelle/parallèle 2 : en supposant présentes sur le disque local les séquences ADN qui encodent ces protéines, écrire un programme pour générer le super-alignement nucléotidique correspondant.*<br>

*Etape optionnelle/parallèle 3 : utiliser une librairie Python pour dessiner l’arbre phylogénétique résultat.* <br>

## Dependencies
If you're on Ubuntu/Debian, please run blast_setup.py in order to install ncbi-blast+ : 
```console
python3 blast_setup.py
```

## Ressources (05/10/2020) :
[BLAST® Command Line Applications User Manual](https://www.ncbi.nlm.nih.gov/books/NBK279690/) <br>
[Téléchargement Blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) <br>

