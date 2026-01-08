from trajectory_generation import *
from modele_differentiel import *
from Robot_repr import bras_rob_model3D


# Afficher chaque matrice de transformation pour suivre le calcul et enregistrer dans une liste les matrices

def main_analyse():
    qu = float(input("Angle de liaison q1 en degrée :\n"))
    qd = float(input("Angle de liaison q2 en degrée :\n"))
    qt = float(input("Angle de liaison q3 en degrée :\n"))

    q = [qu, qd, qt]

    transformation_matrices_calc = generate_transformation_matrices(q, dh, round_p=(5, 1e-6))
    transformation_matrices_show = generate_transformation_matrices(q, dh, round_p=(2, 1e-6))
    print("Matrice de translation T01:\n", transformation_matrices_show[0])
    print("\nMatrice de translation T12:\n", transformation_matrices_show[1])
    print("\nMatrice de translation T23:\n", transformation_matrices_show[2])
    print("\nMatrice de translation T34:\n", transformation_matrices_show[3])

    # Calcul de la transformation complète T(0,4)
    print(f"\nMatrice de translation T0{len(dh['sigma_i'])} :")
    matrice_T0Tn = matrice_Tn(dh, q)
    matrice_T0Tn_rounded = np.round(matrice_T0Tn, decimals=0)
    print(matrice_T0Tn_rounded.astype(int))

    # Pour ce TP Z0 représente l'axe vertical et Y0 celui de la profondeur
    print("\nCoordonnées finales grace a matrice T(0,n) en fonction de X0,Y0,Z0:\n", xy_Ot(matrice_T0Tn))
    rep = int(
        input("Vous voulez verifier ces valeurs avec une simulation 3D du bras?? \n(1) pour 'oui', (2) pour 'non':"))
    if rep == 1:
        bras_rob_model3D(Liaisons, q)
    else:
        pass

    print("\nCoordonnées (x, y, z) en mm en fonction des angles de la liste q:")
    Xd_mgd = mgd(q, Liaisons)
    x_mgd = Xd_mgd[0]
    y_mgd = Xd_mgd[1]
    z_mgd = Xd_mgd[2]
    print("x calculé par le MGD:", x_mgd, "\ny calculé par le MGD:", y_mgd, "\nz calculé par le MGD:", z_mgd, "\n")
    rep = int(input(
        "Vous voulez verifier ces valeurs en les introduisant comme coordonnées de l'organe terminale et lui appliquant le MGI pour trouver les angles introduits au debut? \n(1) pour 'oui', (2) pour 'non, je met d'autres valeurs', (3) pour 'non, je continue', :"))
    if rep == 1:
        verifier_solutions(Xd_mgd, Liaisons)
        Rep=int(input("Est ce que vous voulez une représentation de la position du bras pour chaque configuration donnée?\n(1) pour 'oui', (2) pour 'non'"))
        if Rep == 1:
            sol = mgi(Xd_mgd, Liaisons)
            for i, solution in enumerate(sol):  # Iterar sobre cada solución
                bras_rob_model3D(Liaisons, np.degrees(solution))  # Convertir a grados antes de pasar
            else:
                pass
    elif rep == 2:
        print("Veuillez introduire les coordonnées que vous désirés atteindre")
        x_mgi = float(input("Coordonnée x de l'organe terminale :\n"))
        y_mgi = float(input("Coordonnée y de l'organe terminale :\n"))
        z_mgi = float(input("Coordonnée z de l'organe terminale :\n"))
        Xd = [x_mgi, y_mgi, z_mgi]
        verifier_solutions(Xd, Liaisons)
        Rep = int(input(
            "Est ce que vous voulez une représentation de la position du bras pour chaque configuration donnée?\n(1) pour 'oui', (2) pour 'non'"))
        if Rep == 1:
            sol = mgi(Xd, Liaisons)
            for i, solution in enumerate(sol):  # Iterar sobre cada solución
                bras_rob_model3D(Liaisons, np.degrees(solution))  # Convertir a grados antes de pasar
            else:
                pass
    else:
        pass

    # Calcule de Jacobienne geometrique
    REP = int(
        input(
            f"Voulez-vous calculer la jacobienne du robot pour la configuration introduite au début ({q[0]}, {q[1]}, {q[2]})? \n(1) pour 'oui', (2) pour 'non': "
        )
    )
    if REP == 1:
        J_geo = Jacob_geo(transformation_matrices_calc)
        print("\nJacobienne geométrique:")
        print(np.array2string(J_geo, formatter={'float_kind': lambda x: f"{x:7.1f}"}))

        # Calcule de Jacobienne analytique
        # Matrices sous forme analytique
        # Jacob_an = Jacob_analytique(q)
        # print("\nJacobienne analytique:")
        # sp.pprint(Jacob_an)

        # MDD pour dq1=0.1, dq2=0.2, dq3=0.3 appliqué à la position initiale q1=0, q2=0 et q3=0
        print("\nVeuillez introduire les vitesse articulaires que vous souhaitez donner au robot :")
        dq1 = float(input("dq1:\n"))
        dq2 = float(input("dq2:\n"))
        dq3 = float(input("dq3:\n"))
        dq = [dq1, dq2, dq3]
        dX = MDD(dq, J_geo)
        dX_vert = sp.Matrix(np.round(np.array(dX).reshape(-1, 1), 1))
        print("\nValeurs des vitesses linéaires et angulaires du robot pour la configuration demandée(", q[0], ",",
              q[1], ",", q[2], ") lorsqu'on applique dq1 =",
              dq1, ", dq2 =", dq2, ", dq3 =", dq3)
        sp.pprint(dX_vert)
        # Verification en utilisant MDI inversant la Jacobienne
        rep = int(
            input(
                "Voulez-vous verifier ces valeurs en les introduisant comme vitesses linéaires et angulaires du robot? \n(1) pour 'oui', (2) pour 'non, je met d'autres valeurs', (3) pour 'non, je continue':"))
        if rep == 1:
            dq = MDI(dX, J_geo)
            dq_vert = np.array(dq).reshape(-1, 1)
            print(
                "\nCalcul GEOMETRIQUE des valeurs des vitesses articulaires du robot pour sa position initiale lorsqu'on applique dx =",
                dX[0], ", dy=",
                dX[1], ", dz=", dX[2], ", wx=", dX[3], ", wy=", dX[4], ", wz=", dX[5])
            print(dq_vert)
        elif rep == 2:
            print("\nVeuillez introduire les 6 valeurs suivantes")
            dx = float(input("dx="))
            dy = float(input("dy="))
            dz = float(input("dz="))
            wx = float(input("wx="))
            wy = float(input("wy="))
            wz = float(input("wz="))
            dX = [dx, dy, dz, wx, wy, wz]
            dq = MDI(dX, J_geo)
            dq_vert = np.array(dq).reshape(-1, 1)
            print(
                "\nCalcul GEOMETRIQUE des valeurs des vitesses articulaires du robot pour sa position initiale lorsqu'on applique dx =",
                dx, ", dy=",
                dy, ", dz=", dz, ", wx=", wx, ", wy=", wy, ", wz=", wz)
            print(dq_vert)
        else:
            pass
        print("\n")
    else:
        pass
