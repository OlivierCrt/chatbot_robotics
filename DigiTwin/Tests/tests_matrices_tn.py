import numpy as np
from src.matrice_tn import *
from src.const_v import *


# Angles for testing
q_test = [np.pi, np.pi/2, 0]

# Enable debugging for tested functions
Debug = True

# Target position for IGM
Xd_test = [300, 200, 600]  # Achievable target position by the robot


# Tests for each function
def test_matrice_Tim1_Ti():
    print("Test: matrice_Tim1_Ti")
    T = matrice_Tim1_Ti(0, dh["a_i_m1"][3], dh["alpha_i_m1"][3], dh["r_i"][3], Debug=Debug)
    assert T.shape == (4, 4), "The returned matrix is not of size 4x4"
    print("Result: OK\n")

def test_generate_transformation_matrices():
    print("Test: generate_transformation_matrices")
    T_matrices = generate_transformation_matrices(q_test, dh, round_p=(2, 1e-6), Debug=Debug)
    assert len(T_matrices) == len(q_test) + 1, "The number of matrices does not match the number of joints"
    for T in T_matrices:
        assert T.shape == (4, 4), "One of the matrices is not of size 4x4"
    print("Result: OK\n")

def test_matrice_Tn():
    print("Test: matrice_Tn")
    Tn = matrice_Tn(dh, q_test, Debug=Debug)
    assert Tn.shape == (4, 4), "The matrix T0,n is not of size 4x4"
    print("Result: OK\n")

def test_xy_Ot():
    print("Test: xy_Ot")
    Tn = matrice_Tn(dh, q_test, Debug=Debug)
    xyz = xy_Ot(Tn)
    assert len(xyz) == 3, "The extracted coordinates are not of size 3"
    print("Result: OK\n")

def test_mgd():
    print("Test: mgd")
    Xd = mgd(q_test, Liaisons, Debug=Debug)
    assert len(Xd) == 3, "The coordinates returned by the MGD are not of size 3"
    print("Result: OK\n")

def test_mgi():
    print("Test: mgi")
    solutions = mgi(Xd_test, Liaisons, Debug=Debug)
    assert isinstance(solutions, list), "The IGM does not return a list"
    assert all(len(sol) == 3 for sol in solutions), "A solution does not contain 3 angles"
    print(f'Solutions IGM = {solutions}')
    print("Result: OK\n")

def test_verifier_solutions():
    print("Test: verifier_solutions")
    verifier_solutions(Xd_test, Liaisons)
    print("Result: Verification completed\n")

# Run tests
if __name__ == "__main__":
    print("Starting tests...\n")
    test_matrice_Tim1_Ti()
    test_generate_transformation_matrices()
    test_matrice_Tn()
    test_xy_Ot()
    test_mgd()
    test_mgi()
    test_verifier_solutions()
    print("All tests were successfully passed.")
