import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cbook as cbook
import json
import pylab
from matplotlib.font_manager import FontProperties

def main():

    # files = [
    #      'remote/exp2-2/raw.core.600secs.5users.1koala.adfb'
    #     ,'remote/exp2-2/raw.core.600secs.5users.1koala.d3b9'
    #      ]

    # files = [
    #      'remote/exp2-2_new/raw.core.600secs.5users.1koala.9fce'
    #     ,'remote/exp2-2_new/raw.core.600secs.5users.1koala.a87a'
    #      ]

    # files = [
    #      'remote/exp2-2_new2/raw.core.600secs.5users.1koala.946d'
    #     ,'remote/exp2-2_new2/raw.core.600secs.5users.1koala.8210'
    #      ]

    files = [
         'grid5k/exp2/raw.core.600secs.5users.1koala.6c36'
        ,'grid5k/exp2/raw.core.600secs.5users.1koala.a933'
         ]

    filters=['update_text']
    data00,lbs = get_data(files, filters)

    filters=['update_cursor_position']
    data01,lbs = get_data(files, filters)

    filters=['check_spelling']
    data02,lbs = get_data(files, filters)

    filters=['receive_chat_message']
    data03,lbs = get_data(files, filters)

    # files = ['remote/exp2-2/raw.core.1800secs.2users.1koala.9378'
    #         ,'remote/exp2-2/raw.core.1800secs.2users.1koala.20f2'
    # ]

    # files = ['remote/exp2-2_new/raw.core.1800secs.2users.1koala.62b2'
    #         ,'remote/exp2-2_new/raw.core.1800secs.2users.1koala.c2b4'
    # ]

    # files = ['remote/exp2-2_new2/raw.core.1800secs.2users.1koala.7e03'
    #         ,'remote/exp2-2_new2/raw.core.1800secs.2users.1koala.0d09'
    # ]

    # files = ['remote/exp2-2_compile/raw.core.1800secs.2users.1koala.f7e6'
    #         ,'remote/exp2-2_compile/raw.core.1800secs.2users.1koala.903d'
    # ]

    files = ['grid5k/exp2/raw.core.1800secs.2users.1koala.45d8'
            ,'grid5k/exp2/raw.core.1800secs.2users.1koala.2c90'
    ]

    filters=['full_compile']
    data04,lbs = get_data(files, filters)

    filters=['document_diff']
    data05,lbs = get_data(files, filters)

    #from edge1
    # files = ['remote/exp2-2/raw.edge.600secs.5users.1koala.52a0'
    #          ,'remote/exp2-2/raw.edge.600secs.5users.1koala.3292'
    #          ]

    # files = ['remote/exp2-2_new2/raw.edge.600secs.5users.1koala.418a'
    #          ,'remote/exp2-2_new2/raw.edge.600secs.5users.1koala.3502'
    #          ]

    files = ['grid5k/exp2/raw.edge.600secs.5users.1koala.3275'
            ,'grid5k/exp2/raw.edge.600secs.5users.1koala.9dce'
             ]

    filters=['update_text']
    data10, lbs = get_data(files, filters)

    filters=['update_cursor_position']
    data11,lbs = get_data(files, filters)

    filters=['check_spelling']
    data12,lbs = get_data(files, filters)

    filters=['receive_chat_message']
    data13,lbs = get_data(files, filters)

    # files = ['remote/exp2-2/raw.edge.1800secs.2users.1koala.c59a'
    #         ,'remote/exp2-2/raw.edge.1800secs.2users.1koala.0926'
    # ]

    # files = ['remote/exp2-2_new2/raw.edge.1800secs.2users.1koala.6d00'
    #         ,'remote/exp2-2_new2/raw.edge.1800secs.2users.1koala.c7b7'
    # ]

    # files = ['remote/exp2-2_compile/raw.edge.1800secs.2users.1koala.72a9'
    #         ,'remote/exp2-2_compile/raw.edge.1800secs.2users.1koala.3eda'
    # ]

    files = ['grid5k/exp2/raw.edge.1800secs.2users.1koala.4901'
            ,'grid5k/exp2/raw.edge.1800secs.2users.1koala.5ff4'
    ]

    filters=['full_compile']
    data14,lbs = get_data(files, filters)

    filters=['document_diff']
    data15,lbs = get_data(files, filters)


    # files = [
    #          'remote/exp2-2/raw.edge.600secs.5users.1koala.db52'
    #         ,'remote/exp2-2/raw.edge.600secs.5users.1koala.4583'
    #          ]

    # files = [
    #          'remote/exp2-2_new/raw.edge.600secs.5users.1koala.862e'
    #         ,'remote/exp2-2_new/raw.edge.600secs.5users.1koala.2262'
    #          ]

    # files = [
    #          'remote/exp2-2_new2/raw.edge.600secs.5users.1koala.cde6'
    #         ,'remote/exp2-2_new2/raw.edge.600secs.5users.1koala.4e98'
    #          ]

    files = [
             'grid5k/exp2/raw.edge.600secs.5users.1koala.ac27'
            ,'grid5k/exp2/raw.edge.600secs.5users.1koala.8fb9'
             ]

    filters=['update_text']
    data20,lbs = get_data(files, filters)

    filters=['update_cursor_position']
    data21,lbs = get_data(files, filters)

    filters=['check_spelling']
    data22,lbs = get_data(files, filters)

    filters=['receive_chat_message']
    data23,lbs = get_data(files, filters)



    # files = ['remote/exp2-2/raw.edge.1800secs.2users.1koala.821b'
    #         ,'remote/exp2-2/raw.edge.1800secs.2users.1koala.1069'
    # ]

    # files = ['remote/exp2-2_new/raw.edge.1800secs.2users.1koala.5c6e'
    #         ,'remote/exp2-2_new/raw.edge.1800secs.2users.1koala.652b'
    # ]

    # files = ['remote/exp2-2_new2/raw.edge.1800secs.2users.1koala.edbf'
    #         ,'remote/exp2-2_new2/raw.edge.1800secs.2users.1koala.d10b'
    # ]

    # files = ['remote/exp2-2_compile/raw.edge.1800secs.2users.1koala.b457'
    #         ,'remote/exp2-2_compile/raw.edge.1800secs.2users.1koala.0dc9'
    # ]

    files = ['grid5k/exp2/raw.edge.1800secs.2users.1koala.5899'
            ,'grid5k/exp2/raw.edge.1800secs.2users.1koala.48be'
    ]

    filters=['full_compile']
    data24,lbs = get_data(files, filters)

    filters=['document_diff']
    data25,lbs = get_data(files, filters)


    # titles=[['Update text','Update cursor','Spelling'],['Chat','Compile','History'] ]
    titles = [['Update text', 'Chat'], ['Update cursor','Compile'], ['Spelling','History'] ]
    # data = [[
    #         [data00,data10,data20],
    #         [data01,data11,data21],
    #         [data02,data12,data22],
    #         ],
    #         [
    #         [data03,data13,data23],
    #         [data04,data14,data24],
    #         [data05,data15,data25],
    #         ]
    #         ]
    data = [[
            [data00,data10,data20],
            [data03,data13,data23]
            ],
            [
            [data01,data11,data21],
            [data04,data14,data24],
            ],
            [
            [data02,data12,data22],
            [data05,data15,data25],
            ]

            ]

    fliers = False
    rows = 3
    cols = 2
    # fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(8, 6))
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(4, 8))
    boxprops = dict( color='red')

    color1 = '#D7191C'
    color2 = '#2C7BB6'
    font = {'family': 'serif', 'weight': 'normal', 'size': 11}

    for i in range(rows):
        for j in range(cols):
            axes[i][j].set_title(titles[i][j],fontdict=font)

            bp = axes[i][j].boxplot(data[i][j][0], positions=[1,2], showfliers=fliers, widths=0.5,  )
            paint(bp, color1, color2)
            bp = axes[i][j].boxplot(data[i][j][1], positions=[6,7], showfliers=fliers, widths=0.5)
            paint(bp, color1, color2)
            bp = axes[i][j].boxplot(data[i][j][2], positions=[11,12], showfliers=fliers, widths=0.5)
            paint(bp, color1, color2)

            axes[i][j].set_xticklabels(['core', 'edge1', 'edge2'], rotation=20,fontdict=font)
            axes[i][j].set_xticks([1.5, 6.5, 11.5])
            axes[i][j].set_xlim(0,13)
            # axes[i][j].set_ylim(ymin=0)

            start, end = axes[i,j].get_ylim()
            step = 20
            if titles[i][j] == 'Spelling': step = 10
            if titles[i][j] == 'Chat': step = 50
            if titles[i][j] == 'Compile': step = 250
            if titles[i][j] == 'History': step = 100
            axes[i,j].set_yticks(np.arange(0, end, step))

        axes[i,0].set_ylabel('Latency (ms)',fontdict=font)


    setlegend(axes[0][1], color1, color2,font)
    # fontP = FontProperties()
    # fontP.set_size('small')
    # pylab.legend([plt], "title", prop=fontP)

    fig.subplots_adjust(hspace=0.4, wspace=0.5)
    plt.show()


    # plt.plot(range(len(data[0])), data[0], 'r-', label=labels[0])
    # plt.plot(range(len(data[1])), data[1], 'b-', label=labels[1])
    # leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
    # plt.show()

