import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json


# files = ['../out/raw.localhost.localhost.u1.7bc2'
#          ,'../out/raw.localhost.localhost.u1.9e77'
#          ,'../out/raw.localhost.localhost.u1.86f5'
#         ]

# files = ['../out/test1/raw.edge1.edge1.u1.589e'
#          ,'../out/test1/raw.edge1.edge1.u1.8d54'
#          ,'../out/test1/raw.edge1.edge3.u1.c1a1'
#          ,'../out/test1/raw.edge1.edge3.u1.8ca7'
#          ,'../out/test1/raw.edge1.edge4.u1.71fd'
#          ,'../out/test1/raw.edge1.edge4.u1.0205'
#         ]



# files = [
# '../out/test1/raw.edge1.edge1.u2.94c9'
# ,'../out/test1/raw.edge1.edge1.u2.dbce'
# ,'../out/test1/raw.edge1.edge3.u2.032b'
# ,'../out/test1/raw.edge1.edge3.u2.b119'
# ,'../out/test1/raw.edge1.edge4.u2.e1e6'
# ,'../out/test1/raw.edge1.edge4.u2.eac6'
# ]

# files = [
# '../out/raw.edge1.edge1.u1.1.0b04'
# ,'../out/raw.edge1.edge1.u1.2.5052'
# ,'../out/raw.edge1.edge3.u1.1.690a'
# ,'../out/raw.edge1.edge3.u1.2.a886'
# ,'../out/raw.edge1.edge4.u1.1.16a8'
# ,'../out/raw.edge1.edge4.u1.2.a251'
# ]

# files = [
# '../out/raw.edge1.edge1.u1.1.867a'
# ,'../out/raw.edge1.edge1.u1.2.f480'
# ,'../out/raw.edge1.edge3.u1.1.c0f5'
# ,'../out/raw.edge1.edge3.u1.2.6898'
# ,'../out/raw.edge1.edge4.u1.1.4934'
# ,'../out/raw.edge1.edge4.u1.2.93c1'
# ]

# files = [
# '../out/test4/raw.edge1.edge1.u1.1.4721'
# ,'../out/test4/raw.edge1.edge1.u1.2.5e3e'
# ,'../out/test4/raw.edge1.edge3.u1.1.8e7f'
# ,'../out/test4/raw.edge1.edge3.u1.2.7008'
# ,'../out/test4/raw.edge1.edge4.u1.1.dd65'
# ,'../out/test4/raw.edge1.edge4.u1.2.9257'
# ]

files=[
'../out/raw.edge1.edge3.u1.1.f7af'
]

start = 0
lasty = None
fig, ax = plt.subplots()
for file in files:
       with open(file, "r") as f:
              content = f.read()
              jsonData = json.loads(content)


              y = jsonData['update_text'] #[3,4,4]
              if (lasty): y.insert(0,lasty)
              x = np.arange(start, start + len(y))
              # print(x)
              lasty = y[-1]
              ax.plot(x, y)
              start += len(y)-1


ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.set(xlabel='Time', ylabel='Latency (ms)',
                     title='Title')
ax.grid()

plt.show()