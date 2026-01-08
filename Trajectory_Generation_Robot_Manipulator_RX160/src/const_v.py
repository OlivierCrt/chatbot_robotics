import numpy as np

# Parametres de Denavit Hartenberg modifié
dh = {}
dh["sigma_i"] = [0, 0, 0, 0]
dh["a_i_m1"] = [0, 150, 825, 735]
dh["alpha_i_m1"] = [0, np.pi / 2, 0, 0]
dh["r_i"] = [550, 0, 0, 0]

# Parametres de l'arrondi
decimals = 2
threshold = 1e-7
round_p = (decimals, threshold)

# Pour modélisation 3D du bras robot

"""Dans les listes on a les parametres horizontaux (X), verticaux (Z) et de profondeur (Y), dans cette ordre"""
Liaisons = [
    [150, 550, 0],  # Liaison 1
    [0, 825, 352],  # Liaison 2
    [0, 735, 352],  # Liaison 3
]
