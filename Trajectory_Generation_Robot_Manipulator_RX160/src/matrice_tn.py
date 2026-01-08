import numpy as np


def matrice_Tim1_Ti(qi, ai_m1, alphai_m1, ri, Debug=False):
    """
    Calcule la matrice de transformation DH entre deux liaisons successives.

    Arguments :
        qi : Angle de la liaison i (en radians).
        ai_m1 : Longueur entre les axes des liaisons (en mm).
        alphai_m1 : Angle entre les axes z_{i-1} et z_i (en radians).
        ri : Décalage suivant z_i (en mm).
        Debug : Si True, affiche les étapes intermédiaires pour débogage.

    Retourne :
        Matrice 4x4 de transformation DH.
    """
    matrix_res = np.zeros((4, 4))

    # Calcul des coefficients
    matrix_res[0, 0] = np.cos(qi)
    matrix_res[0, 1] = -np.sin(qi)
    matrix_res[0, 2] = 0
    matrix_res[0, 3] = ai_m1

    matrix_res[1, 0] = np.sin(qi) * np.cos(alphai_m1)
    matrix_res[1, 1] = np.cos(qi) * np.cos(alphai_m1)
    matrix_res[1, 2] = -np.sin(alphai_m1)
    matrix_res[1, 3] = -ri * np.sin(alphai_m1)

    matrix_res[2, 0] = np.sin(qi) * np.sin(alphai_m1)
    matrix_res[2, 1] = np.cos(qi) * np.sin(alphai_m1)
    matrix_res[2, 2] = np.cos(alphai_m1)
    matrix_res[2, 3] = ri * np.cos(alphai_m1)

    matrix_res[3, 0] = 0
    matrix_res[3, 1] = 0
    matrix_res[3, 2] = 0
    matrix_res[3, 3] = 1

    if Debug:
        print(f"Debug matrice_Tim1_Ti:")
        print(f"  qi (rad) = {qi}, ai_m1 = {ai_m1}, alphai_m1 (rad) = {alphai_m1}, ri = {ri}")
        print(f"  Matrice T_i-1,i :\n{matrix_res}")

    return matrix_res



def generate_transformation_matrices(q, dh, round_p=False, Debug=False):
    """
    Génère une liste de matrices de transformation T(i, i+1) à partir des paramètres DH.

    Arguments :
        dh : Dictionnaire contenant les paramètres DH (a_i_m1, alpha_i_m1, r_i).
        q : Liste des angles articulaires (en radians).
        round_p : Tuple (nombre de décimales, seuil pour arrondir à 0).
        Debug : Si True, affiche les étapes intermédiaires pour débogage.

    Retourne :
        Liste de matrices 4x4 de transformation T(i, i+1).
    """
    transformation_matrices = []

    # Copie locale de q pour éviter les effets secondaires
    q_local = q.copy()
    q_local.append(0)  # Ajouter un angle fixe pour la liaison finale
    q_local=np.radians(q_local)

    if Debug:
        print("\n--- Début de generate_transformation_matrices ---")
        print(f"q initial : {q}")
        print(f"q local avec angle fixe : {q_local}")
        print(f"Paramètres DH : {dh}")

    for i in range(len(dh['a_i_m1'])):
        t_i_ip1 = matrice_Tim1_Ti(
            q_local[i],
            dh['a_i_m1'][i],
            dh['alpha_i_m1'][i],
            dh['r_i'][i],
            Debug=Debug
        )

        if round_p:
            t_i_ip1 = np.round(t_i_ip1, round_p[0])
            t_i_ip1[np.abs(t_i_ip1) < round_p[1]] = 0

        if Debug:
            print(f"\nMatrice T_{i},{i+1} calculée :\n{t_i_ip1}")

        transformation_matrices.append(t_i_ip1)

    if Debug:
        print("\n--- Fin de generate_transformation_matrices ---")
        print(f"Liste des matrices générées :")
        for i, T in enumerate(transformation_matrices):
            print(f"Matrice T_{i},{i+1} :\n{T}")

    return transformation_matrices




