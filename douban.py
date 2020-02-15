import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pymongo
from config import *

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]

def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_14_6)AppleWebKit/537.36(KHTML, like Gecko)Chrome/79.0.3945.130Safari/537.36'
        }
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all("div", class_="comment")
    for item in items:
        info = item.find_all(name='span', attrs={"class": "comment-info"})
        for users in info:
            user = users.find_all(name='a', attrs={"class": ""})[0].string
        yield{
            "user":user,
            "time":item.find_all(name='span', attrs={"class":"comment-time"})[0].string.strip(),
            "comment":item.find_all(name='span', attrs={"class":"short"})[0].string
        }
def save_to_mongo(content):
    if db[mongo_table].insert(content):
        print('Successful', content)
        return True
    return False

def main():
    url = 'https://movie.douban.com/subject/27119724/comments?sort=new_score&status=P'
    html =get_page(url)
    for item in parse_page(html):
        save_to_mongo(item)

if __name__ == '__main__':
    main()