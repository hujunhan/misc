import numpy as np

mu = 3.45*1e-6
rad2pi = 180/np.pi
delta_c = 1*mu
# delta_c2=0
l2 = 299*mu
l1 = 300*mu
l = 0.1
f = 0.0045
d = f*l/l1
min_error = np.inf
min_angle = 0
for beta in range(0, 180):
    beta = beta/180*np.pi
    delta_l = l*f*delta_c/(delta_c*l1*np.sin(beta)+f*l1*np.cos(beta))
    y = (d-(delta_l+l)*np.sin(beta))*2*l2/f
    current_error = abs((d-(delta_l+l)*np.sin(beta))*y-2*l*d*np.cos(beta))
    print(current_error)
    if current_error < min_error:
        min_error = current_error
        min_angle = beta
print('estimation angle: {}, error: {}'.format(min_angle*rad2pi, min_error))
        
