# multi-processing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from lxml import etree
import time, sys


def get_urls(zip_arg):
    org_year = zip_arg[0]
    url = zip_arg[1]
    
    # use selenium to get complete source code. 
    options = webdriver.ChromeOptions() 
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    options.add_argument("--no-sandbox") 
    if org_year == 'ICLR_2019_POSTER': time.sleep(20)
    executable_path = './chromedriver' if sys.platform != 'win32' else './chromedriver.exe'
    with webdriver.Chrome(options=options,executable_path=executable_path) as driver:
        wait = WebDriverWait(driver, 30)
        driver.get(url)
        _ = wait.until(presence_of_element_located((By.XPATH, '//a[@title="Download PDF"]')))
        nodes = etree.HTML(driver.page_source).xpath('//a[@title="Download PDF"]/..')

        print(f'{org_year} len: {len(nodes)}')
        res_dict = {}
        res_dict[org_year] = {}
        for node in nodes:
            name = node.xpath('a[1]/text()')[0].strip()
            if name.lower().startswith('withdraw') : continue
            if 'http' not in node.xpath('a[@title="Download PDF"]/@href')[0]:
                url = 'https://openreview.net' + node.xpath('a[@title="Download PDF"]/@href')[0]
            else:
                url = node.xpath('a[@title="Download PDF"]/@href')[0]
            res_dict[org_year][name] = url

        return res_dict

org_year_mark = {
    'ICLR_2016_MAIN':'https://iclr.cc/archive/www/doku.php%3Fid=iclr2016:accepted-main.html',
    'ICLR_2017_MAIN':'https://openreview.net/group?id=ICLR.cc/2017/conference',
    'ICLR_2018_ORAL':'https://openreview.net/group?id=ICLR.cc/2018/Conference#accepted-oral-papers',
    # 'ICLR_2018_POSTER':'https://openreview.net/group?id=ICLR.cc/2018/Conference#accepted-poster-papers', # 上一条包含这两条
    # 'ICLR_2018_WORKSHOP':'https://openreview.net/group?id=ICLR.cc/2018/Conference#workshop-papers',
    'ICLR_2019_ORAL':'https://openreview.net/group?id=ICLR.cc/2019/Conference#accepted-oral-papers',
    'ICLR_2019_POSTER':'https://openreview.net/group?id=ICLR.cc/2019/Conference#accepted-poster-papers'
}

org_year_mark2 = {
    'ICLR_2020_POSTER':'https://openreview.net/group?id=ICLR.cc/2020/Conference#accept-poster',
    'ICLR_2020_SPOTLIGHT':'https://openreview.net/group?id=ICLR.cc/2020/Conference#accept-spotlight',
    'ICLR_2020_ORAL':'https://openreview.net/group?id=ICLR.cc/2020/Conference#accept-talk',
}

def main(org_year_mark = org_year_mark2):
    from multiprocessing.dummy import Pool

    keys = [[i,org_year_mark[i]] for i in org_year_mark.keys()]
    all_dict = {}

    # get_urls(keys[0])
    with Pool(4) as pool:
        pool_iter = pool.imap(get_urls, keys)
        for r in pool_iter:
            all_dict.update(r)

    import json

    with open('ICLR_2020.json','w', encoding='utf8') as f1:
        json.dump(all_dict, f1)
    
if __name__ == "__main__":
    main()