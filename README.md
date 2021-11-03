# PoulPyX

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e752d3704414b51879e738734395413)](https://app.codacy.com/gh/cpasquier/poulpyx?utm_source=github.com&utm_medium=referral&utm_content=cpasquier/poulpyx&utm_campaign=Badge_Grade_Settings)

PoulPyX est un petit générateur de script pour le SAXS, utilisant l'interface tkinter (https://docs.python.org/fr/3/library/tkinter.html).
Il permet, à partir d'un fichier lineup, d'enregistrer les valeurs de x et de transmission à différents points choisis sur le scan de transmission. En ajoutant ensuite les paramètres de mesure voulus (position en z, temps de mesure, nom, nature de l'échantillon...), il génère directement le script de lancement des mesures, ainsi que plusieurs fichiers récapitulant les informations de chaque échantillon.
