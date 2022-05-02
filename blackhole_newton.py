import numpy as np 
import matplotlib.pyplot as plt
from math import atan2
import random

mass_M87 = 1e3
G = 0.007 #grav univ const
C = 3     #speed of light

dt = 0.3  #delta time

class Blackhole:
  def __init__(self):
    self.position = (0,0)
    self.mass = mass_M87
    self.radius = (2*G*self.mass)/(C**2) 
  def draw(self):
   fig, axes = plt.subplots()
   event_horizon = plt.Circle( (0,0), self.radius, color='k')
   axes.set_aspect(1)
   axes.add_artist(event_horizon)

   alfa = np.linspace(0,2*np.pi, 100)

   self.photon_sphere = 1.5 * self.radius
   plt.plot(self.photon_sphere*np.cos(alfa), self.photon_sphere*np.sin(alfa), 'g')

   self.matter_sphere = 3 * self.radius
   plt.plot(self.matter_sphere*np.cos(alfa), self.matter_sphere*np.sin(alfa), 'g')

m87 = Blackhole()
m87.draw()

class Matter:
  def __init__(self, x=-m87.matter_sphere, y=1):
    self.position = [x,y]
    self.theta = atan2(self.position[1], self.position[0])
    self.theta_mh = 0
    self.delta_theta_mh = 0

    self.x_coords = np.array([])
    self.y_coords = np.array([])
  def matterOrbit(self, radius):
    self.position[0] = radius*np.cos(self.theta)
    self.position[1] = radius*np.sin(self.theta)

    self.theta += 0.01

    # random rotations matter-horizontal in orbit
    if not self.delta_theta_mh:
      self.delta_theta_mh = random.uniform(0, np.pi/32)

    self.position[0] = self.position[0]*np.cos((self.delta_theta_mh)) - self.position[1]*np.sin((self.delta_theta_mh))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_mh)) + self.position[1]*np.cos((self.delta_theta_mh))

  def suckedIn(self):
    dist_sqr = (self.position[0]**2 + self.position[1]**2)
    self.accel = (G * m87.mass)/(dist_sqr) 
    
    self.theta = atan2(self.position[1], self.position[0]) 
    self.delta_theta_mh = self.accel * np.sin(self.theta_mh - self.theta) * (dt/C)
    self.theta_mh += self.delta_theta_mh

    # rotation matrix
    self.position[0] = self.position[0]*np.cos((self.delta_theta_mh)) - self.position[1]*np.sin((self.delta_theta_mh))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_mh)) + self.position[1]*np.cos((self.delta_theta_mh))

  def update(self):
    r_sqr = self.position[0]**2 + self.position[1]**2

    if r_sqr >= m87.matter_sphere**2:
      # outside matter orbit
      self.matterOrbit(np.sqrt(r_sqr))
    elif r_sqr < m87.radius**2:
      # inside event horizon
      return False
    else:
      pass
      #self.suckedIn() 

    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])
    return True
  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'k')
    plt.plot(self.position[0], self.position[1], 'ro')

cluster = [Matter() for _ in range(3)]
for matter in cluster:
  for _ in range(1000):
    if not matter.update():
      break
  matter.draw()


class Photon:
  def __init__(self, x=-1, y=m87.photon_sphere+0.2):
    self.position = [x,y]
    self.theta = atan2(self.position[1], self.position[0]) #angle photon-blackhole
    self.theta_ph = 0 #angle photon-horizontal
    self.delta_theta_ph = 0
    self.x_coords = np.array([])
    self.y_coords = np.array([])
    #plt.plot(x,y,'yo')

  def photonSphere(self):
    dist_sqr = (self.position[0]**2 + self.position[1]**2)
    self.accel = (G * m87.mass)/(dist_sqr) 
    
    self.theta = atan2(self.position[1], self.position[0]) 
    self.delta_theta_ph = self.accel * np.sin(self.theta_ph - self.theta) * (dt/C)
    self.theta_ph += self.delta_theta_ph

    # rotation matrix
    self.position[0] = self.position[0]*np.cos((self.delta_theta_ph)) - self.position[1]*np.sin((self.delta_theta_ph))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_ph)) + self.position[1]*np.cos((self.delta_theta_ph))

 
  def unstableOrbit(self, radius):
    self.position[0] = radius*np.cos(self.theta)
    self.position[1] = radius*np.sin(self.theta)

    self.theta += 0.01

    # random rotations photon-horizontal in orbit
    if not self.delta_theta_ph:
      self.delta_theta_ph = random.uniform(0, np.pi/64)

    self.position[0] = self.position[0]*np.cos((self.delta_theta_ph)) - self.position[1]*np.sin((self.delta_theta_ph))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_ph)) + self.position[1]*np.cos((self.delta_theta_ph))

  
  def update(self):
    if self.position[0] > m87.radius+10 or self.position[0] < m87.radius-10:
      return False
    if self.position[1] > m87.radius+10 or self.position[1] < m87.radius-10:
      return False

    r_sqr = self.position[0]**2 + self.position[1]**2 

    if r_sqr < m87.radius**2:
      # inside event horizon
      return False
    
    if r_sqr < m87.photon_sphere**2:
      # inside photon sphere
      self.photonSphere()
    else:
      # outside photon sphere
      self.unstableOrbit(np.sqrt(r_sqr))

    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])
    return True

  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'y')
#    plt.plot(self.position[0], self.position[1], 'ro')

beam = [Photon() for _ in range(10)]
for photon in beam:
  for _ in range(1000):
    if not photon.update():
      break
  photon.draw()

plt.axis('equal')
plt.show()
