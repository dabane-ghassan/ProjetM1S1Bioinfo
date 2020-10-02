# ProjetM1S1Bioinfo

![Logo](photos/logo.png)

***Master Bioinformatique : Développement de logiciels et Analyse de données - Projet dans le cadre de l'UE : Introduction à l'informatique et à la programmation***


Le but de ce projet est de concevoir une application Python. Cette application se décompose en plusieurs modules pour permettre soit un développement linéaire/principal, soit des développements parallèles « à la carte » (par exemple si vous bloquez - ou avez fini - le linéaire). Vous serez notés d’une part sur l’aspect fonctionnel de ce code, donc inutile d’attaquer le module suivant si le précédent n’est pas entièrement fonctionnel. L’autre partie de la note sera liée à la propreté de votre code, dont quelques éléments (de bon sens) sont listés à la fin de ce document.
Le projet peut être réalisé en binôme, mais ce n’est pas une obligation. Dans ce cas, le détail de la répartition des tâches devra être clair et présenté à la soutenance.
Description de l’application
> 1.	Ecrire un programme qui :
a.	lance une recherche BLAST d’un génome requête contre un autre génome cible (paramètres)
b.	lit le fichier résultat afin d’en récupérer la liste des meilleurs hits pour chaque protéine
c.	lance la recherche BLAST réciproque afin d’en déduire la liste des hits bidirectionnels.
Etape optionnelle/parallèle : écrire un programme qui interroge une source de génomes sur le web pour en proposer la liste/le choix à l’utilisateur, et les télécharger alors sur le disque.

> 2.	Ecrire un programme qui lancera le programme précédent pour un ensemble de génomes (>2), afin de les comparer tous les uns aux autres. Le programme regroupera les protéines ayant un hit bidirectionnel commun à travers ces différent génomes en clusters d’orthologues.
Etape optionnelle/parallèle 1 : développer une interface graphique pour sélectionner les génomes parmi ceux présent sur le disque et lancer le programme via cette interface. Une interface graphique de l’étape optionelle précédente peut être aussi envisagée.
Etape optionnelle/parallèle 2 : Créer une base de données composée de trois tables [GENOMES(id, name), PROTEIN(id, genome_id, cluster_id), BLAST(prot1_id, prot2_id, e-value, coverage] pour stocker les données générées.
Etape optionnelle/parallèle 3 : Proposer une interface permettant de visualiser la distribution des e-valeurs à l’intérieur d’un cluster.

> 3.	Ecrire un programme qui :
a.	sélectionne les clusters n’ayant pas plus d’une protéine par organisme
b.	génère un alignement multiple de chaque cluster
c.	concatène les différents alignement en un super-alignement
d.	lance la phylogénie des espèces à partir du super-alignement
Etape optionnelle/parallèle 1 : proposer une visualisation/analyse des clusters pour ne sélectionner qu’une protéine par organisme (si plusieurs dans le cluster). Proposer un moyen de stocker cette information (sur le disque ou la base de données si créée à l’étape précédente). Inclure ces clusters additionnels dans la procédure (étapes b à d).
Etape optionnelle/parallèle 2 : En supposant présentes sur le disque local les séquences ADN qui encodent ces protéines, écrire un programme pour générer le super-alignement nucléotidique correspondant.

*Bonnes pratiques en programmation
Voici une liste non-exhaustive d’éléments sur lesquels nous portera notre attention :
- Prohibition de la langue de Molière
-	Factorisation du code par des fonctions
-	Utilisation de structures de données adaptées
-	Dose et forme (Docstring) judicieuses des commentaires du code
-	Pertinence du nommage des variables, fonctions, fichiers, classes, etc.*

