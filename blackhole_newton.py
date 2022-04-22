import numpy as np
import matplotlib.pyplot as plt
from math import atan2

mass_M87 = 1e3
G = 0.007 #grav univ const
C = 3     #speed of light

dt = 0.2  #delta time

class Blackhole:
  def __init__(self):
    self.position = (0,0)
    self.mass = mass_M87
    self.radius = (2*G*self.mass)/(C**2) 
  def draw(self):
   fig, axes = plt.subplots()
   cc = plt.Circle( (0,0), self.radius, color='k')
   axes.set_aspect(1)
   axes.add_artist(cc)
   alfa = np.linspace(0,2*np.pi, 100)
  # plt.plot(self.radius*np.cos(alfa), self.radius*np.sin(alfa),'k')
   self.photon_sphere = 1.5 * self.radius
   plt.plot(self.photon_sphere*np.cos(alfa), self.photon_sphere*np.sin(alfa), 'g')

m87 = Blackhole()
m87.draw()

class Photon:
  def __init__(self, x=2, y=2):
    self.position = [x,y]
    self.theta = atan2(self.position[1], self.position[0]) #angle photon-blackhole
    self.theta_ph = 0 #angle photon-horizontal
    self.x_coords = np.array([])
    self.y_coords = np.array([])
#    plt.plot(x,y, 'yo')

  def photonSphere(self):
    dist_sqr = (self.position[0]**2 + self.position[1]**2)
    self.accel = (G * m87.mass)/(dist_sqr) 
    
    self.theta = atan2(self.position[1], self.position[0]) #angle photon-blackhole
    self.delta_theta_ph = self.accel * np.sin(self.theta_ph - self.theta) * (dt/C)
    self.theta_ph += self.delta_theta_ph

    # rotation matrix applied to position
    self.position[0] = self.position[0]*np.cos((self.delta_theta_ph)) - self.position[1]*np.sin((self.delta_theta_ph))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_ph)) + self.position[1]*np.cos((self.delta_theta_ph))

 
  def stableOrbit(self, radius):
    self.position[0] = radius*np.cos(self.theta)
    self.position[1] = radius*np.sin(self.theta)

    self.theta += 0.01
 
  def update(self):
    r_sqr = self.position[0]**2 + self.position[1]**2 

    if r_sqr < m87.radius**2:
      return 0 
    
    if r_sqr < m87.photon_sphere**2:
      self.photonSphere()
    else:
      self.stableOrbit(np.sqrt(r_sqr))

    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])
    return 1

  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'y')
    #plt.imshow((self.x_coords, self.y_coords))


beam = [Photon(0.5,y) for y in np.arange(1,3,0.06)]
for photon in beam:
  for _ in range(1000):
    photon.update()
  photon.draw()

plt.axis('equal')
plt.show()
