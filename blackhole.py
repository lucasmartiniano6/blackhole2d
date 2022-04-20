import numpy as np
import matplotlib.pyplot as plt

mass_M87 = 1e4
G = 0.001  #grav univ const
C = 3 #speed of light
dt = 0.2 #delta time

class Blackhole:
  def __init__(self):
    self.position = (0,0)
    self.mass = mass_M87
    self.radius = (2*G*self.mass)/(C**2) 
  def update(self):
   # theta = np.linspace(0,2*np.pi,50)
   # plt.plot(np.cos(theta)*self.radius,np.sin(theta)*self.radius, 'k')
   fig, axes = plt.subplots()
   cc = plt.Circle( (0,0), self.radius, color='k')
   axes.set_aspect(1)
   axes.add_artist(cc)

m87 = Blackhole()
m87.update()

class Photon:
  def __init__(self, pos=[1,3]):
    self.position = pos
    self.vel = C
    self.theta_ph = 0
    self.x_coords = np.array([])
    self.y_coords = np.array([])
  def update(self):
    if self.position[0]**2 + self.position[1]**2 < m87.radius**2:
      return 0 
    #plt.plot(self.position[0], self.position[1], 'yo')
    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])
    dist = np.sqrt(self.position[0]**2 + self.position[1]**2)
    self.theta = np.arctan(self.position[1]/self.position[0])
    self.accel = (G * m87.mass)/(dist**2)
    self.delta_theta_ph = self.accel * np.sin(self.theta_ph - self.theta) * (dt/C)
    self.theta_ph += self.delta_theta_ph
    print(self.theta_ph, self.theta)
    self.position[0] = self.position[0]*np.cos((self.delta_theta_ph)) - self.position[1]*np.sin((self.delta_theta_ph))
    self.position[1] = self.position[0]*np.sin((self.delta_theta_ph)) + self.position[1]*np.cos((self.delta_theta_ph))
    return 1
  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'y')

beam = [Photon([5,3]), Photon([5,5]), Photon([5,7]), Photon([5,9])]

for photon in beam:
  while photon.update():
    pass  
  photon.draw()

plt.axis('equal')
plt.show()
