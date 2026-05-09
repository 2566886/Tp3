import numpy as np

p_min = np.array([r, r])
p_max = np.array([largeur - r, hauteur - r])

# La balle touche un bord si :
np.any(p <= p_min) or np.any(p >= p_max)