import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json


file = '../out/projects/out'


start = 0
lasty = None
fig, ax = plt.subplots()
data={}
first = 0

i=0
with open(file, "r") as f:
    content = f.read()
    lines = content.split('\n')
    for line in lines:
        words = line.split(' ')
        if len(words) != 3: continue
        loc = words[1].strip('(').strip(')')
        if loc not in data:
            data[loc] = {'x':[], 'y':[], 'i':i}
            i += 0.01

with open(file, "r") as f:
    content = f.read()
    lines = content.split('\n')
    for line in lines:
        words = line.split(' ')
        if len(words) != 3: continue
        time = int(words[0][:-4])
        if first == 0:
            first = time
        time -= first
        loc = words[1].strip('(').strip(')')
        count = int(words[2])

        # data[loc]['x'].append(time)
        # data[loc]['y'].append(count)

        for k, v in data.items():
            data[k]['x'].append(time)

            if len(data[k]['y']) == 0:
                data[k]['y'].append(0) if k != 'core' else data[k]['y'].append(10)
            else:
                data[k]['y'].append(data[k]['y'][-1])
            if k == loc:
                data[k]['x'].append(time)
                data[loc]['y'].append(count+data[loc]['i'])


for k,v in data.items():
    print(k)
    ax.plot(v['x'], v['y'],linewidth=3.0)
    # ax.scatter(v['x'], v['y'])

ax.legend(data.keys())

# print(data)

ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.set(xlabel='Time (s)', ylabel='# projects',
                     title='Title')
ax.grid()

plt.show()