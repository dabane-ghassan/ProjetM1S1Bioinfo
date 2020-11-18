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

## Dependencies
If you're on Ubuntu/Debian, please run blast_setup.py in order to install ncbi-blast+ : 
```console
python3 blast_setup.py
```

## Ressources (05/10/2020) :
[BLAST® Command Line Applications User Manual](https://www.ncbi.nlm.nih.gov/books/NBK279690/) <br>
[Téléchargement Blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) <br>

