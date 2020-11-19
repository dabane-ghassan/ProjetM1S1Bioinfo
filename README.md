# ProjetM1S1Bioinfo

![Logo](data/photos/logo.png)

***Master Bioinformatique : Développement de logiciels et Analyse de données - Projet dans le cadre de l'UE : Introduction à l'informatique et à la programmation***

## GUIless Demo 
- Let's import our two classes : 
```python
from blast_hitter import BlastHitter
from clusterizer import Clusterizer
```
- Proteomes can be downloaded with RefSeqScraper script, or manually saved to data/genomes repository.
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

- Now let's create a Clusterizer object after populating our blasthitters with RBH files :

```python
clust = Clusterizer(bhitters, proteomes)
```
- The next and final step would be to create clusters, aligning each one and concatenating all of them and last but not least would be to launch the phylogenetic algorithm and to draw the newick tree: 
```python
clust.cluster_them()
clust.one_align_to_rule_them_all()
clust.draw_tree()
```

## Ressources (05/10/2020) :
[BLAST® Command Line Applications User Manual](https://www.ncbi.nlm.nih.gov/books/NBK279690/) <br>
[Téléchargement Blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) <br>

