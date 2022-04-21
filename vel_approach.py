import numpy as np
import matplotlib.pyplot as plt
import math

mass_M87 = 1e4
G = 0.001  #grav univ const
C = 3 #speed of light
dt = 0.01 #delta time

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
    self.x_coords = np.array([])
    self.y_coords = np.array([])
    self.position = pos
    self.vel_x = C
    self.vel_y = 0
  def update(self):
    if self.position[0]**2 + self.position[1]**2 < m87.radius**2:
      return 0 
    self.x_coords = np.append(self.x_coords, self.position[0])
    self.y_coords = np.append(self.y_coords, self.position[1])

    dist_sqr = (self.position[0]**2 + self.position[1]**2)
    self.accel = (G * m87.mass)/(dist_sqr)

    self.theta = math.atan2(self.position[1], self.position[0])

    self.accel_x =  self.accel * np.cos(self.theta)
    self.accel_y =  self.accel * np.sin(self.theta)

    if self.position[0] > 0 and self.accel_x > 0:
      self.accel_x *= -1
    if self.position[0] < 0 and self.accel_x < 0:
      self.accel_x *= -1
    if self.position[1] > 0 and self.accel_y > 0:
      self.accel_y *= -1
    if self.position[1] < 0 and self.accel_y < 0:
      self.accel_y *= -1

    if abs(self.vel_x) < C:
      self.vel_x += self.accel_x * dt
    if abs(self.vel_y) < C:
      self.vel_y += self.accel_y * dt

    self.position[0] += self.vel_x * dt
    self.position[1] += self.vel_y * dt
    
    if self.position[0] > 0:
      print('X IS BIGGER THAN 0')
    if self.position[1] < 0:
      print('Y IS LESS THAN 0')
    print('Angle', (self.theta*180)/np.pi)
    print('Accel', self.accel_x, self.accel_y)
    print('Vel  ', self.vel_x, self.vel_y)  
    return 1

  def draw(self):
    plt.plot(self.x_coords, self.y_coords, 'y')

beam = [Photon([-2.5,3])]
for photon in beam:
  for _ in range(500):
    photon.update()
  photon.draw()

plt.axis('equal')
plt.show()
