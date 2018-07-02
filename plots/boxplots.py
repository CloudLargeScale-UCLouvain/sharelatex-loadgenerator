import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import json

res = {}
files = ['raw.core.600secs.5users.0koala.5e92', 'raw.core.600secs.5users.1koala.13c7']
for file in files:
    # file_lab = file.split('.')[1] #core or edge
    unique = file.split('.')[5]
    file_lab = 'with koala' if file.split('.')[4] == '1koala' else 'no koala'
    with open('../out/%s' % file ) as f:
        res['%s-%s' %(file_lab,unique)] = json.load(f)

data =[]
labels = []
# filters=['update_text']
filters=['update_cursor_position']
for l in res:
    for k in res[l]:
        if k in filters:
            data.append(res[l][k])
            print len(res[l][k])
            labels.append('%s\n%s' % (k,l))


fig1, ax1 = plt.subplots()
ax1.set_title('Basic Plot')
ax1.boxplot(data, labels=labels)
ax1.grid(axis='y')
ax1.set_ylim(ymin=0)
plt.show()


# plt.plot(range(len(data[0])), data[0], 'r-', label=labels[0])
# plt.plot(range(len(data[1])), data[1], 'b-', label=labels[1])
# leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
# plt.show()