from z3 import *
import math
import time
import itertools
import io
import math
import time
from datetime import datetime


def solve():

    start_time = time.time()
    s = Optimize()
    s.set("timeout", 300 * 1000)

    x = [Int(f"x_{i}") for i in range(n_blocks)]
    y = [Int(f"y_{i}") for i in range(n_blocks)]

    # Variables needed for the non-overlap constraint without the logical or
    '''
    xb = [[Int(f'boolx_{i}_{j}') for i in range(n_blocks)] for j in range(n_blocks)]
    yb = [[Int(f'booly_{i}_{j}') for i in range(n_blocks)] for j in range(n_blocks)]
    '''

    W = max_width
    H = min_pos_area

    max_height = Int('max_height')

    s.add(max_height == min_pos_area)

    for i in range(n_blocks):
        s.add(x[i] + width[i] <= max_width)
        s.add(y[i] + height[i] <= max_height)
        s.add(x[i] >= 0)
        s.add(y[i] >= 0)


    for i in range(n_blocks):
        for j in range(i, n_blocks):
            if i != j:
                # non overlap constraint with logical or
                s.add(Or(Or(x[i] + width[i] <= x[j], x[i] >= x[j] + width[j]),Or(y[i] + height[i] <= y[j], y[i] >= y[j] + height[j])))

    '''
    #non overlap constraint without logcial or and symmetry breaking constraints
    for i in range(n_blocks):
        for j in range(n_blocks):
            if i >= j:
                continue
            # x,y booleans
            s.add(xb[i][j] >= 0)
            s.add(xb[i][j] <= 1)
            s.add(yb[i][j] >= 0)
            s.add(yb[i][j] <= 1)
            
            #non overlap constraints without logical or
            s.add(x[i] + width[i] <= x[j] + W * (xb[i][j] + yb[i][j]))
            s.add(x[i] - width[j] >= x[j] - W * (1 - xb[i][j] + yb[i][j]))
            s.add(y[i] + height[i] <= y[j] + H * (1 + xb[i][j] - yb[i][j]))
            s.add(y[i] - height[j] >= y[j] - H * (2 - xb[i][j] - yb[i][j]))
            
            #symmetry breaking constraint
            s.add(Implies(And(width[i] == width[j],height[i] == height[j]),And(x[i] <= x[j], Implies(x[i] == x[j], y[i] <= y[j]))))
            s.add(Implies(width[i] + width[j] > W,And(x[i]+width[i]>x[j],x[j]+width[j]>x[i])))
            s.add(Implies(height[i] + height[j] > H,And(y[i]+height[i]>y[j],y[j]+height[j]>y[i])))
    '''
    s.minimize(max_height)

    if s.check() == sat:
        print('Solved')
    else:
        print('UNSAT')
        return -1,-1,-1

    return s,x,y

for i in range(1,41):
    file_name = "./../instances/ins-" + str(i) + ".txt"
    buf = open(file_name)
    max_width = int(buf.readline())
    n_blocks = int(buf.readline())

    width = []
    height = []

    for line in buf:
        tmp = line.split()
        tmp = [int(x) for x in tmp]
        width.append(tmp[0])
        height.append(tmp[1])

    blocks = []
    for j, k in zip(width, height):
        blocks.append([j, k])

    area = sum([b[0] * b[1] for b in blocks])
    min_pos_area = math.ceil(area / max_width)

    start = time.time()
    s, px, py = solve()
    end = time.time()
    # Search strategy and check if the timeout is passed
    while s == -1 and (end - start) < 300:
        min_pos_area = min_pos_area + 1
        print("Try with an higher value\n")
        s, px, py = solve()
        end = time.time()
    if s != -1:
        m = s.model()
        file_out = "./../out/out-" + str(i) + ".txt"

        with open(file_out, 'w') as file:

            result = sorted([(d, m[d]) for d in m], key=lambda x: str(x[0]))
            file.write(str(max_width) + ' ' + str(min_pos_area) + "\n")
            file.write(str(n_blocks)+'\n')
            for k in range(1,n_blocks+1):
                file.write(str(width[k-1]) + ' ' + str(height[k-1]) + ' ' + str(m.evaluate(px[k-1])) + ' ' + str(m.evaluate(py[k-1])) + "\n")


