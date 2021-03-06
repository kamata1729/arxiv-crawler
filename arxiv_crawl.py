import arxiv
import requests
import json
import os
from datetime import datetime
import time


def lambda_handler(event, context):
    token = get_token()
    new_papers = get_new_arxiv_papers()
    for paper in new_papers:
        post_paper_to_slack(paper, token, translate=True)
    return True


def get_token():
    if os.path.exists('TOKEN.json'):
        with open('TOKEN.json') as f:
            token = json.load(f)
            return token
    else:
        token = {'GOOGLE_API_KEY': os.environ['GOOGLE_API_KEY'],
                 'SLACK_BOT_USER_OATH_ACCESS_TOKEN': os.environ['SLACK_BOT_USER_OATH_ACCESS_TOKEN'],
                 'SLACK_OATH_ACCESS_TOKEN': os.environ['SLACK_OATH_ACCESS_TOKEN'],
                 'CHANNEL_ID': os.environ['CHANNEL_ID']
                 }
        return token


def get_new_arxiv_papers(search_query="cs.CV", max_results=50):
    arxiv_res = arxiv.query(search_query=search_query,
                            max_results=max_results, sort_by="submittedDate")

    utc = datetime.utcfromtimestamp(time.time())
    news_paper_list = []
    last_updated_time = None
    for i, res in enumerate(arxiv_res):
        updated_time = datetime.strptime(res['updated'], '%Y-%m-%dT%H:%M:%SZ')
        if i == 0:
            print("utc: ", utc)
            print("last updated paper: ", updated_time)
            last_updated_time = updated_time
        if utc.weekday() == 0:  # Monday
            if utc.day - updated_time.day == 3:
                news_paper_list.append(res)
        else:
            if utc.day - updated_time.day == 1:
                news_paper_list.append(res)

    if len(news_paper_list) == 0:
        post_message_to_slack(
            'There is no papers submitted in the last day', get_token())
        post_message_to_slack('last submitted date: {}'.format(
            last_updated_time), get_token())
    return news_paper_list


def translate_text(text, token):
    translate_url = "https://translation.googleapis.com/language/translate/v2?key=" + \
        token['GOOGLE_API_KEY']
    headers = {"Content-Type": "application/json"}
    content = {'q': text,
               'source': 'en',
               'target': 'ja',
               'format': 'text'}
    response = requests.post(
        translate_url, data=json.dumps(content), headers=headers)
    if response.ok:
        translated_data = json.loads(response.text)
        translated_text = translated_data['data']['translations'][0]['translatedText']
        return translated_text
    else:
        return False


def post_paper_to_slack(paper, token, translate=True):
    post_message_url = 'https://slack.com/api/chat.postMessage'
    abstract = paper['summary']
    if translate:
        abstract = translate_text(paper['summary'].replace('\n', ' '), token)

    post_json = {
        'token': token['SLACK_OATH_ACCESS_TOKEN'],
        'text': '*' + paper['title'].replace('\n', '') + '*' + '\n' + paper['arxiv_url'],
        'channel': token['CHANNEL_ID'],
        'username': 'arXiv-crawling',
        'icon_url': 'https://i.imgur.com/ldRH2jt.png',
        'attachments': str([
            {
                "color": "#36a64f",
                "fields": [
                    {
                        "title": "Abstract",
                        "value": abstract,
                    }
                ]
            }])
    }
    requests.post(post_message_url, data=post_json)
    print(paper['title'].replace('\n', ''))


def post_message_to_slack(text, token):
    post_message_url = 'https://slack.com/api/chat.postMessage'
    post_json = {
        'token': token['SLACK_OATH_ACCESS_TOKEN'],
        'text': text,
        'channel': token['CHANNEL_ID'],
        'username': 'arXiv-crawling',
        'icon_url': 'https://i.imgur.com/ldRH2jt.png',
    }
    requests.post(post_message_url, data=post_json)


if __name__ == '__main__':
    lambda_handler(None, None)
