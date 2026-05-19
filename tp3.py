import os
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
mu = 0.1
index = 0
trajectoire = []
balles = []
config_file_path = None
epsilon = 0.0001

fenetre = tk.Tk()
fenetre.title("Jeu de billard")

case_de_donnee = tk.Frame(fenetre)
case_de_donnee.pack(side='left', padx=10, pady=10, anchor='n')

canvas = tk.Canvas(fenetre, width=largeur, height=hauteur, bg="green")
canvas.pack(side='right', padx=10, pady=10)

def dessiner_table():
    canvas.config(width=largeur, height=hauteur)
    canvas.delete("bord")
    canvas.create_rectangle(0, 0, largeur, rayon, fill="brown", tags="bord")  # top
    canvas.create_rectangle(0, hauteur - rayon, largeur, hauteur, fill="brown", tags="bord")  # bottom
    canvas.create_rectangle(0, 0, rayon, hauteur, fill="brown", tags="bord")  # left
    canvas.create_rectangle(largeur - rayon, 0, largeur, hauteur, fill="brown", tags="bord")  # right
    if trajectoire:
        afficher_etat(index)

dessiner_table()

angle = tk.Label(case_de_donnee, text="Entrer l'angle de lancement")
angle.pack(anchor='w')
angle_entree = tk.Spinbox(case_de_donnee, from_=0, to=360, width=10, wrap=True)
angle_entree.insert(0, -30.0)
angle_entree.pack(anchor='w', fill='x')

vitesse = tk.Label(case_de_donnee, text="Entrer la vitesse initiale")
vitesse.pack(anchor='w', pady=(10,0))
vitesse_entree = tk.Spinbox(case_de_donnee, from_=0, to=500, width=10)
vitesse_entree.insert(0, 50.0) 
vitesse_entree.pack(anchor='w', fill='x')

bouton_charger_config = tk.Button(case_de_donnee, text="Charger configuration", command=lambda: charger_configuration())
bouton_charger_config.pack(anchor='center', pady=(10,0))

etat_config = tk.Label(case_de_donnee, text="Aucune configuration chargée", fg="red", wraplength=180, justify='left')
etat_config.pack(anchor='w', pady=(10,0))

