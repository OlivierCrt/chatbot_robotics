import numpy as np
from src.modele_differentiel import *
from src.matrice_tn import *
from src.const_v import dh, Liaisons

# Activer les modes de débogage
Debug = True

# Angles articulaires pour les tests
# Angles pour les tests
q_test = [np.pi, np.pi/2, np.pi/2]

# Position cible pour MGI
Xd_test = [300, 200, 600]

def test_calculate_z_and_o():
    print("Test : calculate_z_and_o")
    T = matrice_Tim1_Ti(q_test[0], dh["a_i_m1"][0], dh["alpha_i_m1"][0], dh["r_i"][0])
    z, o = calculate_z_and_o(T)
    assert z.shape == (3,), "Le vecteur z n'est pas de taille 3"
    assert o.shape == (3,), "Le vecteur o n'est pas de taille 3"
    print("Résultat : OK\n")

def test_Jacob_geo():
    print("Test : Jacob_geo")
    matrices = generate_transformation_matrices(q_test, dh, round_p=(3, 1e-6))
    J = Jacob_geo(matrices)
    assert J.shape == (6, len(q_test)), "La Jacobienne géométrique n'est pas de taille 6x3"
    print("Jacobienne géométrique calculée :\n", J)
    print("Résultat : OK\n")

def test_Jacob_analytique():
    print("Test : Jacob_analytique")
    J = Jacob_analytique()
    assert J.shape == (6, len(q_test)), "La Jacobienne analytique n'est pas de taille 6x3"
    print("Jacobienne analytique calculée :\n", J)
    print("Résultat : OK\n")

def test_MDD():
    print("Test : MDD")
    matrices = generate_transformation_matrices(q_test, dh)
    J = Jacob_geo(matrices)
    velocities = MDD([0.1, 0.2, 0.3], J)
    assert len(velocities) == 6, "Les vitesses OT ne sont pas de taille 6"
    print("Vitesses OT calculées :", velocities)
    print("Résultat : OK\n")

def test_MDI():
    print("Test : MDI")
    matrices = generate_transformation_matrices(q_test, dh)
    J = Jacob_geo(matrices)
    q_dot = MDI([0.5, 0.3, -0.2, 0.1, 0.0, -0.1], J)
    assert len(q_dot) == len(q_test), "Les vitesses articulaires ne sont pas de taille 3"
    print("Vitesses articulaires calculées :", q_dot)
    print("Résultat : OK\n")


def test_jacobienne_geo_vs_analytique():
    print("Test : Cohérence entre Jacobiennes géométrique et analytique")
    matrices = generate_transformation_matrices(q_test, dh)

    # Calcul des Jacobiennes
    J_geo = Jacob_geo(matrices)
    J_analytique_num = Jacob_analytique(q_test)

    # Comparaison entre Jacobienne géométrique et analytique numérique
    print("Jacobienne géométrique (numérique) :\n", J_geo)
    print("Jacobienne analytique (numérique) :\n", J_analytique_num)

    # Comparaison des termes individuels
    for i in range(6):
        for j in range(3):
            print(f"Différence J[{i}, {j}]: Géométrique = {J_geo[i, j]}, Analytique = {J_analytique_num[i, j]}, "
                  f"Diff = {J_geo[i, j] - J_analytique_num[i, j]}")

    assert np.allclose(J_geo, J_analytique_num, atol=1e-6), \
        "Les Jacobiennes géométrique et analytique ne correspondent pas"
    print("Résultat : OK\n")


def test_MDD():
    """
    Test de la fonction MDD (Vérification des vitesses OT calculées).
    """
    print("Test : MDD")
    # Définir une jacobienne J (exemple simple)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Définir des vitesses articulaires v
    v = np.array([1, 2, 3])

    # Résultat attendu
    expected_ot = np.array([1, 2, 3])

    # Appeler la fonction
    ot = MDD(v, J)

    # Vérifier les résultats
    assert np.allclose(ot, expected_ot), f"Erreur dans MDD. Résultat obtenu : {ot}, attendu : {expected_ot}"
    print("Résultat : OK\n")


def test_MDI():
    """
    Test de la fonction MDI (Vérification des vitesses articulaires calculées).
    """
    print("Test : MDI")
    # Définir une jacobienne J (exemple simple)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Définir une vitesse OT souhaitée x
    x = np.array([1, 2, 3])

    # Résultat attendu
    expected_v = np.array([1, 2, 3])

    # Appeler la fonction
    v = MDI(x, J)

    # Vérifier les résultats
    assert np.allclose(v, expected_v), f"Erreur dans MDI. Résultat obtenu : {v}, attendu : {expected_v}"
    print("Résultat : OK\n")


def test_MDD_MDI_integration():
    """
    Test d'intégration entre MDD et MDI.
    Vérifie que MDI(MDD(v, J), J) retourne v (propriété d'inversion).
    """
    print("Test : Intégration MDD et MDI")
    # Définir une jacobienne J (exemple simple)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Définir des vitesses articulaires v
    v = np.array([1, 2, 3])

    # Calculer OT avec MDD
    ot = MDD(v, J)

    # Calculer v récupéré avec MDI
    v_recovered = MDI(ot, J)

    # Vérifier les résultats
    assert np.allclose(v, v_recovered), f"Erreur dans l'intégration MDD-MDI. Résultat obtenu : {v_recovered}, attendu : {v}"
    print("Résultat : OK\n")




# Exécution des tests
if __name__ == "__main__":
    print("Lancement des tests...\n")
    test_calculate_z_and_o()
    test_Jacob_geo()
    test_Jacob_analytique()
    test_MDD()
    test_MDI()
    test_jacobienne_geo_vs_analytique()
    test_MDD()
    test_MDI()
    test_MDD_MDI_integration()

    print("Tous les tests ont été passés avec succès.")