# mgd
def matrice_Tn(dh, q, Debug=False):
    """
    Calcule la matrice T0,n en utilisant les paramètres DH et les angles q.

    Arguments :
        dh : Dictionnaire contenant les paramètres DH.
        q : Liste des angles articulaires (en radians).
        Debug : Si True, affiche les étapes intermédiaires pour débogage.

    Retourne :
        Matrice T0,n (4x4).
    """
    # Copie locale de q pour éviter les effets secondaires
    q_local = q.copy()
    q_local.append(0)  # Ajouter un angle fixe pour la liaison finale
    q_local=np.radians(q_local)

    nbliaison = len(dh['a_i_m1'])
    result_matrix = np.eye(4)

    if Debug:
        print("\n--- Début de matrice_Tn ---")
        print(f"q fourni : {q}")
        print(f"q local avec angle fixe : {q_local}")
        print(f"Paramètres DH : {dh}")

    for i in range(nbliaison):
        mat_temp = matrice_Tim1_Ti(q_local[i], dh['a_i_m1'][i], dh['alpha_i_m1'][i], dh['r_i'][i], Debug=Debug)
        result_matrix = np.dot(result_matrix, mat_temp)

        if Debug:
            print(f"\nMatrice T0,{i+1} après multiplication :\n{result_matrix}")

    if Debug:
        print("\n--- Fin de matrice_Tn ---")
        print(f"Matrice T0,n finale :\n{result_matrix}")

    return result_matrix



# Fonction qui donne les coordonnées obtenus d'une matrice T(0,n)
def xy_Ot(result_matrix):
    return (result_matrix[:3, -1])


# MGD avec q liste d'angles, L liste de longueurs
def mgd(q, Liaisons, Debug=False):
    """
    Calcule les coordonnées opérationnelles (x, y, z) pour une configuration donnée.

    Arguments :
        q : Liste des angles articulaires en degrés (q1, q2, q3).
        Liaisons : Liste des dimensions des liaisons sous forme [horizontal, vertical, profondeur].
        Debug : Si True, affiche les étapes intermédiaires pour débogage.

    Retourne :
        np.array : Coordonnées opérationnelles [x, y, z].
    """
    # Vérifications des entrées
    assert len(q) == 3, "La liste des angles `q` doit contenir exactement 3 éléments."
    assert len(Liaisons) == 3, "La liste `Liaisons` doit contenir exactement 3 liaisons."
    for liaison in Liaisons:
        assert len(liaison) == 3, "Chaque liaison doit être définie par 3 paramètres : [horizontal, vertical, profondeur]."


    # Extraction des dimensions des liaisons
    L1, L2, L3 = Liaisons

    # Angles articulaires en radians
    teta1, teta2, teta3 = np.radians(q)

    # Contributions horizontales
    x1 = L1[0] * np.cos(teta1)
    x2 = L2[2] * np.cos(teta1 + np.pi / 2)
    x3 = L2[1] * np.cos(teta1) * np.cos(teta2)
    x4 = L3[2] * np.cos(teta1 - np.pi / 2)
    x5 = L3[1] * np.cos(teta1) * np.cos(teta3 + teta2)

    # Contributions verticales
    y1 = L1[0] * np.sin(teta1)
    y2 = L2[2] * np.sin(teta1 + np.pi / 2)
    y3 = L2[1] * np.sin(teta1) * np.cos(teta2)
    y4 = L3[2] * np.sin(teta1 - np.pi / 2)
    y5 = L3[1] * np.sin(teta1) * np.cos(teta3 + teta2)

    # Contributions en hauteur
    z1 = L1[1]
    z2 = L2[1] * np.sin(teta2)
    z3 = L3[1] * np.sin(teta3 + teta2)

    # Coordonnées finales
    x = x1 + x2 + x3 + x4 + x5
    y = y1 + y2 + y3 + y4 + y5
    z = z1 + z2 + z3

    if Debug:
        print(f"Debug MGD:")
        print(f"  Angles (radians): teta1={teta1}, teta2={teta2}, teta3={teta3}")
        print(f"  Contributions X: {x1}, {x2}, {x3}, {x4}, {x5}")
        print(f"  Contributions Y: {y1}, {y2}, {y3}, {y4}, {y5}")
        print(f"  Contributions Z: {z1}, {z2}, {z3}")
        print(f"  Coordonnées finales: X={x}, Y={y}, Z={z}")

    # Retour des coordonnées
    return np.array([x, y, z], dtype=np.float64)




