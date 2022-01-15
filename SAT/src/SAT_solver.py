from z3 import *


def solve():
  s = Solver()

  # Definition of variables
  px = [[Bool(f"px_{i+1}_{e}") for e in range(W)] for i in range(n_blocks)]  
  py = [[Bool(f"py_{j+1}_{f}") for f in range(H)] for j in range(n_blocks)] 

  lr = [[Bool(f"lr_{i+1}_{j+1}") if i != j else 0 for j in range(n_blocks)] for i in range(n_blocks)]
  ud = [[Bool(f"ud_{i+1}_{j+1}") if i != j else 0 for j in range(n_blocks)] for i in range(n_blocks)]


  # Auxiliar functions useful for 3-literal clauses of non-overlapping constraint
  def noc_encoding_e(i, j):
    res = []
    res.append([Not(px[j][width[i] - 1])])
    for e in range(W - width[i] - 1):
      res.append([px[i][e], Not(px[j][e + width[i]])])

    res.append([px[i][W - width[i] - 1]])
    return res


  def noc_encoding_f(i, j):
    res = []
    res.append([Not(py[j][height[i] - 1])])
    for f in range(H - height[i] - 1):
      res.append([py[i][f], Not(py[j][f + height[i]])])

    res.append([py[i][H - height[i] - 1]])
    return res


  for i in range(n_blocks): 
    # Variables exceeding the constraints are set to true
    for e in range(W - width[i], W):
      s.add(px[i][e])
    for f in range(H - height[i], H):
      s.add(py[i][f])
    # Order encoding constraints
    for e in range(W - width[i]):  
      s.add(Or(Not(px[i][e]), px[i][e+1]))
    for f in range(H - height[i]):  
      s.add(Or(Not(py[i][f]), py[i][f+1]))

  # 4-literal clauses as non-overlapping constraints
  for i in range(n_blocks):  
    for j in range(n_blocks):
      if i >= j: 
        continue

      s.add(Or(lr[i][j], lr[j][i], ud[i][j], ud[j][i]))

  # 3-literal clauses as non-overlapping constraints
  for i in range(n_blocks):
    for j in range(i+1, n_blocks):
        
      for c in noc_encoding_e(i, j):
        prop = [Not(lr[i][j])] + c
        s.add(Or(prop))
        
      for c in noc_encoding_e(j, i):
        prop = [Not(lr[j][i])] + c
        s.add(Or(prop))

      for c in noc_encoding_f(i, j):
        prop = [Not(ud[i][j])] + c
        s.add(Or(prop))
        
      for c in noc_encoding_f(j, i):
        prop = [Not(ud[j][i])] + c
        s.add(Or(prop))

  # Symmetry breaking constraints:
  # With two rectangles with same height and width, the first one is forced to be
  # on the left of the other in any solution
  for i in range(n_blocks):
    for j in range(i+1, n_blocks):
      
      if width[i] == width[j] and height[i] == height[j]:
        s.add(Not(lr[j][i]))
        s.add(Or(lr[i][j], Not(ud[j][i])))

      # Additional constraints: if sum of dimension exceed max constraint,
      # they cannot be placed side by side
      if width[i] + width[j] > W:
        s.add(And(Not(lr[i][j]), Not(lr[j][i])))    
      
      if height[i] + height[j] > H:
        s.add(And(Not(ud[i][j]), Not(ud[j][i])))

  s.set('timeout', 300 * 1000)
  if s.check() == sat:
    m = s.model()
    print('Solved')
  else:
    print('Not solvable')

  return s, px, py


# Converter: SAT boolean variables are translated in cartesian coordinates
def converter_sat_coord(m, px, py):
  x_sol = []
  y_sol = [] 

  for i in range(n_blocks):
    j = 0
    while j < W:
      if m.evaluate(px[i][j]):
        x_sol.append(j)
        break
      j += 1

    j = 0
    while j < H:
      if m.evaluate(py[i][j]):
        y_sol.append(j)
        break
      j += 1

  return [x_sol, y_sol]


# Read file
import io
import math
import time
import os

for i in range(1, 41):
  file_name = "./instancesTxt/ins-" + str(i) + ".txt"
  buf = open(file_name)
  W = int(buf.readline())
  n_blocks = int(buf.readline())

  width = []
  height = []

  for line in buf:
    tmp = line.split()
    tmp = [int(x) for x in tmp]
    width.append(tmp[0])
    height.append(tmp[1])

  H = int(math.ceil(sum([width[i] * height[i] for i in range(n_blocks)]) / W))
  
  start = time.time()
  s, px, py = solve()
  end = time.time()

  print(file_name + ' ' + "{:.2f}".format(end - start))

  cornerx, cornery = converter_sat_coord(s.model(), px, py)

  print(os.getcwd())
  out_file = '../out/out-{}.txt'.format(i)
  out_buf = open(out_file, 'w')
  out_buf.write(str(W) + ' ' + str(H) + '\n')
  out_buf.write(str(n_blocks) + '\n')

  for (w, h, cx, cy) in zip(width, height, cornerx, cornery):
    out_buf.write(str(w) + ' ' + str(h) + ' ' + str(cx) + ' ' + str(cy) + '\n')
