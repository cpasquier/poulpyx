# PoulPyX

PoulPyX est un petit générateur de script pour le SAXS, utilisant l'interface tkinter (https://docs.python.org/fr/3/library/tkinter.html).
Il permet, à partir d'un fichier lineup, d'enregistrer les valeurs de x et de transmission à différents points choisis sur le scan de transmission. En ajoutant ensuite les paramètres de mesure voulus (position en z, temps de mesure, nom, nature de l'échantillon...), il génère directement le script de lancement des mesures, ainsi que plusieurs fichiers récapitulant les informations de chaque échantillon.

Le script Lupo-PoulPyX permet de calculer directement le facteur de normalisation pour la mise en valeur absolue des spectres, a partir du spectre du Lupo et du fichier lupo.txt genere au prealable par PoulPyX.
