import numpy as np


r = float(input("Entrez le rayon de la balle : "))
largeur = float(input("Entrez la largeur de la fenêtre : "))
hauteur = float(input("Entrez la hauteur de la fenêtre : "))

p_min = np.array([r, r])
p_max = np.array([largeur - r, hauteur - r])

# La balle touche un bord si :
collision = np.any(p <= p_min) or np.any(p >= p_max)