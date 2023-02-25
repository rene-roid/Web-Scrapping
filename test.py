from bs4 import BeautifulSoup
from lxml import etree
import requests

url = 'https://bun.sh/blog/bun-v0.5.6'

# Using BeautifulSoup | HTML
def get_html(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup

def get_paragraphs(soup):
    paragraphs = soup.find_all('p')

    for paragraph in paragraphs:
        print(paragraph.text)

def get_code(soup: BeautifulSoup):
    code = soup.find_all('pre')
    print(code)

    for c in code:
        c = BeautifulSoup(str(c), 'html.parser')
        print(c.text)

#get_paragraphs(get_html(url))
#get_code(get_html(url))


# Using BeautifulSoup | XML
path = '//*[@id="blog-post"]/div[2]/article/p'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def get_xml(url):
    web = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(web.content, 'html.parser')
    dom = etree.HTML(str(soup))
    result = dom.xpath(path)

    # print everything in the result
    for r in result:
        print(r.text)


#get_xml(url)