def lire_fichier_config(chemin):
    if not chemin:
        raise FichierConfigIntrouvable("Aucun fichier de configuration sélectionné.")

    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        raise FichierConfigIntrouvable(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError as erreur:
        raise AnalyseConfigErreur(f"Le fichier JSON est mal formé : {erreur}")

    return valider_config(data)


def valider_config(data):
    if not isinstance(data, dict):
        raise AnalyseConfigErreur("Le contenu du fichier doit être un objet JSON.")

    def champ_required(nom):
        if nom not in data:
            raise ChampConfigManquant(f"Champ manquant : {nom}")
        return data[nom]

    largeur_cfg = champ_required("largeur")
    hauteur_cfg = champ_required("hauteur")
    mu_cfg = champ_required("mu")
    rayon_cfg = champ_required("rayon")
    balles_cfg = champ_required("balles")

    if not isinstance(largeur_cfg, (int, float)) or largeur_cfg <= 0:
        raise ValeurConfigInvalide("La largeur doit être un nombre positif.")
    if not isinstance(hauteur_cfg, (int, float)) or hauteur_cfg <= 0:
        raise ValeurConfigInvalide("La hauteur doit être un nombre positif.")
    if not isinstance(mu_cfg, (int, float)) or mu_cfg < 0 or mu_cfg > 1:
        raise ValeurConfigInvalide("Le coefficient de friction μ doit être entre 0 et 1.")
    if not isinstance(rayon_cfg, (int, float)) or rayon_cfg <= 0:
        raise ValeurConfigInvalide("Le rayon doit être un nombre positif.")
    if not isinstance(balles_cfg, list) or len(balles_cfg) == 0:
        raise ValeurConfigInvalide("La clé 'balles' doit être une liste non vide.")

    balles_valides = []
    for i, balle in enumerate(balles_cfg, start=1):
        if not isinstance(balle, dict):
            raise ValeurConfigInvalide(f"Chaque balle doit être un objet, erreur à l'index {i}.")

        position = None
        if "position" in balle:
            position = balle["position"]
        elif "position_initiale" in balle:
            position = balle["position_initiale"]
        else:
            raise ChampConfigManquant(f"Champ manquant pour la balle {i} : position ou position_initiale")

        if not isinstance(position, (list, tuple)) or len(position) != 2:
            raise ValeurConfigInvalide(f"La position de la balle {i} doit être une liste de deux nombres.")

        x, y = position
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValeurConfigInvalide(f"La position de la balle {i} doit contenir des nombres.")
        if x < rayon_cfg or x > largeur_cfg - rayon_cfg:
            raise ValeurConfigInvalide(f"La position x de la balle {i} doit être entre {rayon_cfg} et {largeur_cfg - rayon_cfg}.")
        if y < rayon_cfg or y > hauteur_cfg - rayon_cfg:
            raise ValeurConfigInvalide(f"La position y de la balle {i} doit être entre {rayon_cfg} et {hauteur_cfg - rayon_cfg}.")

        balles_valides.append({"position": [float(x), float(y)]})

    return {
        "largeur": int(largeur_cfg),
        "hauteur": int(hauteur_cfg),
        "mu": float(mu_cfg),
        "rayon": float(rayon_cfg),
        "balles": balles_valides,
    }


def appliquer_configuration(config, chemin):
    global largeur, hauteur, mu, rayon, balles, config_file_path, index, trajectoire
    largeur = config["largeur"]
    hauteur = config["hauteur"]
    mu = config["mu"]
    rayon = config["rayon"]
    balles = config["balles"]
    config_file_path = chemin
    index = 0
    trajectoire = []
    canvas.delete("balle")
    dessiner_table()
    etat_config.config(
        text=f"Config : {os.path.basename(chemin)} — {largeur}×{hauteur}, μ={mu}, rayon={rayon}, {len(balles)} balle(s)",
        fg="black",
    )


def charger_configuration():
    chemin = filedialog.askopenfilename(
        title="Choisir un fichier de configuration",
        filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*")],
    )
    if not chemin:
        return
    try:
        config = lire_fichier_config(chemin)
        appliquer_configuration(config, chemin)
    except ErreurConfiguration as erreur:
        messagebox.showerror("Erreur de configuration", str(erreur))
    except Exception as erreur:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue : {erreur}")


def lancer_simulation():
    global index, trajectoire
    if not balles:
        messagebox.showerror("Erreur de configuration", "Chargez d'abord un fichier de configuration valide.")
        return

    norme_v = float(vitesse_entree.get())
    theta_deg = np.deg2rad(float(angle_entree.get()))
    p = np.array(balles[0]["position"], dtype=float)
    v = norme_v * np.array([math.cos(theta_deg), -math.sin(theta_deg)])
    dt = 0.5
    index = 0
    trajectoire = []
    trajectoire.append(p.copy())
    dernier_point_affiche = p.copy()
    seuil_visibilite = 1.0  # en pixels
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
        if np.linalg.norm(p - dernier_point_affiche) >= seuil_visibilite:
            trajectoire.append(p.copy())
            dernier_point_affiche = p.copy()

    if not trajectoire or not np.allclose(trajectoire[-1], p):
        trajectoire.append(p.copy())

    index = 0
    afficher_etat(index)

def afficher_etat(i):
    if not trajectoire:
        return
    p = trajectoire[i]
    x, y = p
    canvas.delete("balle")
    canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, fill="white", tags="balle")

def pas_suivant():
    global index
    if not trajectoire or index >= len(trajectoire) - 1:
        return
    index += 1
    afficher_etat(index)

def pas_precedent():
    global index
    if not trajectoire or index <= 0:
        return
    index -= 1
    afficher_etat(index)

def position_finale():
    global index
    if not trajectoire:
        return
    index = len(trajectoire) - 1
    afficher_etat(index)

def reinitialiser():
    global index
    if not trajectoire:
        return
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

fenetre.mainloop()

