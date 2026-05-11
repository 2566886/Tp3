import tkinter as tk
import numpy as np
import math
import json
from tkinter import filedialog, messagebox

class ErreurConfiguration(Exception):
    pass


class FichierConfigIntrouvable(ErreurConfiguration):
    pass


class AnalyseConfigErreur(ErreurConfiguration):
    pass


class ValidationConfigErreur(ErreurConfiguration):
    pass


class ChampConfigManquant(ValidationConfigErreur):
    pass


class ValeurConfigInvalide(ValidationConfigErreur):
    pass


rayon = 10
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
canvas.create_rectangle(0, 0, largeur, rayon, fill="brown")  # top
canvas.create_rectangle(0, hauteur - rayon, largeur, hauteur, fill="brown")  # bottom
canvas.create_rectangle(0, 0, rayon, hauteur, fill="brown")  # left
canvas.create_rectangle(largeur - rayon, 0, largeur, hauteur, fill="brown")  # right

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
friction_entree.insert(0, 0.1)
friction_entree.pack(anchor='w', fill='x')

def lancer_simulation():
    global index, trajectoire
    norme_v = float(vitesse_entree.get())
    theta_deg = np.deg2rad(float(angle_entree.get()))
    mu = float(friction_entree.get())

    p = np.array([rayon, rayon], dtype=float)
    v = norme_v * np.array([math.cos(theta_deg), -math.sin(theta_deg)])
    dt = 5.0
    index = 0
    trajectoire = []
    trajectoire.append(p.copy())

    while np.linalg.norm(v) > epsilon:
        v = v * (1 - mu * dt)
        new_p = p + v * dt
        
        # Check left border
        if new_p[0] <= rayon:
            new_p[0] = rayon
            n = np.array([1.0, 0.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check right border
        if new_p[0] >= largeur - rayon:
            new_p[0] = largeur - rayon
            n = np.array([-1.0, 0.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check top border
        if new_p[1] <= rayon:
            new_p[1] = rayon
            n = np.array([0.0, 1.0])
            v = v - 2 * np.dot(v, n) * n
        
        # Check bottom border
        if new_p[1] >= hauteur - rayon:
            new_p[1] = hauteur - rayon
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
    canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, fill="white", tags="balle")

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

# def _charger_config() -> None:
#     chemin = filedialog.askopenfilename(
#         title="Choisir le fichier de configuration",
#         filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*")],
#     )
#     if not chemin:
#         return

#     try:
#         config = _lire_config(chemin)
#     except ErreurConfiguration as err:
#         messagebox.showerror("Erreur de configuration", str(err))
#         config = None
#         config_label.config(text="Aucun fichier chargé.")
#         lancer_button.config(state=tk.DISABLED)
#         return
        
# def _valider_config(config: dict) -> None:
#     if not isinstance(config, dict):
#         raise ValidationConfigErreur("La configuration doit être un objet JSON.")

#     required = ["surface", "friction", "rayon_balle", "balles"]
#     for champ in required:
#         if champ not in config:
#             raise ChampConfigManquant(f"Champ manquant : {champ}")

#     surface = config["surface"]
#     if not isinstance(surface, dict):
#         raise ValeurConfigInvalide("'surface' doit être un objet avec largeur et hauteur.")

#     largeur_surface = surface.get("largeur")
#     hauteur_surface = surface.get("hauteur")
#     if not (isinstance(largeur_surface, (int, float)) and largeur_surface > 0):
#         raise ValeurConfigInvalide("'surface.largeur' doit être un nombre positif.")
#     if not (isinstance(hauteur_surface, (int, float)) and hauteur_surface > 0):
#         raise ValeurConfigInvalide("'surface.hauteur' doit être un nombre positif.")

#     friction = config["friction"]
#     if not (isinstance(friction, (int, float)) and 0 <= friction <= 1):
#         raise ValeurConfigInvalide("'friction' doit être un nombre entre 0 et 1.")

#     rayon = config["rayon_balle"]
#     if not (isinstance(rayon, (int, float)) and rayon > 0):
#         raise ValeurConfigInvalide("'rayon_balle' doit être un nombre positif.")

#     balles = config["balles"]
#     if not isinstance(balles, list) or len(balles) == 0:
#         raise ValeurConfigInvalide("'balles' doit être une liste non vide.")

#     for index, balle in enumerate(balles, start=1):
#         if not isinstance(balle, dict):
#             raise ValeurConfigInvalide(f"Chaque balle doit être un objet JSON (balle #{index}).")

#         position = balle.get("position")
#         if not (
#             isinstance(position, list)
#             and len(position) == 2
#             and all(isinstance(coord, (int, float)) for coord in position)
#         ):
#             raise ValeurConfigInvalide(f"La position de la balle #{index} doit être une liste de deux nombres.")

#         x, y = position
#         if not (rayon <= x <= largeur_surface - rayon and rayon <= y <= hauteur_surface - rayon):
#             raise ValeurConfigInvalide(
#                 f"La position de la balle #{index} doit être à l’intérieur de la zone valide.")

#         if "angle" in balle and not isinstance(balle["angle"], (int, float)):
#             raise ValeurConfigInvalide(f"L'angle de la balle #{index} doit être un nombre.")
#         if "vitesse" in balle and not (isinstance(balle["vitesse"], (int, float)) and balle["vitesse"] >= 0):
#             raise ValeurConfigInvalide(f"La vitesse de la balle #{index} doit être un nombre positif.")


# config_label.config(text=f"Config chargée : {chemin}")

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

canvas.create_oval(rayon - rayon, rayon - rayon, rayon + rayon, rayon + rayon, fill="white", tags="balle")

fenetre.mainloop()

