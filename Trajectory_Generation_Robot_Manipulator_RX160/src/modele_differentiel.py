import numpy as np
import sympy as sp


def calculate_z_and_o(T):
    """
    Extrae el vector z y la posición o de una matriz de transformación homogénea.
    """
    z = T[:3, 2]  # Tercera columna (vectores z)
    o = T[:3, 3]  # Cuarta columna (posición)
    return z, o


def Jacob_geo(matrices, Debug=False):
    if Debug:
        print("--- Débogage Jacobienne géométrique ---")
    T_01 = matrices[0]
    T_02 = np.dot(T_01, matrices[1])
    T_03 = np.dot(T_02, matrices[2])
    T_0T = np.dot(T_03, matrices[3])

    z0, o0 = calculate_z_and_o(T_01)
    z1, o1 = calculate_z_and_o(T_02)
    z2, o2 = calculate_z_and_o(T_03)
    _, ot = calculate_z_and_o(T_0T)

    if Debug:
        print(f"z0 = {z0}, o0 = {o0}")
        print(f"z1 = {z1}, o1 = {o1}")
        print(f"z2 = {z2}, o2 = {o2}")
        print(f"ot = {ot}")

    jp1 = np.cross(z0, ot - o0)
    jp2 = np.cross(z1, ot - o1)
    jp3 = np.cross(z2, ot - o2)

    if Debug:
        print(f"jp1 = {jp1}, jp2 = {jp2}, jp3 = {jp3}")

    J = np.array([
        [jp1[0], jp2[0], jp3[0]],
        [jp1[1], jp2[1], jp3[1]],
        [jp1[2], jp2[2], jp3[2]],
        [z0[0], z1[0], z2[0]],
        [z0[1], z1[1], z2[1]],
        [z0[2], z1[2], z2[2]],
    ])
    if Debug:
        print("Jacobienne géométrique (J) :\n", J)
        print("--- Fin du débogage Jacobienne géométrique ---")

    return J


def Jacob_analytique(q=None, Debug=False):
    """
    Calcule la Jacobienne analytique en mode débogage.
    - Si `q` est fourni, la Jacobienne est calculée numériquement.
    - Affiche toujours la Jacobienne symbolique avec les ci et si.

    Paramètres :
        M (list): Liste des matrices de transformation analytiques.
        q (list ou None): Liste des valeurs numériques des angles [q1, q2, q3] (en radians).

    Retour :
        np.ndarray : Jacobienne calculée numériquement si `q` est fourni.
        sp.Matrix : Jacobienne symbolique si `q` n'est pas fourni.
    """
    # Définition des symboles pour c_i et s_i
    c1, s1, c2, s2, c3, s3, c4, s4 = sp.symbols('c1 s1 c2 s2 c3 s3 c4 s4')

    T01 = sp.Matrix([
        [c1, -s1, 0, 0],
        [s1, c1, 0, 0],
        [0, 0, 1, 550],
        [0, 0, 0, 1]
    ])

    T12 = sp.Matrix([
        [c2, -s2, 0, 150],
        [0, 0, -1, 0],
        [s2, c2, 0, 0],
        [0, 0, 0, 1]
    ])

    T23 = sp.Matrix([
        [c3, -s3, 0, 825],
        [s3, c3, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    T34 = sp.Matrix([
        [c4, 0, 0, 735],
        [0, c4, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Calcul des matrices cumulées
    T_01 = T01
    T_02 = T01 * T12
    T_03 = T_02 * T23
    T_0T = T_03 * T34

    # Calcul des vecteurs z et o
    z0 = T_01[:3, 2]
    o0 = T_01[:3, 3]
    z1 = T_02[:3, 2]
    o1 = T_02[:3, 3]
    z2 = T_03[:3, 2]
    o2 = T_03[:3, 3]
    ot = T_0T[:3, 3]

    # Calcul des termes de la Jacobienne
    Jp1 = z0.cross(ot - o0)
    Jp2 = z1.cross(ot - o1)
    Jp2_simp = 735 * c2 * c3 + 825 * c2 - 735 * s2 * s3
    Jp3 = z2.cross(ot - o2)
    Jp3_simp = 735 * (c2 * c3 - s2 * s3)

    # Jacobienne complète
    J = sp.Matrix([
        [Jp1[0], Jp2[0], Jp3[0]],
        [Jp1[1], Jp2[1], Jp3[1]],
        [Jp1[2], Jp2_simp, Jp3_simp],
        [z0[0], z1[0], z2[0]],
        [z0[1], z1[1], z2[1]],
        [z0[2], z1[2], z2[2]],
    ])
    if (Debug):
        # Affichage en mode débogage
        print("--- Débogage Jacobienne analytique ---")
        print("z0 =")
        sp.pprint(sp.Matrix(z0))
        print("o0 =")
        sp.pprint(sp.Matrix(o0))
        print("z1 =")
        sp.pprint(sp.Matrix(z1))
        print("o1 =")
        sp.pprint(sp.Matrix(o1))
        print("z2 =")
        sp.pprint(sp.Matrix(z2))
        print("o2 =")
        sp.pprint(sp.Matrix(o2))
        print("ot =")
        sp.pprint(sp.Matrix(ot))
        print("Jp1 =")
        sp.pprint(sp.Matrix(Jp1))
        print("Jp2 =")
        sp.pprint(sp.Matrix(Jp2))
        print("Jp3 =")
        sp.pprint(sp.Matrix(Jp3))
        print("Jacobienne analytique (symbolique) :")
        sp.pprint(J)
        print("--- Fin du débogage Jacobienne analytique ---")

    # Si des valeurs numériques pour q sont fournies, calculer et retourner la Jacobienne numérique
    if q is not None:
        q = np.radians(q)
        # Substituer les valeurs numériques de q dans les ci et si
        subs = {
            c1: np.cos(q[0]), s1: np.sin(q[0]),
            c2: np.cos(q[1]), s2: np.sin(q[1]),
            c3: np.cos(q[2]), s3: np.sin(q[2]),
        }
        J_numeric = np.array(J.subs(subs)).astype(np.float64)
        return J_numeric

    # Si pas de valeurs numériques, retourner la Jacobienne symbolique
    return J


def MDD(v, J):
    """
    Return vitesses OT
    parametre Vitesses articulaires, J jacobienne

    """
    return np.dot(J, v)


def MDI(x, J):
    """return q vitesse
    param : x vitesse de l OT souhaitée , J jacobienne"""
    return np.dot(np.linalg.pinv(J), x)
