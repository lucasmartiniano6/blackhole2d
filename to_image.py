#!/usr/bin/env python3
import blackhole
import numpy as np
from tqdm import tqdm

RE_CALCULATE = False

def timer(f):
  from time import perf_counter
  def wrapper(*args, **kwargs):
    t0 = perf_counter()
    val = f(*args, **kwargs)
    t1 = perf_counter()
    print(f'function <{f.__name__}> : {t1-t0}')
    return val
  return wrapper

@timer
def calculate():
  m87 = blackhole.Blackhole()

  cluster = [blackhole.Matter(m87) for _ in range(1000)]
  for matter in tqdm(cluster):
    for _ in range(900):
      if not matter.update():
        break

  beam = [blackhole.Photon(m87) for _ in range(80)]
  for photon in tqdm(beam):
    for _ in range(850):
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
def normalizeRange(cluster, beam, img_size=1500):
  MATTER_CLR = 0.7
  PHOTON_CLR = 1
  
  import numpy as np
  img = np.zeros((img_size,img_size))

  for matter in tqdm(cluster):
    for x,y in zip(matter.x_coords, matter.y_coords):
      norm_x = translate(x, -5,5, 0, img_size)
      norm_y = translate(y, -5,5, 0, img_size)
      img[norm_x, norm_y] = MATTER_CLR

  for photon in tqdm(beam):
    for x,y in zip(photon.x_coords, photon.y_coords):
      norm_x = translate(x, -5,5, 0, img_size)
      norm_y = translate(y, -5,5, 0, img_size)
      img[norm_x, norm_y] = PHOTON_CLR
  return img

def createNpz():
  cluster, beam = calculate()
  img = normalizeRange(cluster, beam)
  np.savez('processed_img.npz', img)
  print('Created file: processed_img.npz')

def loadNpz():
  img = np.load('processed_img.npz')['arr_0']
  print('Loaded file: <processed_img.npz>')
  return img

if __name__ == '__main__':
  import matplotlib.pyplot as plt
  if RE_CALCULATE:
    createNpz()
  img = loadNpz()
  plt.imshow(img, cmap='hot')
  plt.show()
