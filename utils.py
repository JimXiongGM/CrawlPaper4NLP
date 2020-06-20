import re, os ,sys, traceback, subprocess, time, json


org_years_dict = {}
org_years_dict['ACL'] = ['2014', '2015', '2016', '2017', '2018', '2019']
org_years_dict['AAAI'] = ['2014', '2015', '2016', '2017', '2018', '2019']
org_years_dict['EMNLP'] = ['2014', '2015', '2016', '2017', '2018', '2019']
org_years_dict['ICLR'] = ['2017', '2018', '2019', '2020']
org_years_dict['ICML'] = ['2017', '2018']
org_years_dict['KDD'] = ['2017', '2018', '2019']
org_years_dict['NIPS'] = ['2017', '2018', '2019']
org_years_dict['NAACL'] = ['2015', '2016', '2018', '2019']
org_years_dict['IJCAI'] = ['2015', '2016', '2017', '2018', '2019']

def get_json_file_paths(json_file_folder = './'):
    # json_file_folder = './pdf_es_json/old/'.endswith
    if not json_file_folder.endswith('/'): json_file_folder = json_file_folder + '/'
    json_file_paths = []
    for org in org_years_dict.keys():
        file_name = json_file_folder + f'{org}_' + '_'.join([year for year in org_years_dict[org]]) + '.json'
        json_file_paths.append(file_name)
    return json_file_paths

def gen_files_path_from_dict(json_files_path = './url_json/', base_url = '/home/d/papers_data'):
    all_files_path = []
    json_paths = get_json_file_paths(json_files_path)
    for json_path in json_paths:
        org = json_path.split('/')[-1].split('_')[0]
        with open(json_path, 'r', encoding='utf8') as f:
            j = json.load(f)
        for org_year in j.keys():
            org = org_year.split('_')[0]
            for _name in j[org_year]:
                name = simple_clean_text(_name)
                path = f'{base_url}/{org}/{org_year}/{name}.pdf'
                all_files_path.append(path)
    return all_files_path


def ACL_headers_cookies(year = '2019'):
    headers={
        'authority': 'www.aclweb.org',
        'method': 'GET',
        'path': f'/anthology/events/acl-{year}/',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.aclweb.org/anthology/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    cookies = {}
    return headers, cookies

def NAACL_headers_cookies(year = '2019'):
    headers={
        'authority': 'www.aclweb.org',
        'method': 'GET',
        'path': f'/anthology/events/naacl-{year}/',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.aclweb.org/anthology/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    cookies = {}
    return headers, cookies

def AAAI_headers_cookies(year = None, which = 2, code = None):
    # 1: get urls in AAAI   2: download from AAAI
    headers_1={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.aaai.org',
        'Referer': 'https://www.aaai.org/Library/conferences-library.php',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    }
    cookies_1 = {}

    headers_2={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'OCSSID=9r5krtocddt02fmtr6evlou893',
        'DNT': '1',
        'Host': 'www.aaai.org',
        'Referer': f'https://www.aaai.org/ocs/index.php/AAAI/AAAI{year[-2:]}/paper/view/{code}',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    cookies_2 = {}


    headers_3 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'OCSSID=sjr2idatv41mfie8cqlgu44jc3',
        'DNT': '1',
        'Host': 'www.aaai.org',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }
    cookies_3 = {}

    if which == 1: return headers_1, cookies_1
    elif which == 2: return headers_2, cookies_2
    else: return headers_3, cookies_3


def KDD_headers_cookies(which = 2):
    # 1: get urls in kdd   2: download from acm
    headers_1={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'www.kdd.org',
        'If-Modified-Since': 'Thu, 16 Jan 2020 07:26:33 GMT',
        'Referer': 'https://www.kdd.org/kdd2019/accepted-papers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    cookies_1={
        'Cookie': 'exp_last_visit=1577351708; exp_csrf_token=c9dae914de4e747620980bde7af551844c9ccf1a; __atuvc=0%7C49%2C0%7C50%2C0%7C1%2C2%7C52%2C6%7C3; __atuvs=5e200fcdf2bda16c005; __atssc=google%3B9; exp_last_activity=1579160466; exp_tracker=%7B%220%22%3A%22kdd2019-temp%2Fassets%2Fvendor%2Fpopper.min.js.map%22%2C%221%22%3A%22accepted-papers%22%2C%222%22%3A%22kdd2019-temp%2Fassets%2Fvendor%2Fpopper.min.js.map%22%2C%223%22%3A%22accepted-papers%22%2C%224%22%3A%22kdd2019-temp%2Fassets%2Fvendor%2Fpopper.min.js.map%22%2C%22token%22%3A%228b83867b0bee10dd5a70f30a72d08d9f%22%7D',
    }
    
    headers_2={
        'authority': 'dl.acm.org',
        'method': 'GET',
        'path': '/doi/10.1145/3292500.3330975',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.kdd.org/kdd2019/accepted-papers/view/a-free-energy-based-approach-for-distance-metric-learning',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    cookies_2={
        'Cookie': '__cfduid=d2575d799789c47de63806df246dee5b51571835023; JSESSIONID=0536fc86-6085-4d21-b5a1-da0742b6a9b3; SERVER=WZ6myaEXBLEcXtPO7sb42g==; MAID=Dz83dvV5NxGh6b+Yq+nUfw==; MACHINE_LAST_SEEN=2020-01-15T23%3A26%3A41.139-08%3A00; cookiePolicy=accept; __atuvc=8%7C3; __atuvs=5e201032a13450b4007'
    }
    if which == 1: return headers_1, cookies_1
    else: return headers_2, cookies_2


def EMNLP_headers_cookies(year):
    headers ={
        'authority': 'www.aclweb.org',
        'method': 'GET',
        'path': f'/anthology/events/emnlp-{year}/',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'dnt': '1',
        'if-modified-since': 'Wed, 08 Jan 2020 21:25:02 GMT',
        'referer': 'https://www.aclweb.org/anthology/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',

    }
    cookies = {}
    return headers, cookies

def ICLR_headers_cookies(year):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'openreview.net',
        'Referer': f'https://openreview.net/group?id=ICLR.cc/{year}/Conference',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }
    cookies = {}
    return headers, cookies

def NIPS_headers_cookies():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'papers.nips.cc',
        'If-None-Match': '"a77d30b1f35c8de6a7b2881ed4d6b51c"',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    cookies = {}
    return headers, cookies

def ICML_headers_cookies():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Host': 'proceedings.mlr.press',
        'If-Modified-Since': 'Wed, 24 Oct 2018 16:09:15 GMT',
        'If-None-Match': 'W/"5bd0992b-3a7d"',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',       
    }
    cookies = {}
    return headers, cookies

