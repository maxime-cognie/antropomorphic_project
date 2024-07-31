#!/usr/bin/env python3

from sympy import Matrix, cos, sin, Symbol, trigsimp, pi, preview, eye
from sympy.interactive import printing


class DHParameters():
    def __init__(self, DH_param):
        # DH parameters
        self.DH_param_ = DH_param
        self.theta = self.get_dh_param("theta")
        self.alpha = self.get_dh_param("alpha")
        self.d = self.get_dh_param("d")
        self.r = self.get_dh_param("r")

    def get_dh_param(self, name):

        if name in self.DH_param_:
            return self.DH_param_[name]
        else:
            assert False, "Asked for Non existen param DH name ="+str(name)
    
    def __str__(self):
        return f'DH parameters:\n theta: {self.theta}\n alpha: {self.alpha}\n d: {self.d}\n r: {self.r}'
        

class HomogeneousMatrix():
    def __init__(self):
        self.A = eye(4)
    
    def __mul__(self, other):
        return self.A * other.A

    def compute_matrix(self, dh_param):
        print("Compute Matrix for " + str(dh_param))
        self.A = Matrix([[cos(dh_param.theta), -sin(dh_param.theta)*cos(dh_param.alpha), sin(dh_param.theta)*sin(dh_param.alpha), dh_param.r*cos(dh_param.theta)],
                            [sin(dh_param.theta), cos(dh_param.theta)*cos(dh_param.alpha), -cos(dh_param.theta)*sin(dh_param.alpha), dh_param.r*sin(dh_param.theta)],
                            [0, sin(dh_param.alpha), cos(dh_param.alpha), dh_param.d],
                            [0,0,0,1]])
    
    def generate_matrix(self, file_name):
        printing.init_printing(use_latex = True)
        print("Generate Matrix: " + file_name)
        preview(self.A, viewer="file", filename=file_name+".png", dvioptions=["-D","300"])
    
    def simplify(self):
        self.A = trigsimp(self.A)
    
    def position(self):
        print("\nPosition Matrix:")
        print(self.A[0:3,3])
    
    def orientation(self):
        print("\nOrientation Matrix:")
        print(self.A[0:3,0:3])

def main():
    DH_param_1 = DHParameters(
        {"theta":Symbol("theta_1"),
        "alpha":pi/2,
        "d":0,
        "r":0})
    
    DH_param_2 = DHParameters(
        {"theta":Symbol("theta_2"),
        "alpha":0,
        "d":0,
        "r":Symbol("r_2")})
    
    DH_param_3 = DHParameters(
        {"theta":Symbol("theta_3"),
        "alpha":0,
        "d":0,
        "r":Symbol("r_3")})
    
    A_0_1 = HomogeneousMatrix()
    A_1_2 = HomogeneousMatrix()
    A_2_3 = HomogeneousMatrix()

    A_0_1.compute_matrix(DH_param_1)
    A_1_2.compute_matrix(DH_param_2)
    A_2_3.compute_matrix(DH_param_3)

    A_0_1.generate_matrix("A_0_1")    
    A_1_2.generate_matrix("A_1_2")    
    A_2_3.generate_matrix("A_2_3")

    A_0_2 = HomogeneousMatrix()
    A_0_3 = HomogeneousMatrix() 

    A_0_2.A = A_0_1 * A_1_2
    A_0_3.A = A_0_2 * A_2_3
    A_0_3.generate_matrix("A_0_3")
    A_0_3.simplify()
    A_0_3.generate_matrix("A_0_3_simplified")
    
if __name__ == "__main__":
    main()
