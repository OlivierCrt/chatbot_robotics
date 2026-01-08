from src.main_analyse import main_analyse
from Tests.plotly3d import *


def menu():
    print("Menu:")
    print("1. Matrices,Mgd,Mgi")
    print("2. Visualiser des lois de mouvement temporelles et les graph associés")
    print("0. Quitter")

    choix = input("Veuillez choisir une option: ")
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1" :
            main_analyse()    
        if choix == "2" :
            V1 = float(input("Vitesse 1 :\n"))
            V2 = float(input("Vitesse 2 :\n"))
            x=float(input("Coordonnée x partagé par A et B :\n"))
            A = np.array([x, float(input("Coordonnée y pour A :\n")), float(input("Coordonnée z pour A :\n"))])
            B = np.array([x, float(input("Coordonnée y pour B :\n")), float(input("Coordonnée z pour B :\n"))])
            K = float(input("Acceleration :\n"))
            while K <= 0.0:
                print("L'accéleleration doit etre positive ! Entrez une acceleration positive.")
                K = float(input("Acceleration :\n"))
            traj(A,B,V1,V2,K, Debug=True)
            print("Voulez vous lancer une simulation avec ces données?")
            k = input("1: Oui 2: Non\n")
            if k == "1" :
                bras_rob_model3D_animation(A,B,V1,V2,K)