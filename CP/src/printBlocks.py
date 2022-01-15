import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np
import random


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def random_color():
    rgbl = [255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


def retrive_data(file_name):
    buf = open(file_name)
    total_res = {}
    total_dim = buf.readline().split()
    total_res['max_width'] = int(total_dim[0])
    total_res['max_height'] = int(total_dim[1])
    n_blocks = buf.readline()
    total_res['n_blocks'] = int(n_blocks)

    widths = []
    heights = []
    cornerx = []
    cornery = []
    for line in buf:
        tmp = line.split()
        tmp = [int(x) for x in tmp]
        widths.append(tmp[0])
        heights.append(tmp[1])
        cornerx.append(tmp[2])
        cornery.append(tmp[3])

    total_res['widths'] = widths
    total_res['heights'] = heights
    total_res['cornerx'] = cornerx
    total_res['cornery'] = cornery
    buf.close()

    return total_res


file_name = '../out/ins-{}.txt'.format(2)
data = retrive_data(file_name)

n_blocks = data['n_blocks']

heights = data['heights']
widths = data['widths']

cornerx = data['cornerx']
cornery = data['cornery']

print(cornerx)
print(cornery)

max_width = data['max_width']
max_height = data['max_height']

rects = []
for w, h in zip(widths, heights):
    rects.append([w, h])

corners = []
for cx, cy in zip(cornerx, cornery):
    corners.append([cx, cy])

cmap = get_cmap(n_blocks)

rectAll = patches.Rectangle((0, 0), width=max_width, height=max_height, edgecolor="r", fill=False)
rect = []

for i in range(0, len(rects)):
    rect.append(patches.Rectangle((cornerx[i], cornery[i]), width=widths[i], height=heights[i], facecolor=cmap(i), edgecolor='black'))

fig, ax = plt.subplots()
ax.add_patch(rectAll)
for x in rect:
    ax.add_patch(x)
ax.set_xlim([0, max_width+2])
ax.set_ylim([0, max_height+2])
ticksx = np.arange(0, max_width + 1, 1)
ticksy = np.arange(0, max_height + 1, 1)
ax.set_xticks(ticksx)
ax.set_yticks(ticksy)
plt.grid()
plt.show()
