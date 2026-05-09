import numpy as np
import math

p_0 = np.array([0, 0])
v0_mag = 2          
theta_deg = 30      
v_0 = v0_mag * np.array([math.cos(theta_deg), -math.sin(theta_deg)])
dt = 0.2

N = 20000
for pas in range(N):
    p = p_0 + v_0 * dt
    p_0 = p
    print(f"pas={pas}, p={p}")
