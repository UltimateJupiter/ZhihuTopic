import requests
import sys
import time
import json
from tqdm import trange

from answer_fetcher import get_answers
from joblib import Parallel, delayed

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39',
}
    

def get_raw_json(topicid, limit, offset, q_count):
    url = f'https://www.zhihu.com/api/v4/topics/{topicid}/feeds/timeline_question?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Cdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit={limit}&offset={offset}'
    resp = requests.get(url, headers=headers)
    # print(resp)
    if resp.status_code != 200:
        print('failed')

    if offset % 500 == 0:
        print("Working on {} / {}".format(offset, q_count), flush=True)

    content = resp.json()
    data = content.get('data')
    # print(content)
    res = []
    for i in range(limit):
        try:
            vals = data[i]['target']
            info = [vals['id'], vals['created'], vals['answer_count'], vals['follower_count'], vals['title']]
            q_id = vals['id']
            answer_info = get_answers(q_id, 40)
            info.append(answer_info)
            res.append(info)
        except:
            print("Failed at question {}".format(i + offset))
            continue
    return res
    # uniqid = data.get('uniqid')

    # all_data = user_indexes.get('all').get('data')
    # result = decrypt(ptbk, all_data)
    # result = result.split(',')

def get_topic(topic_id, q_count):
    print("Scrapping {} with {} questions".format(topic_id, q_count))
    res = Parallel(n_jobs=8, verbose=10)(delayed(get_raw_json)(topic_id, 10, 10 * i, q_count) for i in range(int(q_count / 10)))
    return res

if __name__ == '__main__':
    topic_id = 19582963
    res = get_topic(19582963, 4000)
    print(res)
