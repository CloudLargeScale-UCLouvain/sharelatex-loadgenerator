import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json


files = ['../out/raw.localhost.localhost.u1.a420', '../out/raw.localhost.localhost.u2.15e3']
start = 0
fig, ax = plt.subplots()
for file in files:
       with open(file, "r") as f:
              print('lesh presh')
              content = f.read()
              jsonData = json.loads(content)


              y = jsonData['update_text'] #[3,4,4]
              x = np.arange(start, start + len(y))

              ax.plot(x, y)
              start = len(y)


ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
                     title='About as simple as it gets, folks')
ax.grid()

plt.show()