import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import json


def main():

    # files = ['raw.core.600secs.5users.0koala.5e92', 'raw.core.600secs.5users.1koala.13c7'] #koala overhead
    # files = ['remote/raw.core.600secs.5users.0koala.0b52', 'remote/raw.edge.600secs.5users.0koala.171e'] #edge/core 20 ms update_text
    # files = ['remote/raw.core.600secs.5users.1koala.1eaa','remote/raw.edge.600secs.5users.0koala.80c3'] #edge/core 50 ms update_text
    files = ['remote/raw.core.600secs.5users.1koala.d65b','remote/raw.edge.600secs.5users.1koala.e481'] #edge/core 50 ms update_text

    #files = ['remote/raw.core.1800secs.2users.1koala.7058','remote/raw.edge.1800secs.2users.1koala.bb8c'] #compile

    filters=['update_text']
    data00,labels00 = get_data(files, filters)

    filters=['update_cursor_position']
    data01,labels01 = get_data(files, filters)

    filters=['check_spelling']
    data02,labels02 = get_data(files, filters)

    filters=['receive_chat_message']
    data12,labels12 = get_data(files, filters)

    # files = ['remote/raw.core.1800secs.2users.1koala.7058','remote/raw.edge.1800secs.2users.1koala.bb8c'] #compil
    files = ['remote/raw.core.1800secs.2users.1koala.a2c8','remote/raw.edge.1800secs.2users.1koala.7540'] #compil

    filters=['full_compile']
    data10,labels10 = get_data(files, filters)

    filters=['document_diff']
    data11,labels11 = get_data(files, filters)


    labels=['core', 'edge']
    fliers = False

    rows = 2
    cols = 3
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(6, 6))

    axes[0,0].set_title('Update text')
    axes[0,0].boxplot(data00, labels=labels, showfliers=fliers)

    axes[0,1].set_title('Update cursor')
    axes[0,1].boxplot(data01, labels=labels, showfliers=fliers)

    axes[0,2].set_title('Spelling')
    axes[0,2].boxplot(data02, labels=labels, showfliers=fliers)


    axes[1,0].set_title('Compile')
    axes[1,0].boxplot(data10, labels=labels, showfliers=fliers)

    axes[1,1].set_title('History')
    axes[1,1].boxplot(data11, labels=labels, showfliers=fliers)

    axes[1,2].set_title('Chat')
    axes[1,2].boxplot(data12, labels=labels, showfliers=fliers)

    axes[0,0].set_ylabel('Latency (ms)')
    axes[1,0].set_ylabel('Latency (ms)')

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











