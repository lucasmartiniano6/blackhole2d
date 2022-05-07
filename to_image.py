import blackhole

def timer(f):
  from time import time
  def wrapper(*args, **kwargs):
    t0 = time()
    val = f(*args, **kwargs)
    t1 = time()
    print(f'{f} em: {t1-t0}')
    return val
  return wrapper

@timer
def calculate():
  m87 = blackhole.Blackhole()

  cluster = [blackhole.Matter(m87) for _ in range(40)]
  for matter in cluster:
    for _ in range(1000):
      if not matter.update():
        break

  beam = [blackhole.Photon(m87) for _ in range(40)]
  for photon in beam:
    for _ in range(1000):
      if not photon.update():
        break
  return cluster, beam

def translate(value, a1, b1, a2, b2):
  # (a1,b1) -> (a2,b2)
  oldrange = abs(a1-b1)
  newrange = abs(a2-b2)

  newvalue = (((value - a1) * newrange) / oldrange) + a2
  return int(round(newvalue, 3))

@timer
def normalizeRange(cluster, beam, img_size=1000):
  YELLOW = 250
  GREY = 100
  
  import numpy as np
  img = np.zeros((img_size,img_size))

  for matter in cluster:
    for x,y in zip(matter.x_coords, matter.y_coords):
      norm_x = translate(x, -5,5, 0, img_size)
      norm_y = translate(y, -5,5, 0, img_size)
      img[norm_x, norm_y] = GREY

  for photon in beam:
    for x,y in zip(photon.x_coords, photon.y_coords):
      norm_x = translate(x, -5,5, 0, img_size)
      norm_y = translate(y, -5,5, 0, img_size)
      img[norm_x, norm_y] = YELLOW
  return img

if __name__ == '__main__':
  cluster, beam = calculate()
  img = normalizeRange(cluster, beam)
  import matplotlib.pyplot as plt
  plt.imshow(img, cmap='hot')
  plt.show()
