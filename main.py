import requests
import argparse
import re

keys1=[r'.*cod.*', r'.*计算机.*', r'.*Computer.*']  #第一个关键字列表
keys2=[r'.*paper.*', r'.*试卷.*', r'.*exam.*', r'.*test.*', r'.*试题.*']  #第二个关键字列表
search='ustc' #这里放搜索关键词
parser = argparse.ArgumentParser(description='Ustc-course Spyder')
parser.add_argument('token', help='token for your github account', type=str)
args = parser.parse_args()
token=args.token
headers={"Authorization":"token "+token}
search=search.replace(' ','+')
url_list=[]
for page in range(1,11):
    repo=requests.get("https://api.github.com/search/repositories?q="+search+"&per_page=100&page="+str(page),headers=headers).json()
    if(len(repo['items'])==0):
        break
    for item in repo['items']:
        full_name=item['full_name']
        branch=item['default_branch']
        tree_url='https://api.github.com/repos/'+full_name+'/git/trees/'+branch+'?recursive=1'
        content=requests.get(tree_url,headers=headers)
        if 'tree' not in content.json().keys():
            continue
        files=full_name.lower()
        for file in content.json()["tree"]:
            files+=file['path'].lower()
        match_keys1 = any(re.search(key, files, re.IGNORECASE) for key in keys1)
        match_keys2 = any(re.search(key, files, re.IGNORECASE) for key in keys2)
        if match_keys1 and match_keys2:
            print('https://github.com/'+full_name)
