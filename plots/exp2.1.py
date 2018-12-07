import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import json


def main():

    # files = ['raw.core.600secs.5users.0koala.5e92', 'raw.core.600secs.5users.1koala.13c7'] #koala overhead
    # files = ['remote/raw.core.600secs.5users.0koala.0b52', 'remote/raw.edge.600secs.5users.0koala.171e'] #edge/core 20 ms update_text
    # files = ['remote/raw.core.600secs.5users.1koala.1eaa','remote/raw.edge.600secs.5users.0koala.80c3'] #edge/core 50 ms update_text
    # files = ['remote/exp2/raw.edge.600secs.2users.1koala.2139' #edge 1 #core project first run
    #          ,'remote/exp2/raw.edge.600secs.2users.1koala.4225'  #edge 2
    #          ,'remote/exp2/raw.core.600secs.2users.1koala.b05d'  #core
    #          ] #edge/core 50 ms update_text

    files = ['remote/exp2/raw.edge.600secs.2users.1koala.b846' #core project
            ,'remote/exp2/raw.edge.600secs.2users.1koala.d178'
            ,'remote/exp2/raw.core.600secs.2users.1koala.3a1a'
             ]

    #files = ['remote/raw.core.1800secs.2users.1koala.7058','remote/raw.edge.1800secs.2users.1koala.bb8c'] #compile

    filters=['update_text']
    data00,labels00 = get_data(files, filters)

    filters=['update_cursor_position']
    data01,labels01 = get_data(files, filters)

    filters=['check_spelling']
    data02,labels02 = get_data(files, filters)

    filters=['receive_chat_message']
    data03,labels03 = get_data(files, filters)

    files = ['remote/exp2/raw.edge.1800secs.1users.1koala.2285'
            ,'remote/exp2/raw.edge.1800secs.1users.1koala.5a72'
            ,'remote/exp2/raw.core.1800secs.1users.1koala.946d'
    ]

    filters=['full_compile']
    data04,labels04 = get_data(files, filters)

    filters=['document_diff']
    data05,labels05 = get_data(files, filters)


    files = ['remote/exp2/raw.edge.600secs.2users.1koala.5385' #first run
            ,'remote/exp2/raw.edge.600secs.2users.1koala.8d2b'
            ,'remote/exp2/raw.core.600secs.2users.1koala.cab0'
             ]


    filters=['update_text']
    data10,labels10 = get_data(files, filters)

    filters=['update_cursor_position']
    data11,labels11 = get_data(files, filters)

    filters=['check_spelling']
    data12,labels12 = get_data(files, filters)

    filters=['receive_chat_message']
    data13,labels13 = get_data(files, filters)

    files = ['remote/exp2/raw.edge.1800secs.1users.1koala.b36f'
            ,'remote/exp2/raw.edge.1800secs.1users.1koala.d325'
            ,'remote/exp2/raw.core.1800secs.1users.1koala.3325'
    ]

    filters=['full_compile']
    data14,labels14 = get_data(files, filters)

    filters=['document_diff']
    data15,labels15 = get_data(files, filters)


    labels=['edge1', 'edge2', 'core']
    fliers = False

    rows = 2
    cols = 6
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(8, 6))

    axes[0,0].set_title('Update text')
    axes[0,0].boxplot(data00, labels=labels, showfliers=fliers)

    axes[0,1].set_title('Update cursor')
    axes[0,1].boxplot(data01, labels=labels, showfliers=fliers)

    axes[0,2].set_title('Spelling')
    axes[0,2].boxplot(data02, labels=labels, showfliers=fliers)

    axes[0,3].set_title('Chat')
    axes[0,3].boxplot(data03, labels=labels, showfliers=fliers)

    axes[0,4].set_title('Compile')
    axes[0,4].boxplot(data04, labels=labels, showfliers=fliers)

    axes[0,5].set_title('History')
    axes[0,5].boxplot(data05, labels=labels, showfliers=fliers)


    axes[1,0].set_title('Update text')
    axes[1,0].boxplot(data10, labels=labels, showfliers=fliers)

    axes[1,1].set_title('Update cursor')
    axes[1,1].boxplot(data11, labels=labels, showfliers=fliers)

    axes[1,2].set_title('Spelling')
    axes[1,2].boxplot(data12, labels=labels, showfliers=fliers)

    axes[1,3].set_title('Chat')
    axes[1,3].boxplot(data13, labels=labels, showfliers=fliers)

    axes[1,4].set_title('Compile')
    axes[1,4].boxplot(data14, labels=labels, showfliers=fliers)

    axes[1,5].set_title('History')
    axes[1,5].boxplot(data15, labels=labels, showfliers=fliers)

    axes[0,0].set_ylabel('Latency (ms)')
    # axes[1,0].set_ylabel('Latency (ms)')

    for i in range(rows):
        for j in range(cols):
            axes[i,j].set_ylim(ymin=0)

    fig.subplots_adjust(hspace=0.4, wspace=0.5)
    plt.show()


    # plt.plot(range(len(data[0])), data[0], 'r-', label=labels[0])
    # plt.plot(range(len(data[1])), data[1], 'b-', label=labels[1])
    # leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
    # plt.show()

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











