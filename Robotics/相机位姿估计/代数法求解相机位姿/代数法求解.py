#!/usr/bin/env python
# coding: utf-8

# In[1]:


from virtual_camera import VirtualCamera
import numpy as np
from scipy.optimize import fsolve
from scipy.spatial.transform import Rotation
import scipy
import time
set_x = 5.2
set_y = 3.3
set_z = 0.5
set_rx = np.pi/6
set_ry = np.pi/3
set_rz = np.pi/5


# ## 相机scale矩阵 

# In[2]:


L = 1
mu = 3.45e-6
f = 0.003
C_x = 500
C_y = 500
scale = np.asarray([[f/mu, 0, C_x],
                    [0, f/mu, C_y],
                    [0, 0, 1]])
scale_inv = np.linalg.inv(scale)
print(scale_inv)


# In[3]:


r = Rotation.from_euler('XYZ', [-set_rx, -set_ry, -set_rz])
quat = r.as_quat()
print(r.as_matrix())
true_ans = np.asarray([set_x, set_y, set_z, set_rx /
                      np.pi*180, set_ry/np.pi*180, set_rz/np.pi*180])
print(true_ans)


# ## 利用相机模型映射点坐标

# In[4]:


cam = VirtualCamera(set_rx, set_ry, set_rz,
                    set_x, set_y, set_z, 0.003, [1000, 1000])
p = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
p = p.reshape(-1, 3)
pixels = (cam.project_world_to_pixel(p))
pixelsT = pixels.T
pixelsT = np.matmul(scale_inv, pixelsT)
pixels = pixelsT.T
print(pixels[0][0])


# ## 定义优化函数

# In[5]:


def func(xx):
    T_x, T_y, T_z,  x, y, z, w = xx
    p0x = -T_x*(-2*y**2 - 2*z**2 + 1) - T_y *         (-2*w*z + 2*x*y) - T_z*(2*w*y + 2*x*z)
    p0y = -T_x*(2*w*z + 2*x*y) - T_y*(-2*x**2 -
                                      2*z**2 + 1) - T_z*(-2*w*x + 2*y*z)
    Z_p0 = -T_x*(-2*w*y + 2*x*z) - T_y*(2*w*x + 2*y*z) -         T_z*(-2*x**2 - 2*y**2 + 1)
    pxx = -T_x*(-2*y**2 - 2*z**2 + 1) - T_y*(-2*w*z + 2*x*y) -         T_z*(2*w*y + 2*x*z) - 2*y**2 - 2*z**2 + 1
    pxy = -T_x*(2*w*z + 2*x*y) - T_y*(-2*x**2 - 2*z**2 + 1) -         T_z*(-2*w*x + 2*y*z) + 2*w*z + 2*x*y
    Z_px = -T_x*(-2*w*y + 2*x*z) - T_y*(2*w*x + 2*y*z) -         T_z*(-2*x**2 - 2*y**2 + 1) - 2*w*y + 2*x*z
    pyx = -T_x*(-2*y**2 - 2*z**2 + 1) - T_y*(-2*w*z + 2*x*y) -         T_z*(2*w*y + 2*x*z) - 2*w*z + 2*x*y
    pyy = -T_x*(2*w*z + 2*x*y) - T_y*(-2*x**2 - 2*z**2 + 1) -         T_z*(-2*w*x + 2*y*z) - 2*x**2 - 2*z**2 + 1
    Z_py = -T_x*(-2*w*y + 2*x*z) - T_y*(2*w*x + 2*y*z) -         T_z*(-2*x**2 - 2*y**2 + 1) + 2*w*x + 2*y*z
    return [p0x/Z_p0-pixels[0, 0],
            p0y/Z_p0-pixels[0, 1],
            pxx/Z_px-pixels[1, 0],
            pxy/Z_px-pixels[1, 1],
            pyx/Z_py-pixels[2, 0],
            pyy/Z_py-pixels[2, 1],
            w**2+x**2+y**2+z**2-1]


def quatans_to_degreeans(ans):
    q = Rotation.from_quat(ans[3: 7])
    euler = -q.as_euler('XYZ')
    calc_ans = np.append(ans[0:3], euler/np.pi*180)
    calc_ans = np.asarray(calc_ans)
    return calc_ans


# ## 求解

# In[6]:


xnum = 5j
ynum = 5j
total_guess = int(abs(xnum*ynum))
grid = np.mgrid[-5:5:xnum, -5:5:ynum]
gridx = grid[0]
gridy = grid[1]
gridx = np.reshape(gridx, (total_guess, 1))
gridy = np.reshape(gridy, (total_guess, 1))


# In[7]:


np.set_printoptions(precision=2, suppress=True)
lower_bound = [-5, -5, -5, -1, -1, -1, -1]
upper_bound = [5, 5, 5, 1, 1, 1, 1]
bound = scipy.optimize.Bounds(lower_bound, upper_bound)
guess = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
start = time.time()
all_ans = []
for index in range(len(gridx)):
    g1 = np.random.uniform(-5, 5, 3)
    g2 = np.random.uniform(-0.1, 0.1, 4)
    g = np.append(g1, g2)
    g[0], g[1], g[2] = gridx[index], gridy[index], 0.5

    ans = fsolve(func, g)
    # ans = scipy.optimize.root(func, guess, method='hybr')
    # ans = scipy.optimize.minimize(func, guess, bounds=bound)

    ans = quatans_to_degreeans(ans)
    if len(all_ans) == 0:
        all_ans.append(ans)
    exist_ans = False
    for old_ans in all_ans:
        if sum(abs(old_ans-ans)) < 0.1:
            exist_ans = True
            break
    if exist_ans == False:
        all_ans.append(ans)

for i in range(len(all_ans)):
    print(f'solution {i+1} : {np.round(all_ans[i],2)}')
end = time.time()
print(f'Cost {end-start} seconds, {total_guess} guesses')
print(f'The true ans is {np.round(true_ans,2)}')


# In[8]:


# clac_ans = quatans_to_degreeans(ans)
print(f'Cost {end-start} seconds')
# print(f'The true ans is {np.round(true_ans,2)}')
# print(f'The calc ans is {np.round(calc_ans,2)}')
# print(f'The error is    {np.round(calc_ans-true_ans,2)}')


# In[ ]:




