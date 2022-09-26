import sympy
import numpy as np
def Transform(theta, d, a, alpha):
    ct = sympy.cos(theta)
    st = sympy.sin(theta)
    ca = sympy.cos(alpha)
    sa = sympy.sin(alpha)
    return np.asarray(
        [
            [ct, -st, 0, a],
            [st * ca, ct * ca, -sa, -sa * d],
            [st * sa, ct * sa, ca, ca * d],
            [0, 0, 0, 1],
        ]
    )

x,y,z,theta1,theta2,d1,d2,d3,d4,d5,d6=sympy.symbols('x,y,z,theta1,theta2,d1,d2,d3,d4,d5,d6')
pi=sympy.pi
T_tran_x=Transform(0,0,0,-pi/2)
T_x=Transform(0,x,0,0)
T_tran_y=Transform(pi/2,0,0,pi/2)
T_y=Transform(0,y,0,0)
T_tran_z=Transform(pi/2,0,0,pi/2)
T_z=Transform(0,z,0,0)
T_tran_ms=Transform(pi/2,d2,d4,0)
T_ms=Transform(theta1,0,0,0)
T_tran_ss=Transform(-pi/2,d5,0,-pi/2)
T_ss=Transform(theta2,0,0,0)
T_tran_end=Transform(0,0,0,0)
T_end=Transform(0,d6,0,0)
