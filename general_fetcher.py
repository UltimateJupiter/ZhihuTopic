task_list = [
    [19662742, "资本家"],
    [20073342, "社会主义"],
    [19916030, "剥削"],
    [20064332, "996"],
    [19613266, "左派"],
    [19960840, "强制加班"],
    [19582963, "资本主义"],
    [19685024, "阶级"],
    [19582433, "苏联"],
    [19571449, "马克思"],
    [19924829, "共产国际"],
    [19599479, "世界史"],
    [19551424, "政治"],
    [19566933, "社会"],
    [19551077, "历史"]
]

from essense_fetcher import get_topic_essence
from answer_fetcher import get_answer_of_q
import json
import sys

def fetch(i):
    tid, name = task_list[i]
    print(name)
    # res = get_topic_essence(tid, 1000)
    res = get_topic_essence(tid, 1000)
    concat_res = []
    for x in res:
        concat_res.extend(x)
    
    fl = './log/{}_{}_essense.json'.format(tid, name)
    with open(fl, 'w') as outfile:
        json.dump(concat_res, outfile)
    print("{} done".format(name))

    questions = list(set([x[5] for x in concat_res]))
    print("Extend search {} with {} questions".format(name, len(questions)))

    q_res = get_answer_of_q(questions, 100)
    total_ans = sum(len(x) for x in q_res)

    fl = './log/{}_{}_q.json'.format(tid, name)
    with open(fl, 'w') as outfile:
        json.dump(q_res, outfile)
    print("{} extended search done with {} answers".format(name, total_ans))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        fetch(int(sys.argv[1]))
    elif len(sys.argv) == 3:
        print("seq")
        for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
            fetch(i)
    else:
        for i in range(len(task_list)):
            fetch(i)