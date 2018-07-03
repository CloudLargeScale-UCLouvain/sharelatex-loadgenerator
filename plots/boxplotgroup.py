import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import json


from pylab import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes



res = {}
# files = ['raw.core.600secs.5users.0koala.5e92', 'raw.core.600secs.5users.1koala.13c7']
files = ['raw.core.600secs.5users.0koala.0b52', 'raw.edge.600secs.5users.0koala.171e']
for file in files:
    file_lab = file.split('.')[1] #core or edge
    # file_lab = 'with koala' if file.split('.')[4] == '1koala' else 'no koala'
    unique = file.split('.')[5]

    with open('../out/remote/%s' % file ) as f:
        res['%s-%s' %(file_lab,unique)] = json.load(f)

data =[]
labels = []
# filters=['update_text']
filters=['update_text', 'update_cursor_position']
for l in res:
    for k in res[l]:
        if k in filters:
            data.append(res[l][k])
            print len(res[l][k])
            labels.append('%s\n%s' % (k,l))


# fig1, ax1 = plt.subplots()
# ax1.set_title('Basic Plot')
# ax1.boxplot(data, positions=[1, 2], labels=labels)
# ax1.boxplot(data, positions=[4, 5], labels=labels)
# ax1.grid(axis='y')
# ax1.set_ylim(ymin=0)
# plt.show()


# plt.plot(range(len(data[0])), data[0], 'r-', label=labels[0])
# plt.plot(range(len(data[1])), data[1], 'b-', label=labels[1])
# leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
# plt.show()


# function for setting the colors of the box plots pairs
def setBoxColors(bp):
    setp(bp['boxes'][0], color='blue')
    setp(bp['caps'][0], color='blue')
    setp(bp['caps'][1], color='blue')
    setp(bp['whiskers'][0], color='blue')
    setp(bp['whiskers'][1], color='blue')
    # if (len(bp['fliers']) > 1):
    # setp(bp['fliers'][0], color='blue')
    # setp(bp['fliers'][1], color='blue')
    setp(bp['medians'][0], color='blue')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    # if (len(bp['fliers']) > 3):
    # setp(bp['fliers'][2], color='red')
    # setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

# Some fake data to plot
A= [[1, 2, 5],  [7, 2]]
B = [[5, 7, 2, 2, 5], [7, 2, 5]]
C = [[3,2,5,7], [6, 7, 3]]

fig = figure()
ax = axes()
# hold(True)

# first boxplot pair
bp = boxplot(data, positions = [1, 2], widths = 0.6)
setBoxColors(bp)

# # second boxplot pair
# bp = boxplot(B, positions = [4, 5], widths = 0.6)
# setBoxColors(bp)
#
# # thrid boxplot pair
# bp = boxplot(C, positions = [7, 8], widths = 0.6)
# setBoxColors(bp)

# set axes limits and labels
# xlim(0,9)
# ylim(0,9)
# ylim(ymin=0)
xlim(xmin=0)

ax.set_xticklabels(['A', 'B', 'C'])
ax.set_xticks([1.5, 4.5, 7.5])

# draw temporary red and blue lines and use them to create a legend
hB, = plot([1,1],'b-')
hR, = plot([1,1],'r-')
legend((hB, hR),('Apples', 'Oranges'))
hB.set_visible(False)
hR.set_visible(False)

show()










