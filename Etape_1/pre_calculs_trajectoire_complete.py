import tkinter as tk
import numpy as np
import math

p = np.array([0, 0])
norme_v = float(input("Inserez la norme de la vitesse = "))     
theta_deg = float(input("Inserez l'angle de la vitesse (en degres) = "))  
v = norme_v * np.array([math.cos(theta_deg), -math.sin(theta_deg)])
dt = 0.2
r = int(input("Inserez le rayon de la balle = "))
largeur = int(input("Inserez la largeur de la fenetre = "))
hauteur = int(input("Inserez la hauteur de la fenetre = "))
p_min = np.array([r, r])
p_max = np.array([largeur - r, hauteur - r])

# La balle touche un bord si :
np.any(p <= p_min) or np.any(p >= p_max)
while v != np.array([0, 0]):
    p = p + v * dt
    if np.any(p <= p_min) or np.any(p >= p_max):
        v = 0

