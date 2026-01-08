<div align="left">
  <a href="fr_README.md">
    <img src="https://img.shields.io/badge/lang-fr-blue">
  </a>
</div>

# DigiTwin - Circular Trajectory Generation with a Robot Manipulator (Staubli RX160)
### *For a more complete overview of my work, visit my portfolio at [imonge.es](https://imonge.es/proyecto/2?lang=en).*

## Description

This project is a comprehensive RRR robot model, including modeling parameters, simulations, and associated tests. It enables geometric and kinematic modeling calculations as well as trajectory simulations.

---

## File Structure

### `const_v.py`
- Contains the constants defining the RRR robot.
- Axis distance parameters and Denavit-Hartenberg (DH) parameters.

### `matrices_tn.py`
- **`matrice_Tim1_Ti(qi, ai_m1, alphai_m1, ri, Debug=False)`**  
  Calculates the DH transformation matrix between two successive joints.

- **`generate_transformation_matrices(q, dh, round_p=False, Debug=False)`**  
  Generates a list of transformation matrices \( T(i, i+1) \) based on the DH parameters.

- **`matrice_Tn(dh, q, Debug=False)`**  
  Calculates the global matrix \( T0,n \) using the DH parameters and joint angles \( q \).

- **`mgd(q, Liaisons, Debug=False)`**  
  Solves the direct geometric modeling.

- **`mgi(Xd, Liaisons, Debug=False)`**  
  Solves the inverse geometric modeling.

- **`xy_Ot(result_matrix)`**  
  Extracts the operational coordinates obtained from the \( T0,n \) matrix.

---

### `modele_differentiel.py`
- Contains functions related to the robot's differential model, including:
  - Jacobians calculated geometrically.
  - Jacobians calculated analytically.
  - Direct Differential Model (DDM).
  - Inverse Differential Model (IDM).

---

### `trajectory_generation.py`
- **`traj(A, B, V1, V2, K, Debug=False)`**  
  Generates a circular trajectory in \( \mathbb{R}^3 \) space between two points \( A \) and \( B \).  
  **Arguments:**
  - `A`, `B`: Starting and ending points \([x, y, z]\).
  - `V1`, `V2`: Initial and final velocities (mm/s).
  - `K`: Acceleration.
  - `Debug`: Displays details for debugging.  
  **Returns:**
  - Joint trajectories, velocities, and operational positions.

---

### `main.py`
- Main executable file.
- Allows users to test and use all features through guided interactions.

---

### Tests and Simulations
- Auxiliary files contain the necessary simulations and tests to validate the model and functions.

---

## Usage

### 1. Clone the repository
```bash
git clone https://github.com/IsmaTIBU/DigiTwin.git
```
### 2. Install dependencies
```bash
pip install -r required.txt
```
### 3. Run the main file
```bash
python src/main.py
```
### 4. Expected Inputs
  Units :  
    -Linear velocities : mm/s  
    -Angular velocities : rad/s  
    -Joint velocities : rad/s  
    -Distances : mm
