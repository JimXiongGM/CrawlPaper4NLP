from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from lxml import etree
import time
import requests
from utils import get_headers_cookies
from multiprocessing.dummy import Pool
from tqdm import tqdm_notebook as tqdm

# use selenium to get complete source code. 
options = webdriver.ChromeOptions() 
# options.add_argument('--headless') 
options.add_argument('--disable-gpu') 
options.add_argument("--no-sandbox") 

urls = [
'https://icml.cc/Conferences/2017/Schedule?type=Poster',
'https://icml.cc/Conferences/2018/Schedule?type=Poster',
]

all_dict = {}
headers, _ = get_headers_cookies('ICML')
with webdriver.Chrome(options=options,executable_path='./chromedriver') as driver:
    for year,url in zip(['2017', '2018'], urls):
        
        urls_list_1 = []
        
        all_dict[f'ICML_{year}'] = {}
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        _ = wait.until(presence_of_element_located((By.XPATH, '//a[contains(text(),"PDF »")]')))

        nodes = etree.HTML(driver.page_source).xpath('//a[contains(text(),"PDF »")]')
        print(f'{year} len: {len(nodes)}')
        for node in nodes:
            href = node.xpath('@href')[0].strip()
            urls_list_1.append(href)
        
        def _get_url(url):
            try:
                with webdriver.Chrome(options=options,executable_path='./chromedriver') as driver:
                    wait = WebDriverWait(driver, 20)
                    driver.get(url)
                    _ = wait.until(presence_of_element_located((By.XPATH, '//a[contains(text(),"Download PDF")]')))
                    
                    time.sleep(2)
                    name = etree.HTML(driver.page_source).xpath('//*[@class="post-content"]/h1/text()')[0]
                    href = etree.HTML(driver.page_source).xpath('//a[contains(text(),"Download PDF")]/@href')[0]
                    return [name, href]
            except:
                return f'ERROR :{name}  {url}'
        
        pbar = tqdm(total = (len(urls_list_1)))
        with Pool(16) as pool:
            pool_iter = pool.imap(_get_url, urls_list_1)
            for i in pool_iter:
                if 'ERROR ' not in i:
                    name = i[0]
                    href = i[1]
                    all_dict[f'ICML_{year}'][name] = href
                else:
                    print (i)
                pbar.update()

for key in [i for i in all_dict.keys()]:
    print(f'{key} len: {len(all_dict[key])}')
    
import json
with open('ICML_2017_2018.json', 'w', encoding='utf8') as f1:
    json.dump(all_dict, f1)