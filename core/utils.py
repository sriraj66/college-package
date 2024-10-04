import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .embed import Emmbedded
import threading
from .models import *

def extract_page_urls(site_url):
    # Define custom headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(site_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = soup.find_all('a')
        
        page_urls = set()
        pdf_urls = set()
        png_urls = set()
        html_php_urls = set()
        ip_address_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')  # Regular expression pattern for IP address
        
        for link in links:
            href = link.get('href')
            if href and not href.startswith("mailto:"):  # Check if the link is not a mailto link
                absolute_url = urljoin(site_url, href)
                
                if (re.search(ip_address_pattern, absolute_url) is None) and \
                   ('mycamu.co.in' not in absolute_url) and \
                   ('form.jotform' not in absolute_url):
                    
                    if absolute_url.endswith('.pdf'):
                        pdf_urls.add(absolute_url)
                    elif absolute_url.endswith('.png'):
                        png_urls.add(absolute_url)
                    elif absolute_url.endswith(('.html', '.php')):
                        html_php_urls.add(absolute_url)
                    else:
                        page_urls.add(absolute_url)
        
        return page_urls, pdf_urls, png_urls, html_php_urls
    else:
        print(f"Failed to retrieve content from {site_url}. Status code: {response.status_code}")
        return set(), set(), set(), set()

def callback_function(id,urls):
    obj = ChatBot.objects.get(id=id)
    obj.running = True
    print("Embeding urls to the models")
    emb = Emmbedded(uid=obj.uid,prompt="SETUP",urls=urls)
    emb.add_sources()
    obj.state = True
    obj.save()

 

def add_source(id,site_url):
    try:
        obj = ChatBot.objects.get(id=id)
        urls = set()
        for i in site_url:    
            page_urls, pdf_urls, png_urls, html_php_urls = extract_page_urls(i)
            page_urls = page_urls.union(html_php_urls)
            print("Source URL from : ",i)
            for j in page_urls:
                print("Added : ",j)
                urls.add(j)
                
        callback_function(id,urls)
    except Exception as e:
        print(e)
            
def separate_urls(input_string):
    urls = [url.strip() for url in input_string.split('\r\n') if url.strip()]
    return urls

def start_page_source(id):
    clg = ChatBot.objects.get(id=id)
    urls = set()
    urls.add(clg.root_url)
    sub_urls = separate_urls(clg.aditional_urls)
    for i in sub_urls:
        urls.add(i)
    
    t = threading.Thread(target=add_source, args=(id,urls))
    
    t.start()

if __name__ == '__main__':
    pass