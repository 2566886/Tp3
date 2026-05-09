import tkinter as tk
from simulation_numérique_discrète import creer_simulation, etape_simulation

fenetre = tk.Tk()
fenetre.title("Jeu de billard")

case_donnee = tk.Frame(fenetre)
case_donnee.pack(side='left', padx=10, pady=10, anchor='n')

canvas = tk.Canvas(fenetre, width=400, height=300, bg="green")
canvas.pack(side='right', padx=10, pady=10)

angle = tk.Label(case_donnee, text="Entrer l'angle de lancement")
angle.pack(anchor='w')
angle_entree = tk.Spinbox(case_donnee, from_=0, to=360, width=10, wrap=True)
angle_entree.insert(0, 0)
angle_entree.pack(anchor='w', fill='x')

vitesse = tk.Label(case_donnee, text="Entrer la vitesse initiale")
vitesse.pack(anchor='w', pady=(10,0))
vitesse_entree = tk.Spinbox(case_donnee, from_=0, to=100, width=10)
vitesse_entree.insert(0, 0) 
vitesse_entree.pack(anchor='w', fill='x')

lancer = tk.Button(case_donnee, text="Lancer")
lancer.pack(anchor='w', pady=(10,0))

fenetre.mainloop()

