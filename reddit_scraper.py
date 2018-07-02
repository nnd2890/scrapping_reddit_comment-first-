import urllib.request
from bs4 import BeautifulSoup
import json

def parse_comment_page(page_url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    request = urllib.request.Request(page_url,headers={'User-Agent':user_agent})
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, 'html.parser')
    main_post = soup.find('div',attrs={'data-test-id':'post-content'})
    comment_area = soup.find('div',attrs={'class':'z37iyq-0 hCmtoZ'})

    title = main_post.find('span',attrs={'class':'y8HYJ-y_lTUHkQIc1mdCq s1qvxt86-0 hrMDVl'}).text
    upvotes = main_post.find('div',attrs={'class':'_1rZYMD_4xY3gRcSS3p8ODO'}).text
    original_poster = main_post.find('a',attrs={'class':'_2tbHP6ZydRpjI44J3syuqC s1461iz-1 gWXVVu'}).text
    comment_count = main_post.find('div',attrs={'class':'_1UoeAeSRhOKSNdY_h3iS1O _3m17ICJgx45k_z-t82iVuO'}).text
    comments = comment_area.find_all('div',attrs={'class':'r4x9ih-4 bUDVGu'})
    extracted_comments = []
    for comment in comments:
        commenter = comment.find('div',attrs={'class':'wx076j-0 hPglCh'}).text
        comment_text = comment.find('div',attrs={'class':'r4x9ih-6 iZRNCr s1hmcfrd-0 gOQskj'}).text
        extracted_comments.append({'commenter':commenter,'comment_text':comment_text})    

    post_data = {
        'title':title,
        'upvotes':upvotes,
        'commemt_count':comment_count,
        'original_poster':original_poster,
        'comment':extracted_comments
    }
    return post_data

url = "https://www.reddit.com/top/"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
request = urllib.request.Request(url,headers={'User-Agent':user_agent})
html = urllib.request.urlopen(request).read()

soup = BeautifulSoup(html,'html.parser')
main_table = soup.find("div",attrs={'class':'s1us1wxs-0 iENbwa s12rq52u-0 jNBfJm'})
links = main_table.find_all("a",class_="SQnoC3ObvgnGjWt90zD9Z")
comment_a_tags = main_table.find_all('a',attrs={'class':'_1UoeAeSRhOKSNdY_h3iS1O _1Hw7tY9pMr-T1F4P1C-xNU'})

extracted_records = []
for link in links:
    title = link.text
    url = link['href']

    if not url.startswith('http'):
        url = "https://reddit.com" + url
    record = {
        'title':title,
        'url':url
    }
    extracted_records.append(record)

urls = []
for a_tag in comment_a_tags[:3]:
    url = a_tag['href']
    if not url.startswith('http'):
        url = 'https://reddit.com' + url
        print('Extracting data form %s'%url)
        urls.append(parse_comment_page(url))
    

# with open('data.json', 'w') as outfile:
#     json.dump(extracted_records, outfile)

with open('comments.json', 'w') as outfile:
    json.dump(urls, outfile)