def paint(bp, color1, color2):
    pylab.setp(bp['boxes'][0], color=color1)
    pylab.setp(bp['caps'][0], color=color1)
    pylab.setp(bp['caps'][1], color=color1)
    pylab.setp(bp['whiskers'][0], color=color1)
    pylab.setp(bp['whiskers'][1], color=color1)
    pylab.setp(bp['medians'][0], color=color1)

    pylab.setp(bp['boxes'][1], color=color2)
    pylab.setp(bp['caps'][2], color=color2)
    pylab.setp(bp['caps'][3], color=color2)
    pylab.setp(bp['whiskers'][2], color=color2)
    pylab.setp(bp['whiskers'][3], color=color2)
    pylab.setp(bp['medians'][1], color=color2)

def setlegend(axes, color1, color2, font):
    hB, = pylab.plot([1,1],color1)
    hR, = pylab.plot([1,1],color2)
    # axes.legend((hB, hR),('project "Core"', 'project "Edge" '),loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=2)
    mpl.rc('font', **font)
    axes.legend((hB, hR),('project "Core"', 'project "Edge" '),loc='upper center', bbox_to_anchor=(-0.25, 1.40), ncol=2)
    hB.set_visible(False)
    hR.set_visible(False)

def get_data(files, filters):
    res = {}
    ids = []
    for file in files:
        file_lab = file.split('.')[1] #core or edge
        # file_lab = 'with koala' if file.split('.')[4] == '1koala' else 'no koala'
        unique = file.split('.')[5]
        with open('../out/%s' % file ) as f:
            res['%s-%s' %(file_lab,unique)] = json.load(f)
            ids.append('%s-%s' %(file_lab,unique))


    data =[]
    labels = []
    for l in ids:
        for k in res[l]:
            if k in filters:
                data.append(res[l][k])
                # print len(res[l][k])
                labels.append('%s\n%s' % (k,l))

    return data, labels


main()











