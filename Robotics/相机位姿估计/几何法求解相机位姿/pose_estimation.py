from __future__ import division
import math
import cmath
import numpy as np
import timeit


def ferrari(a,b,c,d,e):
    "resolution of P=ax^4+bx^3+cx^2+dx+e=0"
    "CN all coeffs real."
    "First shift : x= z-b/4/a  =>  P=z^4+pz^2+qz+r"
    z0 = b/4/a
    a2, b2, c2, d2 = a*a, b*b, c*c, d*d
    p = -3*b2/(8*a2)+c/a
    q = b*b2/8/a/a2 - 1/2*b*c/a2 + d/a
    r = -3/256*b2*b2/a2/a2 + c*b2/a2/a/16-b*d/a2/4+e/a
    "Second find X so P2=AX^3+BX^2+C^X+D=0"
    A = 8
    B = -4*p
    C = -8*r
    D = 4*r*p-q*q
    y0, y1, y2 = cardan(A, B, C, D)
    if abs(y1.imag) < abs(y0.imag):
        y0 = y1
    if abs(y2.imag) < abs(y0.imag):
        y0 = y2
    a0 = (-p+2*y0.real)**.5
    if a0 == 0:
        b0 = y0**2-r
    else:
        b0 = -q/2/a0
    r0, r1 = roots2(1, a0, y0+b0)
    r2, r3 = roots2(1, -a0, y0-b0)
    return (r0-z0, r1-z0, r2-z0, r3-z0)


def cardan(a, b, c, d):
    J = cmath.exp(2j*math.pi/3)
    Jc = 1/J
    u = np.empty(2, np.complex128)
    z0 = b/3/a
    a2, b2 = a*a, b*b
    p = -b2/3/a2 + c/a
    q = (b/27*(2*b2/a2-9*c/a)+d)/a
    D = -4*p*p*p-27*q*q
    r = cmath.sqrt(-D/27+0j)
    u = ((-q-r)/2)**0.33333333333333333333333
    v = ((-q+r)/2)**0.33333333333333333333333
    w = u*v
    w0 = abs(w+p/3)
    w1 = abs(w*J+p/3)
    w2 = abs(w*Jc+p/3)
    if w0 < w1:
        if w2 < w0:
            v *= Jc
    elif w2 < w1:
        v *= Jc
    else:
        v *= J
    return u+v-z0, u*J+v*Jc-z0, u*Jc+v*J-z0


def roots2(a, b, c):
    bp = b/2
    delta = bp*bp-a*c
    u1 = (-bp-delta**.5)/a
    u2 = -u1-b/a
    return u1, u2



def calculate_pitch_deltal_test(): #by xinghua
    ## Set the parameters
    # definition:
    #l1, perpendicular to conveyor belt, i.e., along y direction, the measured value of the eclipse,unit is meter and calculated as l1=ly_pixel*mu
    #l2, parelled to conveyor belt,i.e., along x direction, the measured value of the eclipse, unit is meter and calculated as l2=lx_pixel*mu
    l1 = 5.79
    l2 = 7.48
    delta_c1 = 0.001
    delta_c2 = 30.44
    f = 30
    l = 0.1
    
    d = f*l/l1
    
    delta_lx = d*delta_c2/f
    delta_ly = d*delta_c1/f

    ## Calculate the coefficients
    A = l2**4*l1**2
    B = 2*delta_c2*f*l2**3*l1
    C = delta_c2**2*f**2*l2**2+f**4*l2**2-2*f**2*l2**2*l1**2
    D = -2*delta_c2*f**3*l2*l1
    E = f**4*l1**2-f**4*l2**2
    arg = (A, B, C, D, E)
    arg = (x*1e10 for x in arg)
    A, B, C, D, E = arg
    ans = ferrari(A,B,C,D,E)
    potential_ans=[]
    for a in ans:
        if a.imag == 0:
            x = a.real
            beta = math.asin(x)/math.pi*180
            potential_ans.append(beta)
    return [d,delta_lx,delta_ly,potential_ans]


def calculate_pitch_deltal(l1,l2,delta_c1, delta_c2, l_meter):
    ## Set the parameters
    # definition:
    #l1, perpendicular to conveyor belt, i.e., along y direction, the measured value of the eclipse,unit is meter and calculated as l1=ly_pixel*mu
    #l2, parelled to conveyor belt,i.e., along x direction, the measured value of the eclipse, unit is meter and calculated as l2=lx_pixel*mu
    #unit for l1,l2,delta_c1, delta_c2 are all lx_pixel
    
    mu = 3.45*1e-6
    f = 1024
    d_meter = f*l_meter/(l1)
    delta_lx_meter = d_meter*delta_c2/f
    delta_ly_meter = d_meter*delta_c1/f

    ## Calculate the coefficients
    A = l1**4*l2**2
    B = 2*delta_c2*f*l1**3*l2
    C = delta_c2**2*f**2*l1**2+f**4*l1**2-2*f**2*l1**2*l2**2
    D = -2*delta_c2*f**3*l1*l2
    E = f**4*l2**2-f**4*l1**2
    arg = (A, B, C, D, E)
    arg = (x for x in arg)
    A, B, C, D, E = arg
    ans = ferrari(A,B,C,D,E)
    potential_ans=[]
    for a in ans:
        if a.imag == 0:
            x = a.real
            beta = math.asin(x)/math.pi*180
            potential_ans.append(beta)
    
    # calculate delta lx that parelled to conveyor belt.
    potential_move=[]
    delta_l=d_meter*delta_c2/f
    for beta in potential_ans:
        beta_rad=beta/180*math.pi
        delta_l_conveyor=(d_meter*math.tan(beta_rad)-delta_l)*math.cos(beta_rad)
        potential_move.append(delta_l_conveyor)
    return [d_meter,delta_lx_meter,delta_ly_meter, potential_ans]


    

if __name__ == '__main__':
    ans=calculate_pitch_deltal(300,250,100,0.1,0.0045)
    print(ans)
    # Make the coeffecients larger to reduce computation error
    
    ## Calculate the numerical solution (minimum error)
    # min_error = 9999999
    # min_angle = 0
    # for beta in range(-180, 180):
    #     x = math.sin(beta/180*math.pi)
    #     current_error = abs(A*(x**4)+B*(x**3)+C*(x**2)+D*x+E)
    #     if current_error < min_error:
    #         min_error = current_error
    #         min_angle = beta
    #     elif beta==(min_angle+1):
    #         print('estimation angle: {}, error: {}'.format(min_angle, current_error))
    # print('----------------------')
    # print('delta l: ', delta_lx)
    
