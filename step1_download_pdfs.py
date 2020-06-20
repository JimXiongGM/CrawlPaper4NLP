from tqdm import tqdm
import requests, json, os, re, time
from multiprocessing import Pool
from utils import get_headers_cookies, check_pdf, yield_tuples, save_screenshot, simple_clean_text


proxies = { "socks5": "http://127.0.0.1:1080", "socks5": "http://127.0.0.1:1080", }
# proxies = None

# folder = '/home/d/papers_data'
folder = './papers_data'

def _for_IAAI(year, code1, code2):

    AAAI_year = year[-2:]

    if AAAI_year == '14':
        url = f'https://www.aaai.org/ocs/index.php/IAAI/IAAI{AAAI_year}/paper/download/{code1}/{code2}'
        # url = f'https://www.aaai.org/ocs/index.php/EAAI/EAAI{AAAI_year}/paper/viewFile/{code1}/{code2}'
    elif AAAI_year == '15':
        url = f'https://www.aaai.org/ocs/index.php/IAAI/IAAI{AAAI_year}/paper/viewFile/{code1}/{code2}'
    elif AAAI_year == '16':
        url = f'https://www.aaai.org/ocs/index.php/IAAI/IAAI{AAAI_year}/paper/download/{code1}/{code2}'
    elif AAAI_year == '17':
        url = f'https://aaai.org/ocs/index.php/IAAI/IAAI{AAAI_year}/paper/download/{code1}/{code2}'
    return url
    

def download_multi(dw_tuple):
    """e.g. dw_tuple = ('ACL_xxxx,name,url')"""
    # basic
    dw_tuple = list(dw_tuple)
    org_year = dw_tuple[0].strip()
    org = org_year.split('_')[0]
    year = org_year.split('_')[1]
    # if year != '2019': return
    pdf_name = simple_clean_text(dw_tuple[1])
    file_name = f'{folder}/{org}/{org_year}/{pdf_name}.pdf'
    import os
    if os.path.exists(file_name): return True
    pdf_url = dw_tuple[2].strip()
    headers, cookies = get_headers_cookies(org, year)
    retry = 0

    # settings for AAAI
    if org == 'AAAI':
        code1, code2 = pdf_url.split('/')[-2:]
        headers, cookies = get_headers_cookies(org, year, which=2, code = code1)
        AAAI_year = year[-2:]
        AAAI_pdf_url = f'https://aaai.org/ocs/index.php/AAAI/AAAI{AAAI_year}/paper/download/{code1}/{code2}' \
            if AAAI_year != '19' else pdf_url
        pdf_url = AAAI_pdf_url
    
    dw_tuple[2] = pdf_url
    if not os.path.exists(f'{folder}/{org}/{org_year}'): os.makedirs(f'{folder}/{org}/{org_year}')

    FLAG = check_pdf(file_name)
    while not FLAG:
        retry += 1
        time.sleep(0.5)

        if retry >= 2:
            if org != 'AAAI' or retry >=3:
                if os.path.exists(file_name): os.remove(file_name)
                return f'ERROR AFTER RETRY:{dw_tuple}'
            else:
                # try again for IAAI
                headers, cookies = get_headers_cookies(org, year, which=3)
                dw_tuple[2] = pdf_url = _for_IAAI(year, code1, code2)
                # print(file_name, pdf_url)
                # pass

        try: 
            with requests.Session() as s:
                pdf_content = s.get(pdf_url, headers = headers, cookies = cookies, proxies=proxies, allow_redirects=True, timeout = 90).content
            print(len(pdf_content))
            # if len(pdf_content) > 1000: FLAG = True
        except: 
            continue

        with open(file_name,'wb') as F:
            F.write(pdf_content)
        
        FLAG = check_pdf(file_name)

    return True

def run(url_path = 'ACL_pdfs_all.json', prossing_num = 8):
    with open(url_path,'r', encoding = 'utf8') as f:
        pdf_tuples_list = [i for i in yield_tuples(json.load(f))]

    errs = []
    with tqdm(total = len(pdf_tuples_list), ncols=100) as pbar:
        with Pool(prossing_num) as pool:
            pool_iter = pool.imap(download_multi, pdf_tuples_list)
            for r in pool_iter:
                if 'ERROR ' in str(r): errs.append(r)
                pbar.update()
    
    if len(errs) != 0:
        time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        with open(f'DownLoad_Errors_{time_now}.log', 'w', encoding='utf8') as err_file:
            for i in errs:
                err_file.write(f'{i}\n')
    
    print (f'{url_path}: DONE! please check the error file! err nums: {len(errs)}')

def test(url_path = 'ACL_pdfs_all.json'):
    with open(url_path,'r') as f:
        pdf_tuples_list = [i for i in yield_tuples(json.load(f))]
    print(f'pdf_tuples_list[0]: {pdf_tuples_list[0]}')
    download_multi(pdf_tuples_list[0])

if __name__ == "__main__":
    # test()
    # run(url_path = 'ACL_pdfs_all.json') # OK
    # run(url_path = 'EMNLP_pdfs_all.json') # OK

    # run(url_path = './url_json/NAACL_2014_2015_2016_2017_2018_2019.json', prossing_num = 8)
    # run(url_path = './url_json/AAAI_2014_2015_2016_2017_2018_2019.json', prossing_num = 8)
    # run(url_path = './url_json/ICLR_2020.json', prossing_num = 8)
    # run(url_path = 'KDD_2017_2018_2019.json', prossing_num = 16) # ok remain 14 errs
    # run(url_path = 'NIPS_2017_2018_2019.json', prossing_num = 16) # no err!
    # run(url_path = 'ICML_2017_2018.json', prossing_num = 16) # 
    run(url_path = './url_json/IJCAI_2015_2016_2017_2018_2019.json', prossing_num = 8)
    # test('AAAI_pdfs_all.json')
    