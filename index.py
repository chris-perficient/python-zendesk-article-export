import os
import datetime
import csv

import requests

credentials = '', ''
session = requests.Session()
session.auth = credentials

date = datetime.date.today()
backup_path = os.path.join('backups', str(date), 'en-US')
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []
brands = [
  'https://prft-mso.zendesk.com/api/v2/help_center/en-us/articles',
  'https://prft-converge.zendesk.com/api/v2/help_center/en-us/articles',
  'https://prftamazonconnect.zendesk.com/api/v2/help_center/en-us/articles',
  'https://prft-cconnect.zendesk.com/api/v2/help_center/en-us/articles',
];

endpoint = 'https://perficient.zendesk.com/api/v2/help_center/en-us/articles.json'
while endpoint:
    response = session.get(endpoint)
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(response.status_code))
        exit()
    data = response.json()

    for article in data['articles']:
        if article['body'] is None:
            continue
        title = '<h1>' + article['title'] + '</h1>'
        filename = '{id}.html'.format(id=article['id'])
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article['body'])
        # print('{id} copied!'.format(id=article['id']))

        log.append((filename, article['title'], article['author_id']))

    endpoint = data['next_page']
    if data['next_page']:
      print("not null", data['next_page'])
      endpoint = data['next_page']
    else:
        if not brands:
            continue
        if brands:
            temp = brands.pop()
            endpoint = temp
            print("Brand", endpoint)

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID'))
    for article in log:
        writer.writerow(article)








# while endpoint:
#     response = requests.get(endpoint, auth=credentials)
#     if response.status_code != 200:
#         print('Failed to retrieve articles with error {}'.format(response.status_code))
#         exit()
#     data = response.json()

#     for article in data['articles']:
#         # if article['body'] is None:
#         #     continue
#         # title = '<h1>' + article['title'] + '</h1>'
#         # filename = '{id}.html'.format(id=article['id'])
#         # with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
#         #     f.write(title + '\n' + article['body'])
#         print('{id} copied!'.format(id=article['id']))
#         log.append(article)
#         # print(article)

        

#     endpoint = data['next_page']

# print("LOGGG", log)
# jsonString = json.dumps(log, separators=(',', ':'))
# jsonFile = open("backups.json", "w")
# jsonFile.write(jsonString)
# jsonFile.close()


# with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow( ('File', 'Title', 'Author ID') )
#     for article in log:
#         writer.writerow(article)