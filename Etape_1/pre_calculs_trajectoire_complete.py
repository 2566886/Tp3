import tkinter as tk
import numpy as np
import math

r = 10
largeur = 1000
hauteur = 750
index = 0
trajectoire = []

fenetre = tk.Tk()
fenetre.title("Jeu de billard")

case_de_donnee = tk.Frame(fenetre)
case_de_donnee.pack(side='left', padx=10, pady=10, anchor='n')

canvas = tk.Canvas(fenetre, width=1000, height=750, bg="green")
canvas.pack(side='right', padx=10, pady=10)

angle = tk.Label(case_de_donnee, text="Entrer l'angle de lancement")
angle.pack(anchor='w')
angle_entree = tk.Spinbox(case_de_donnee, from_=0, to=360, width=10, wrap=True)
angle_entree.insert(0, 30.0)
angle_entree.pack(anchor='w', fill='x')

vitesse = tk.Label(case_de_donnee, text="Entrer la vitesse initiale")
vitesse.pack(anchor='w', pady=(10,0))
vitesse_entree = tk.Spinbox(case_de_donnee, from_=0, to=500, width=10)
vitesse_entree.insert(0, 2.0) 
vitesse_entree.pack(anchor='w', fill='x')

def lancer_simulation():
    global index, trajectoire
    norme_v = float(vitesse_entree.get())
    theta_deg = np.deg2rad(float(angle_entree.get()))

    p = np.array([r, r], dtype=float)
    v = norme_v * np.array([math.cos(theta_deg), -1 * math.sin(theta_deg)])

    dt = 0.2
    p_min = np.array([r, r])
    p_max = np.array([largeur - r, hauteur - r])
    index = 0
    trajectoire = []
    trajectoire.append(p.copy())

    while not (np.any(p < p_min) or np.any(p > p_max)):
        p = p + v * dt
        trajectoire.append(p.copy())
    afficher_etat(0)

def afficher_etat(i):
    p = trajectoire[i]
    x, y = p
    canvas.delete("balle")
    canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", tags="balle")

def pas_suivant():
    global index
    if index >= len(trajectoire) -1:
        return 
    index += 1
    afficher_etat(index)

def pas_precedent():
    global index
    if index <= 0:
        return
    index -= 1
    afficher_etat(index)

def position_finale():
    global index
    index = len(trajectoire) - 1
    afficher_etat(index)

def reinitialiser():
    global index
    index = 0
    afficher_etat(index)

lancer = tk.Button(case_de_donnee, text="Lancer", command=lancer_simulation)
lancer.pack(anchor='center', pady=(10,0))

bouton_suivant = tk.Button(case_de_donnee, text="Pas suivant", command=pas_suivant)
bouton_suivant.pack(anchor='center', pady=(10,0))

bouton_precedent = tk.Button(case_de_donnee, text="Pas précédent", command=pas_precedent)
bouton_precedent.pack(anchor='center', pady=(10,0))

bouton_position_finale = tk.Button(case_de_donnee, text="Position finale", command=position_finale)
bouton_position_finale.pack(anchor='center', pady=(10,0))

bouton_reinitialiser = tk.Button(case_de_donnee, text="Réinitialiser", command=reinitialiser)
bouton_reinitialiser.pack(anchor='center', pady=(10,0))

canvas.create_oval(r - r, r - r, r + r, r + r, fill="white", tags="balle")

fenetre.mainloop()