def IJCAI_headers_cookies(year):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'has_js=1',
        'DNT': '1',
        'Host': 'www.ijcai.org',
        'Referer': f'https://www.ijcai.org/Proceedings/{year}/',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    cookies = {}
    return headers, cookies

def get_headers_cookies(org, year=None, which = 2, code = None):
    if org == 'ACL':
        return ACL_headers_cookies(year = year) if (int(year)<2020 and int(year)>2000) else None
    elif org == 'EMNLP':
        return EMNLP_headers_cookies(year = year)
    elif org == 'AAAI':
        return AAAI_headers_cookies(year = year, which = which, code = code)
    elif org == 'KDD':
        return KDD_headers_cookies(which = which)
    elif org == 'ICLR':
        return ICLR_headers_cookies(year = year)
    elif org == 'NIPS':
        return NIPS_headers_cookies()
    elif org == 'ICML':
        return ICML_headers_cookies()
    elif org == 'NAACL':
        return NAACL_headers_cookies()
    elif org == 'IJCAI':
        return IJCAI_headers_cookies(year = year)

def save_screenshot(url, file_name):
    from selenium import webdriver

    options = webdriver.ChromeOptions() 
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu') 
    options.add_argument("--no-sandbox") 
    driver = webdriver.Chrome(options=options,executable_path='./chromedriver')
    driver.get(url)
    driver.maximize_window()
    driver.get_screenshot_as_file(f'./ERROR_shot_{file_name}.png')
    driver.quit()

# fix pdf structure (occurs in AAAI papers)
# need to install qpdf (support both win and linux)
# make sure adding qpdf to win's PATH and using CMD terminal.
def fix_pdf(file_name, qpdf_path = "C:\\Program Files\\qpdf-9.1.0\\bin\\qpdf.exe"):
    if sys.platform != 'win32': qpdf_path = 'qpdf'
    temp_file = f'{file_name}.TEMP'
    subprocess.run([qpdf_path, "--linearize", file_name, temp_file])
    # print (res)
    # time.sleep(1)
    if not os.path.exists(temp_file): return False
    os.remove(file_name)
    os.rename(temp_file, file_name)
    return True



from pdfminer.high_level import extract_text
# pip install pdfminer.six    
def check_pdf(pdf_path):
    if not os.path.exists(pdf_path): return False
    try:
        _ = extract_text(pdf_path, maxpages=1, caching=True)
        return True
    except:
        # traceback.print_exc()
        print(f'BAD CHECK: {pdf_path}')
        try:
            fix_pdf(file_name = pdf_path, qpdf_path = 'qpdf')
            _ = extract_text(pdf_path, maxpages=1, caching=True)
            return True
        except:
            # traceback.print_exc()
            pass
        return False

