import numpy as np
from src.modele_differentiel import *
from src.matrice_tn import *
from src.const_v import dh, Liaisons

# Enable debug mode
Debug = True

# Joint angles for tests
# Angles for testing
q_test = [np.pi, np.pi/2, np.pi/2]

# Target position for IGM
Xd_test = [300, 200, 600]

def test_calculate_z_and_o():
    print("Test: calculate_z_and_o")
    T = matrice_Tim1_Ti(q_test[0], dh["a_i_m1"][0], dh["alpha_i_m1"][0], dh["r_i"][0])
    z, o = calculate_z_and_o(T)
    assert z.shape == (3,), "The vector z is not of size 3"
    assert o.shape == (3,), "The vector o is not of size 3"
    print("Result: OK\n")

def test_Jacob_geo():
    print("Test: Jacob_geo")
    matrices = generate_transformation_matrices(q_test, dh, round_p=(3, 1e-6))
    J = Jacob_geo(matrices)
    assert J.shape == (6, len(q_test)), "The geometric Jacobian is not of size 6x3"
    print("Geometric Jacobian calculated:\n", J)
    print("Result: OK\n")

def test_Jacob_analytique():
    print("Test: Jacob_analytique")
    J = Jacob_analytique()
    assert J.shape == (6, len(q_test)), "The analytical Jacobian is not of size 6x3"
    print("Analytical Jacobian calculated:\n", J)
    print("Result: OK\n")

def test_MDD():
    print("Test: MDD")
    matrices = generate_transformation_matrices(q_test, dh)
    J = Jacob_geo(matrices)
    velocities = MDD([0.1, 0.2, 0.3], J)
    assert len(velocities) == 6, "The OT velocities are not of size 6"
    print("OT velocities calculated:", velocities)
    print("Result: OK\n")

def test_MDI():
    print("Test: MDI")
    matrices = generate_transformation_matrices(q_test, dh)
    J = Jacob_geo(matrices)
    q_dot = MDI([0.5, 0.3, -0.2, 0.1, 0.0, -0.1], J)
    assert len(q_dot) == len(q_test), "The joint velocities are not of size 3"
    print("Joint velocities calculated:", q_dot)
    print("Result: OK\n")


def test_jacobian_geo_vs_analytical():
    print("Test: Consistency between geometric and analytical Jacobians")
    matrices = generate_transformation_matrices(q_test, dh)

    # Compute Jacobians
    J_geo = Jacob_geo(matrices)
    J_analytical_num = Jacob_analytique(q_test)

    # Compare geometric and numerical analytical Jacobians
    print("Geometric Jacobian (numerical):\n", J_geo)
    print("Analytical Jacobian (numerical):\n", J_analytical_num)

    # Compare individual terms
    for i in range(6):
        for j in range(3):
            print(f"Difference J[{i}, {j}]: Geometric = {J_geo[i, j]}, Analytical = {J_analytical_num[i, j]}, "
                  f"Diff = {J_geo[i, j] - J_analytical_num[i, j]}")

    assert np.allclose(J_geo, J_analytical_num, atol=1e-6), \
        "The geometric and analytical Jacobians do not match"
    print("Result: OK\n")


def test_MDD():
    """
    Test for the MDD function (Verification of calculated OT velocities).
    """
    print("Test: MDD")
    # Define a Jacobian J (simple example)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Define joint velocities v
    v = np.array([1, 2, 3])

    # Expected result
    expected_ot = np.array([1, 2, 3])

    # Call the function
    ot = MDD(v, J)

    # Verify results
    assert np.allclose(ot, expected_ot), f"Error in MDD. Result obtained: {ot}, expected: {expected_ot}"
    print("Result: OK\n")


def test_MDI():
    """
    Test for the MDI function (Verification of calculated joint velocities).
    """
    print("Test: MDI")
    # Define a Jacobian J (simple example)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Define a desired OT velocity x
    x = np.array([1, 2, 3])

    # Expected result
    expected_v = np.array([1, 2, 3])

    # Call the function
    v = MDI(x, J)

    # Verify results
    assert np.allclose(v, expected_v), f"Error in MDI. Result obtained: {v}, expected: {expected_v}"
    print("Result: OK\n")


def test_MDD_MDI_integration():
    """
    Integration test between MDD and MDI.
    Verifies that MDI(MDD(v, J), J) returns v (inversion property).
    """
    print("Test: MDD and MDI Integration")
    # Define a Jacobian J (simple example)
    J = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    # Define joint velocities v
    v = np.array([1, 2, 3])

    # Compute OT with MDD
    ot = MDD(v, J)

    # Compute recovered v with MDI
    v_recovered = MDI(ot, J)

    # Verify results
    assert np.allclose(v, v_recovered), f"Error in MDD-MDI integration. Result obtained: {v_recovered}, expected: {v}"
    print("Result: OK\n")


# Run tests
if __name__ == "__main__":
    print("Starting tests...\n")
    test_calculate_z_and_o()
    test_Jacob_geo()
    test_Jacob_analytique()
    test_MDD()
    test_MDI()
    test_jacobian_geo_vs_analytical()
    test_MDD()
    test_MDI()
    test_MDD_MDI_integration()

    print("All tests passed successfully.")
