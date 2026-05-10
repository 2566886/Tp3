import tkinter as tk
import numpy as np
import math

r = 10
largeur = 1000
hauteur = 625
index = 0
trajectoire = []
epsilon = 0.1

fenetre = tk.Tk()
fenetre.title("Jeu de billard")

case_de_donnee = tk.Frame(fenetre)
case_de_donnee.pack(side='left', padx=10, pady=10, anchor='n')

canvas = tk.Canvas(fenetre, width=1000, height=625, bg="green")
canvas.pack(side='right', padx=10, pady=10)

# Draw bands
canvas.create_rectangle(0, 0, largeur, r, fill="brown")  # top
canvas.create_rectangle(0, hauteur - r, largeur, hauteur, fill="brown")  # bottom
canvas.create_rectangle(0, 0, r, hauteur, fill="brown")  # left
canvas.create_rectangle(largeur - r, 0, largeur, hauteur, fill="brown")  # right

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

friction = tk.Label(case_de_donnee, text="Entrer le coefficient de friction μ")
friction.pack(anchor='w', pady=(10,0))
friction_entree = tk.Spinbox(case_de_donnee, from_=0, to=1, increment=0.01, width=10)
friction_entree.insert(0, 0.01)
friction_entree.pack(anchor='w', fill='x')

def lancer_simulation():
    global index, trajectoire
    norme_v = float(vitesse_entree.get())
    theta_deg = np.deg2rad(float(angle_entree.get()))
    mu = float(friction_entree.get())

    p = np.array([r, r], dtype=float)
    v = norme_v * np.array([math.cos(theta_deg), -math.sin(theta_deg)])
    dt = 5.0
    index = 0
    trajectoire = []
    trajectoire.append(p.copy())

    while np.linalg.norm(v) > epsilon:
        v = v * (1 - mu * dt)
        new_p = p + v * dt
        
        # Check left border
        if new_p[0] <= r:
            new_p[0] = r
            n = np.array([1.0, 0.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check right border
        if new_p[0] >= largeur - r:
            new_p[0] = largeur - r
            n = np.array([-1.0, 0.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check top border
        if new_p[1] <= r:
            new_p[1] = r
            n = np.array([0.0, 1.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check bottom border
        if new_p[1] >= hauteur - r:
            new_p[1] = hauteur - r
            n = np.array([0.0, -1.0])
            v = v - 2 * np.dot(v, n) * n
        
        p = new_p
        trajectoire.append(p.copy())
    index = len(trajectoire) - 1
    afficher_etat(index)

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