from pdfminer.layout import LAParams
laparams=LAParams(
    line_overlap=0.5,
    char_margin=2.0,
    line_margin=0.5,
    word_margin=0.1,
    boxes_flow=0.5,
    detect_vertical=True,
    all_texts=True,
)


from func_timeout import func_timeout, FunctionTimedOut
# !pip install func_timeout

def time_out_wrap(time_out:int, do_function, *kwargs):
    try:
        doitReturnValue = func_timeout(time_out, do_function, args = kwargs)
        return doitReturnValue
    except FunctionTimedOut:
        print (f"{do_function.__name__}{kwargs} could not complete within {time_out} seconds and was terminated.")
    except:
        traceback.print_exc()
    return f"ERROR : time out. {do_function.__name__}{kwargs}.\n"


import pdfminer
def read_pdf(pdf_file_name):
    try: 
        err_message = None
        pdf_text = extract_text(pdf_file_name, laparams=laparams)
        return clean_text(pdf_text)
    except FileNotFoundError:
        err_message = f'ERROR NOFILE: {pdf_file_name}'
    except pdfminer.pdfparser.PDFSyntaxError:
        err_message = f'ERROR PDF: {pdf_file_name}'
    except:
        err_message = f'ERROR FILE: {pdf_file_name}'
    return err_message
    

def yield_tuples(pdfs_dict): # a dict
    for org_year in pdfs_dict:
        for pdf_name, pdf_url in pdfs_dict[org_year].items():
            yield (org_year, pdf_name, pdf_url)

def simple_clean_text(raw):
    raw = re.sub(r'[\\/:*?"<>|]', " ", raw)
    raw = re.sub(r' +',' ',raw)
    return raw.strip()

def clean_text(raw):
    raw = raw.replace('-\n','').replace('\n',' ').lower()
    raw = re.sub(r' +',' ',raw)
    # full-width character --> half-width
    def strQ2B(ustring):
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code == 12288:        
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):
                inside_code -= 65248
            rstring += chr(inside_code)
        return rstring
    
    # handle unseen char
    def unseen_char(ustring):
        return re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', ustring)

    return unseen_char(strQ2B(raw))

# find all rel paths
import os 
def listdir(path, list_name, extension_names = ['.pdf']):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name, extension_names)  
        elif os.path.splitext(file_path)[1] in extension_names:  
            list_name.append(file_path) 

from tqdm import tqdm
from multiprocessing import Pool
def check_all_pdfs(path = './'):
    file_paths = []
    listdir(path,file_paths)
    # file_paths = [i.replace('\\', '/') for i in file_paths]
    file_paths = [i for i in file_paths]

    bad_count = 0
    pbar = tqdm(total = len(file_paths), ncols=80)
    with Pool(8) as pool:
        pool_iter = pool.imap(check_pdf, file_paths)
        for r in pool_iter:
            if not r: bad_count += 1
            pbar.update()

    return bad_count


import hashlib
# create es index
def curlmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()

def split_path(path):
    # /home/d/papers_data/ACL/ACL_2016/xxx.pdf   
    split_slash = '\\' if sys.platform == 'win32' else '/'

    try:
        folder_name = path.split(split_slash)[-4]
        org = path.split(split_slash)[-3]
        org_year = path.split(split_slash)[-2]
        file_name = path.split(split_slash)[-1]
        return folder_name, org, org_year, file_name
    except:
        return f'ERROR: {path}'


if __name__ == "__main__":
    # bad_count = check_all_pdfs('/home/d/papers_data/')
    # print(f'bad_count: {bad_count}')
    # print(fix_pdf('/home/d/papers_data/ACL/ACL_2016/Multimodal Learning and Reasoning.pdf'))
    # print(check_pdf('/home/d/papers_data/ACL/ACL_2016/Multimodal Learning and Reasoning.pdf'))
    # a = read_pdf('AAAI/AAAI_2014/Deploying CommunityCommands  A Software Command Recommender System Case Study.pdf')
    # print(a)


    # err files:
    x1 = '/home/d/papers_data/EMNLP/EMNLP_2015/Online Updating of Word Representations for Part-of-Speech Tagging.pdf'
    x2 = '/home/d/papers_data/ACL/ACL_2018/Do Neural Network Cross-Modal Mappings Really Bridge Modalities .pdf'
    x3 = '/home/d/papers_data/ACL/ACL_2018/Event2Mind  Commonsense Inference on Events, Intents, and Reactions.pdf'
    x4 = '/home/d/papers_data/ACL/ACL_2019/Bilingual Lexicon Induction with Semi-supervision in Non-Isometric Embedding Spaces.pdf'

    # print(check_pdf(x1))
    # print(check_pdf(x2))
    # print(check_pdf(x3))

    for x in [x1]:
        r = read_pdf(x)
        print(f'len: {len(x)}. \n{r[:500]}')
    pass


