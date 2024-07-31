#!/usr/bin/env python3

from planar_3dof_control.move import JointMover

from antropomorphic_project.generate_matrixes import HomogeneousMatrix, DHParameters
from sympy import pi

def main():
    theta_1 = input("Enter theta_1 value: ")
    theta_2 = input("Enter theta_2 value: ")
    theta_3 = input("Enter theta_3 value: ")

    print(theta_1, theta_2, theta_3)
    DH_param_1 = DHParameters(
        {"theta":theta_1,
        "alpha":pi/2,
        "d":0,
        "r":0})
    
    DH_param_2 = DHParameters(
        {"theta":theta_2,
        "alpha":0,
        "d":0,
        "r":1.0})
    
    DH_param_3 = DHParameters(
        {"theta":theta_3,
        "alpha":0,
        "d":0,
        "r":1.0})
    
    A_0_1 = HomogeneousMatrix()
    A_1_2 = HomogeneousMatrix()
    A_2_3 = HomogeneousMatrix()
    A_0_2 = HomogeneousMatrix()
    A_0_3 = HomogeneousMatrix()

    A_0_1.compute_matrix(DH_param_1)
    A_1_2.compute_matrix(DH_param_2)
    A_2_3.compute_matrix(DH_param_3)

    A_0_2.A = A_0_1 * A_1_2
    A_0_3.A = A_0_2 * A_2_3
    A_0_3.simplify()
    A_0_3.generate_matrix("A_0_3_simplified_evaluated")

    A_0_3.position()
    
    A_0_3.orientation()

if __name__ == "__main__":
    main()