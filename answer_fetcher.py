import requests
import sys
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39',
}

def get_raw_json(qid, limit, offset):
    url = f'https://www.zhihu.com/api/v4/questions/{qid}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit={limit}&offset={offset}&platform=desktop&sort_by=default'

    resp = requests.get(url, headers=headers)
    # print(resp)
    if resp.status_code != 200:
        print('failed')

    content = resp.json()
    data = content.get('data')
    res = []
    for i in range(limit):
        try:
            vals = data[i]
            info = [vals['id'], vals['created_time'], vals['comment_count'], vals['voteup_count']]
            res.append(info)
        except:
            print("Failed at answer {}".format(i + offset))
            break
    return res


def get_answers(q_id, answer_count):
    lapse = min(20, answer_count)
    res = []
    if lapse == 0:
        return res
    # print("Scrapping {} with {} answers".format(q_id, answer_count))
    for i in range(int(answer_count / lapse)):
        result = get_raw_json(q_id, lapse, lapse * i)
        res.extend(result)
    return res

if __name__ == '__main__':
    res = get_answers(455440748, 1)
    print(res)
