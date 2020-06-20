from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from lxml import etree
import requests, time, json
from utils import get_headers_cookies, simple_clean_text
from multiprocessing.dummy import Pool
from tqdm import tqdm

# use selenium to get complete source code. 
options = webdriver.ChromeOptions() 
options.add_argument('--headless') 
options.add_argument('--disable-gpu') 
options.add_argument("--no-sandbox") 

urls = [
'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017',
'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018',
'https://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019',]

all_dict = {}
headers, _ = get_headers_cookies('NIPS')
with webdriver.Chrome(options=options,executable_path='./chromedriver.exe') as driver:
    years = []
    for url in urls:
        
        names_list = []
        urls_list_1 = []
        pdf_url_list = []
        
        year = url[-4:]
        years.append(year)
        all_dict[f'NIPS_{year}'] = {}
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        _ = wait.until(presence_of_element_located((By.XPATH, '//a[contains(@href,"/paper/")]')))

        nodes = etree.HTML(driver.page_source).xpath('//a[contains(@href,"/paper/")]')
        print(f'{year} len: {len(nodes)}')
        for node in nodes:
            name = simple_clean_text(node.xpath('string(.)'))
            href = 'https://papers.nips.cc' + node.xpath('@href')[0]
            names_list.append(name)
            urls_list_1.append(href)
        
        
        def _get_url(url):
            try:
                with requests.Session() as s:
                    res1 = s.get(url, headers = headers, timeout = 20)
                href = etree.HTML(res1.content).xpath('//a[contains(text(),"[PDF]")]/@href')[0]
                return 'https://papers.nips.cc' + href
            except:
                return f'ERROR :{url}'
        
        pbar = tqdm(total = (len(urls_list_1)))
        with Pool(16) as pool:
            pool_iter = pool.imap(_get_url, urls_list_1)
            for i in pool_iter:
                if 'ERROR ' not in i:
                    pdf_url_list.append(i)
                else:
                    print (i)
                pbar.update()
        
        for i,j in zip(names_list, pdf_url_list):
            all_dict[f'NIPS_{year}'][i] = j

        print(f'{year}  len names_list: {len(names_list)}  pdf_url_list: {len(pdf_url_list)}')

_years = '_'.join(years)
with open(f'NIPS_{_years}.json', 'w', encoding='utf8') as f1:
    json.dump(all_dict, f1)