# MGI: On donne une configuration initiale au robot et on demande de ce mettre dans une autre
# On rentre coordonnées et on récupere des angles
def mgi(Xd, Liaisons, Debug=False):
    x, y, z = Xd
    L1 = Liaisons[0]  # [horizontal, vertical, profondeur]
    L2 = Liaisons[1]
    L3 = Liaisons[2]
    solutions = []

    def calculer_solutions(q1):
        X = L2[1]
        Y = L3[1]
        Z1 = np.cos(q1) * x + np.sin(q1) * y - L1[0]
        Z2 = z - L1[1]

        if Debug:
            print(f"Debug: Z1={Z1}, Z2={Z2}, X={X}, Y={Y}")

        # Calcul de q3
        c3 = (Z1 ** 2 + Z2 ** 2 - X ** 2 - Y ** 2) / (2 * X * Y)
        if c3 < -1 or c3 > 1:
            return []  # Pas de solution valide
        c3 = np.clip(c3, -1, 1)

        q31 = np.arctan2(np.sqrt(1 - c3 ** 2), c3)
        q32 = np.arctan2(-np.sqrt(1 - c3 ** 2), c3)

        if Debug:
            print(f"Debug: c3={c3}, q31={q31}, q32={q32}")

        # Calcul de q2
        B1 = X + Y * c3
        B21 = Y * np.sin(q31)
        B22 = Y * np.sin(q32)

        s21 = (B1 * Z2 - B21 * Z1) / (B1 ** 2 + B21 ** 2)
        c21 = (B1 * Z1 + B21 * Z2) / (B1 ** 2 + B21 ** 2)
        q21 = np.arctan2(s21, c21)

        s22 = (B1 * Z2 - B22 * Z1) / (B1 ** 2 + B22 ** 2)
        c22 = (B1 * Z1 + B22 * Z2) / (B1 ** 2 + B22 ** 2)
        q22 = np.arctan2(s22, c22)


        if Debug:
            print(f"Debug: q21={q21}, q22={q22}")

        return [[q1, q21, q31], [q1, q22, q32]]

    q1_1 = np.arctan2(y, x)
    solutions.extend(calculer_solutions(q1_1))
    q1_2 = q1_1 - np.pi
    solutions.extend(calculer_solutions(q1_2))

    return solutions





def verifier_solutions(Xd, Liaisons):
    # Obtenir toutes les combinaisons possibles d'angles avec la fonction mgi
    solutions = mgi(Xd, Liaisons)

    print("\nValeurs possibles des angles pour atteindre la configuration souhaitée Xd:", Xd)
    for i, sol in enumerate(solutions):
        print(f"Solution {i + 1} (en degrés) : {np.round(np.degrees(sol), 2)}")

    # Itérer sur chaque combinaison d'angles et vérifier avec la fonction mgd
    for i, q in enumerate(np.degrees(solutions)):
        # Calculer les coordonnées (x, y, z) en utilisant la fonction mgd avec les angles q
        Xd_mgd = mgd(q, Liaisons)
        Xd_mgd = np.round(Xd_mgd, 3)

        # Calculer l'erreur entre les coordonnées souhaitées et celles obtenues
        erreur = np.linalg.norm(Xd_mgd - Xd)

        # Afficher le résultat pour chaque ensemble d'angles
        print(f"\nVérification de la solution {i + 1}:")
        print(f"Angles (en degrés): {np.round((q), 2)}")
        print(f"Coordonnées obtenues par MGD: {Xd_mgd}")
        print(f"Erreur par rapport à la position désirée: {np.round(erreur, 6)}")

        if erreur < 0.1:  # Tolérance pour considérer que la solution est correcte
            print("Résultat : Correct !")
        else:
            print("Résultat : Incorrect")
