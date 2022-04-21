import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm

mass_M87 = 1000
G = 0.007  #grav univ const
C = 3 #speed of light

dt = 0.4 #delta time

class Blackhole:
  def __init__(self):
    self.position = (0,0)
    self.mass = mass_M87
    self.radius = (2*G*self.mass)/(C**2) 
    print(self.radius)
  def update(self):
   fig, axes = plt.subplots()
   cc = plt.Circle( (0,0), self.radius, color='k')
   axes.set_aspect(1)
   axes.add_artist(cc)

m87 = Blackhole()
m87.update()

class Photon:
  def __init__(self, pos=[1,3]):
    self.position = pos
    self.theta_ph = 0
    self.x_coords = np.array([])
    self.y_coords = np.array([])
  def update(self):
    if self.position[0]**2 + self.position[1]**2 < m87.radius**2:
      return 0 
    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])
    
    dist_sqr = (self.position[0]**2 + self.position[1]**2)
    self.accel = (G * m87.mass)/(dist_sqr)

    self.theta = math.atan2(self.position[1], self.position[0])
    self.delta_theta_ph = self.accel * np.sin(self.theta_ph - self.theta) * (dt/C)
    self.theta_ph += self.delta_theta_ph

    self.position[0] = self.position[0]*np.cos((self.delta_theta_ph)) - self.position[1]*np.sin((self.delta_theta_ph))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_ph)) + self.position[1]*np.cos((self.delta_theta_ph))

    return 1

  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'y')


beam = [Photon([-2,2])]
for photon in beam:
  while photon.update():
    pass
  photon.draw()

plt.axis('equal')
plt.show()
