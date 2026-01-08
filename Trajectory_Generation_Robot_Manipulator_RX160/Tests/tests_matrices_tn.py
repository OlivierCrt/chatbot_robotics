import numpy as np
from src.matrice_tn import *
from src.const_v import *


# Angles pour les tests
q_test = [np.pi, np.pi/2, 0]

#On active le debugage des fctns testés
Debug = True

# Position cible pour MGI
Xd_test = [300, 200, 600]  # Position cible réalisable par le robot


# Tests de chaque fonction
def test_matrice_Tim1_Ti():
    print("Test : matrice_Tim1_Ti")
    T = matrice_Tim1_Ti(0, dh["a_i_m1"][3], dh["alpha_i_m1"][3], dh["r_i"][3],Debug=Debug)
    assert T.shape == (4, 4), "La matrice retournée n'est pas de taille 4x4"
    print("Résultat : OK\n")

def test_generate_transformation_matrices():
    print("Test : generate_transformation_matrices")
    T_matrices = generate_transformation_matrices(q_test, dh, round_p=(2, 1e-6),Debug=Debug)
    assert len(T_matrices) == len(q_test) + 1, "Le nombre de matrices ne correspond pas au nombre de liaisons"
    for T in T_matrices:
        assert T.shape == (4, 4), "Une des matrices n'est pas de taille 4x4"
    print("Résultat : OK\n")

def test_matrice_Tn():
    print("Test : matrice_Tn")
    Tn = matrice_Tn(dh, q_test,Debug=Debug)
    assert Tn.shape == (4, 4), "La matrice T0,n n'est pas de taille 4x4"
    print("Résultat : OK\n")

def test_xy_Ot():
    print("Test : xy_Ot")
    Tn = matrice_Tn(dh, q_test,Debug=Debug)
    xyz = xy_Ot(Tn)
    assert len(xyz) == 3, "Les coordonnées extraites ne sont pas de taille 3"
    print("Résultat : OK\n")

def test_mgd():
    print("Test : mgd")
    Xd = mgd(q_test, Liaisons,Debug=Debug)
    assert len(Xd) == 3, "Les coordonnées retournées par le MGD ne sont pas de taille 3"
    print("Résultat : OK\n")

def test_mgi():
    print("Test : mgi")
    solutions = mgi(Xd_test, Liaisons,Debug=Debug)
    assert isinstance(solutions, list), "Le MGI ne retourne pas une liste"
    assert all(len(sol) == 3 for sol in solutions), "Une solution ne contient pas 3 angles"
    print(f'Solutions MGI = {solutions}')
    print("Résultat : OK\n")

def test_verifier_solutions():
    print("Test : verifier_solutions")
    verifier_solutions(Xd_test, Liaisons)
    print("Résultat : Vérification effectuée\n")

# Exécution des tests
if __name__ == "__main__":
    print("Lancement des tests...\n")
    test_matrice_Tim1_Ti()
    test_generate_transformation_matrices()
    test_matrice_Tn()
    test_xy_Ot()
    test_mgd()
    test_mgi()
    test_verifier_solutions()
    print("Tous les tests ont été passés avec succès.")
