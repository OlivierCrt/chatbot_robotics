# Circular Trajectory Generation with a Robot Manipulator - RX160

## Description  
This project focuses on modeling and simulating a 3-DOF RRR robot manipulator, specifically designed for generating and executing circular trajectories in 3D space. It includes tools for geometric and kinematic modeling, trajectory planning, and differential analysis, enabling precise control and simulation of the robot's movements.

---

## Key Functionalities  

### 1. **Geometric Modeling**  
   - **Direct Geometric Modeling (DGM):** Computes the end-effector position and orientation based on joint angles.  
   - **Inverse Geometric Modeling (IGM):** Determines the required joint angles to achieve a desired end-effector position.  

### 2. **Kinematic Modeling**  
   - **Transformation Matrices:** Computes transformation matrices between successive links using Denavit-Hartenberg (DH) parameters.  
   - **Global Transformation Matrix:** Calculates the overall transformation matrix from the base to the end-effector.  

### 3. **Differential Modeling**  
   - **Direct Differential Model (DDM):** Computes end-effector velocities from joint velocities using the Jacobian matrix.  
   - **Inverse Differential Model (IDM):** Computes required joint velocities to achieve a desired end-effector velocity.  

### 4. **Trajectory Generation**  
   - **Circular Trajectory Planning:** Generates smooth circular trajectories in 3D space between two points, with control over initial and final velocities and acceleration.  
   - **Operational and Joint Trajectories:** Provides both operational space (end-effector) and joint space trajectories for execution.  

### 5. **Simulation and Testing**  
   - Includes tools for validating the robot's geometric, kinematic, and trajectory planning models through simulations and tests.  

---

## Usage  

> **Note:** The parameters of the RRR robot can be edited in the file **config.py** to adapt to any configuration.


### 1. **Setup**  
   - Clone the repository:  
     ```bash  
     git clone https://github.com/OlivierCrt/Trajectory_Generation_Robot_Manipulator_RX160  
     ```  
   - Install dependencies:  
     ```bash  
     pip install -r required.txt  
     ```  

### 2. **Running the Project**  
   - Execute the main file to interact with the functionalities:  
     ```bash  
     python Test/main.py  
     ```  
   - If a module error occurs, try:  
     ```bash  
     python -m Tests.main.py  
     ```  
     or add the main directory to your environment variables.  

### 3. **Inputs and Units**  
   - **Linear Velocities:** mm/s  
   - **Angular Velocities:** rad/s  
   - **Joint Velocities:** rad/s  
   - **Distances:** mm  

---

This project provides a comprehensive framework for modeling, simulating, and controlling an RRR robot manipulator, with a focus on circular trajectory generation and execution.


