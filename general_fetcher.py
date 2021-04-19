task_list = [
    [19662742, "资本家", 1755],
    [20073342, "社会主义", 2415],
    [19916030, "剥削", 571],
    [20064332, "996", 3320],
    [19613266, "左派", 2597],
    [19960840, "强制加班", 3375],
    [19582963, "资本主义", 5233],
    [19685024, "阶级", 16027],
    [19551424, "政治", 245533]
]

from topic_fetcher import get_topic
import json

for tid, name, count in task_list:
    res = get_topic(tid, count)
    fl = './log/{}_{}.json'.format(tid, name)
    with open(fl, 'w') as outfile:
        json.dump(res, outfile)
    print("{} done".format(name))