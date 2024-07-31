#!/usr/bin/env python3

from math import atan2, pi, sin, cos, pow, sqrt



from dataclasses import dataclass
@dataclass
class EndEffectorWorkingSpace:
    # Pos of The P3, which is the one we resolved for
    Pee_x: float
    Pee_y: float
    Pee_z: float

class ComputeIk():

    def __init__(self, DH_parameters):
        
        # DH parameters
        self.DH_parameters_ = DH_parameters

    def get_dh_param(self, name):

        if name in self.DH_parameters_:
            return self.DH_parameters_[name]
        else:
            assert False, "Asked for Non existen param DH name ="+str(name)

    def compute_ik(self, end_effector_pose, theta2_config = "plus", theta3_config = "plus"):
        
        # Initialization
        Pee_x = end_effector_pose.Pee_x
        Pee_y = end_effector_pose.Pee_y
        Pee_z = end_effector_pose.Pee_z

        # We get all the DH parameters
        r2 = self.get_dh_param("r2")
        r3 = self.get_dh_param("r3")

        print("Input Data===== theta_2_config CONFIG = "+str(theta2_config))
        print("Input Data===== theta_3_config CONFIG = "+str(theta3_config))
        print("Pee_x = "+str(Pee_x))
        print("Pee_y = "+str(Pee_y))
        print("Pee_z = "+str(Pee_z))
        print("r2 = "+str(r2))
        print("r3 = "+str(r3))

        possible_solution = True

        # We declare all the equations for theta1, theta2, theta3
        #########################################################################
        # theta_1

        theta_1 = atan2(Pee_y,Pee_x)

        # theta_3
        c3 = ( (pow(Pee_x,2) + pow(Pee_y,2) + pow(Pee_z,2)) - (pow(r2,2) + pow(r3,2))) / (2.0 * r2 * r3)

        # We have to decide which solution we want
        if theta3_config == "plus":
            # Positive
            numerator = sqrt(1-pow(c3,2))
        else:
            # Negative
            numerator = -1.0 * sqrt(1-pow(c3,2))

        denominator = c3

        theta_3 = atan2(numerator, denominator)

        # theta_2
        alpha_numerator = sqrt(pow(Pee_z,2))
        alpha_denominator = sqrt((pow(Pee_x,2) + pow(Pee_y,2)))
        gamma_numarator = r3*sin(theta_3)
        gamma_denominator = r2 + r3*cos(theta_3)

        if theta2_config == "plus":
            theta_2 = atan2(alpha_numerator,alpha_denominator) - atan2(gamma_numarator,gamma_denominator)
        else:
            theta_2 = - atan2(alpha_numerator,alpha_denominator) - atan2(gamma_numarator,gamma_denominator)
            # Adjust thetas to fit the right quadrant
            if theta2_config == theta3_config:
                theta_2 += -pi
            else:
                theta_2 -= -pi
            theta_1 -= pi
        

        print("theta_1 solution possible C1=="+str(cos(theta_1))+", S1=="+str(sin(theta_1)))
        print("theta_2 solution possible C2=="+str(cos(theta_2))+", S2=="+str(sin(theta_2)))
        print("theta_3 solution possible C3=="+str(cos(theta_3))+", S3=="+str(sin(theta_3)))

        # Verify that the solution is reachable by the real robot (joint limitations are respected)
        if not(-pi/4 <= theta_2 <= 3*pi/4):
            print(">>>>>>>>>>>>>>> theta_2 NOT POSSIBLE, MIN="+str(-pi/4)+", theta_2="+str(theta_2)+", MAX="+str(3*pi/4))
            possible_solution = False
        if not(-3*pi/4 <= theta_3 <= 3*pi/4):
            print(">>>>>>>>>>>>>>> theta_2 NOT POSSIBLE, MIN="+str(-3*pi/4)+", theta_2="+str(theta_3)+", MAX="+str(3*pi/4))
            possible_solution = False
        
        theta_array = [theta_1, theta_2, theta_3]

        return theta_array, possible_solution

def calculate_ik(Pee_x, Pee_y, Pee_z, DH_parameters, theta2_config = "plus", theta3_config = "plus"):



    ik = ComputeIk(DH_parameters = DH_parameters)
    end_effector_pose = EndEffectorWorkingSpace(Pee_x = Pee_x,
                                                Pee_y = Pee_y,
                                                Pee_z = Pee_z)

    thetas, possible_solution = ik.compute_ik(  end_effector_pose=end_effector_pose,
                                                theta2_config = theta2_config,
                                                theta3_config = theta3_config)

    print("Angles thetas solved ="+str(thetas))
    print("possible_solution = "+str(possible_solution))

    return thetas, possible_solution

if __name__ == '__main__':
    
    r1 = 0.0
    r2 = 1.0
    r3 = 1.0

    # theta_i here are valriables of the joints
    # We only fill the ones we use in the equations, the others were already 
    # replaced in the Homogeneous matrix
    DH_parameters={"r1":r1,
                    "r2":r2,
                    "r3":r3}

    Pee_x = 0.5
    Pee_y = 0.6
    Pee_z = 0.7

    # Calculate the inverse kinematic for all four possible configurations
    calculate_ik(Pee_x=Pee_x, Pee_y=Pee_y, Pee_z=Pee_z,DH_parameters=DH_parameters)
    calculate_ik(Pee_x=Pee_x, Pee_y=Pee_y, Pee_z=Pee_z,DH_parameters=DH_parameters, theta2_config = "plus", theta3_config = "minus")
    calculate_ik(Pee_x=Pee_x, Pee_y=Pee_y, Pee_z=Pee_z,DH_parameters=DH_parameters, theta2_config = "minus", theta3_config = "plus")
    calculate_ik(Pee_x=Pee_x, Pee_y=Pee_y, Pee_z=Pee_z,DH_parameters=DH_parameters, theta2_config = "minus", theta3_config = "minus")