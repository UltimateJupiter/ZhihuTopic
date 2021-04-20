import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
from datetime import datetime
import json

plt.style.use('ggplot')

task_list = [
    [19662742, "资本家", "Bourgeois"],
    [19582963, "资本主义", "Capitalism"],
    [19960840, "强制加班","Mandatory Overwork"],
    [20064332, "996", "996"],
    [19916030, "剥削", "Exploitation"],
    [19685024, "阶级", "Class"],
    [19613266, "左派", "Left Wing"],
    [19571449, "马克思", "Marx (Marxism)"],
    [19924829, "共产国际", "Commintern"],
    [20073342, "社会主义", "Socialism"],
    [19582433, "苏联", "Soviet Union"],
    [19599479, "世界史", "World History"],
    [19551424, "政治", "Politics"],
    [19566933, "社会", "Society"],
    [19551077, "历史", "History"]
]

def seq_moving_average(x, w):
    kernel = np.zeros(w)
    mid = len(kernel) / 2
    for i in range(len(kernel)):
        kernel[i] = np.exp(- (i - mid) ** 2 / (w ** 2 / 32))
    base = np.convolve(np.ones_like(x), kernel, 'same')
    return np.convolve(np.array(x), kernel, 'same') / base

def load_essence(fl):
    comments, voteups = [], []
    dates = []
    with open(fl) as infl:
        ls = json.load(infl)

    for l in ls:
        dates.append(int(l[1] / (24 * 3600)))
        voteups.append(l[2])
        comments.append(l[3])

    ret = date_sum(dates, voteups, comments)
    return ret

def load_extend_search(fl):
    comments, voteups = [], []
    dates = []
    with open(fl) as infl:
        ls = json.load(infl)

    for q in ls:
        for l in q:
            dates.append(int(l[1] / (24 * 3600)))
            voteups.append(l[3])
            comments.append(l[2])

    ret = date_sum(dates, voteups, comments)
    return ret

def date_sum(dates, voteups, comments):

    all_dates = np.arange(15700, 18650)
    
    voteup_record, comment_record = {}, {}
    for i, date in enumerate(dates):
        if date not in voteup_record:
            voteup_record[date] = voteups[i]
        else:
            voteup_record[date] += voteups[i]
        if date not in comment_record:
            comment_record[date] = comments[i]
        else:
            comment_record[date] += comments[i]
    
    all_voteups, all_comments = np.zeros_like(all_dates), np.zeros_like(all_dates)
    for i, date in enumerate(all_dates):
        if date in voteup_record:
            all_voteups[i] = voteup_record[date]
        if date in comment_record:
            all_comments[i] = comment_record[date]
    return all_dates, all_voteups, all_comments

def get_normalize_flow(args, comment_weight, smooth):
    flows = []
    for i in args:
        fl = '../log/{}_{}_q.json'.format(task_list[i][0], task_list[i][1])
        flows.append(load_extend_search(fl))
    
    index_smooth = None

    for i, [dates, voteups, comments] in enumerate(flows):
        if index_smooth is None:
            index_smooth = seq_moving_average(voteups + comments * comment_weight, smooth)
        else:
            index_smooth += seq_moving_average(voteups + comments * comment_weight, smooth)
    return index_smooth

def label_axis(dates):
    ticks_major = []
    ticks_major_keys = []
    ticks_minor = []
    for date in dates:
        date_str = datetime.isoformat(datetime.fromtimestamp(date * 24 * 3600), timespec='hours')[:-3]
        if date_str.endswith('-01-01'):
            ticks_major.append(date)
            ticks_major_keys.append(date_str[:4])
        elif date_str.endswith('-01'):
            ticks_minor.append(date)
    return ticks_major, ticks_major_keys, ticks_minor

def vis_extend(args=None, normalize_args=None, smooth=1000, comment_weight=5, name=''):

    flows = []
    kws = []
    for i in args:
        fl = '../log/{}_{}_q.json'.format(task_list[i][0], task_list[i][1])
        flows.append(load_extend_search(fl))
        kws.append(task_list[i][2])

    if normalize_args is not None:
        normalize_flow = get_normalize_flow(normalize_args, comment_weight, smooth)
    
    plt.figure(figsize=(10, 5))
    for i, [dates, voteups, comments] in enumerate(flows):
        print(kws[i])
        index_smooth = seq_moving_average(voteups + comments * comment_weight, smooth)
        if normalize_args is not None:
            index_smooth /= normalize_flow
        index_smooth /= np.max(index_smooth)
        plt.plot(dates, index_smooth, label=kws[i])

    plt.ylim([-0.1, 1.19])
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=5, fancybox=False, shadow=False)
    ticks_major, ticks_major_keys, ticks_minor = label_axis(dates)
    plt.xticks(ticks_major, ticks_major_keys)
    plt.gca().set_xticks(ticks_minor, minor=True)
    
    plt.xlabel('Year')
    plt.ylabel('Popularity Index (Normalized)')

    plt.savefig('index_{}.png'.format(name), dpi=300)
    # print(flows, kws)

if __name__ == "__main__":
    vis_extend([0,1,2,3], normalize_args=[11, 12, 13, 14], name='Overwork')
    vis_extend([5,6,7,8], normalize_args=[11, 12, 13, 14], name='Left')
    vis_extend([9,10], normalize_args=[11, 12, 13, 14], name='Soviet')
    # vis_extend([0,1,2], normalize_args=[11, 12, 13, 14], name='Overwork')