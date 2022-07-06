import requests
import shutil
from bs4 import BeautifulSoup

lines = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
with open('links-to-scrape.txt', 'r') as f:
    lines = f.read().split('\n')
    
def extract_full_res_img_link(href):
    response = requests.get(href)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_link = soup.find(id='file').find('a')
    
    print('Extracted full res image from https:' + img_link['href'] + ' with status code ' + response.status_code)
    return ('https:' + img_link['href'])

def extract_hrefs(wiki_urls):
    hrefs = []
    
    for url in wiki_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find(id='firstHeading')
        img = soup.find('a', class_='image')
        
        
        hrefs.append([title.text + '.png', 'https://en.wikipedia.org' + img['href']])
        print('Got href ', img['href'], ' with status code ', response.status_code)
        
    return hrefs


hrefs = []
for i in extract_hrefs(lines):
    full_res = extract_full_res_img_link(i[1])
    hrefs.append([i[0], full_res])


for h in hrefs:
    # h[0] = title , h[1] = url
    r = requests.get(h[1], headers=headers, stream = True)
    print('Writing to file... ', h[0])
    
    r.raw_decode_content = True
    if r.status_code == 200:
        with open(h[0], 'wb') as fi:
            shutil.copyfileobj(r.raw, fi)
            print('Successfully wrote to file ', h[0])    
    else:
        print('err creating img files', r.status_code)
        
    


    
