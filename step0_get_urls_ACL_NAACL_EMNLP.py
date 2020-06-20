import requests, json
from lxml import etree 
from utils import get_headers_cookies 

def get_ACL_all_pdf_urls(year):
    headers, _ = get_headers_cookies(org = 'ACL', year = year)
    url = f'https://www.aclweb.org/anthology/events/acl-{year}/'
    with requests.Session() as s:
        response = s.get(url, headers = headers)
        print(f'{year} status code: {response.status_code}')
    pdf_urls_dict = {}
    for node in etree.HTML(response.text).xpath('//a[contains(@href, ".pdf")]/../..//strong'):
        name = node.xpath('string(a)').strip()
        if name.startswith('Proceedings of') : continue
        url = 'https://www.aclweb.org' + node.xpath('a/@href')[0][:-1] + '.pdf'
        if url not in pdf_urls_dict.values(): pdf_urls_dict[name] = url
    print (f'len: {len(pdf_urls_dict.items())}')
    return pdf_urls_dict

def get_ACL_papers(years = ['2019']):
    res_dict = {}
    for year in years:
        res_dict[f'ACL_{year}'] = get_ACL_all_pdf_urls(year)
    return res_dict

def get_ACL(from_year = 2014, to_year = 2020):
    ACL_pdfs_all = get_ACL_papers([str(i) for i in range(from_year, to_year)])
    _years = '_'.join([str(i) for i in range(from_year,to_year)])
    with open(f'./ACL_{_years}.json', 'w') as f:
        json.dump(ACL_pdfs_all, f)
    print('ACL DONE!')

# NAACL
def get_NAACL_all_pdf_urls(year):
    headers, _ = get_headers_cookies(org = 'ACL', year = year)
    url = f'https://www.aclweb.org/anthology/events/naacl-{year}/'
    with requests.Session() as s:
        response = s.get(url, headers = headers)
        print(f'{year} status code: {response.status_code}')
    pdf_urls_dict = {}
    for node in etree.HTML(response.text).xpath('//a[contains(@href, ".pdf")]/../..//strong'):
        name = node.xpath('string(a)').strip()
        if name.startswith('Proceedings of') : continue
        url = 'https://www.aclweb.org' + node.xpath('a/@href')[0][:-1] + '.pdf'
        # print (url, name)
        if url not in pdf_urls_dict.values(): pdf_urls_dict[name] = url
    print (f'{year} len: {len(pdf_urls_dict.items())}')
    return pdf_urls_dict

def get_NAACL_papers(years = ['2019']):
    res_dict = {}
    for year in years:
        res_dict[f'NAACL_{year}'] = get_NAACL_all_pdf_urls(year)
    return res_dict

def get_NAACL(from_year = 2014, to_year = 2020, skip_year = ['2017', '2014']):
    NAACL_pdfs_all = get_NAACL_papers([str(i) for i in range(from_year, to_year) if str(i) not in skip_year])
    _years = '_'.join([str(i) for i in range(from_year,to_year)])
    with open(f'./NAACL_{_years}.json', 'w') as f:
        json.dump(NAACL_pdfs_all, f)
    print('NAACL DONE!')
    
    
# EMNLP
def get_EMNLP_all_pdf_urls(year):
    headers, _ = get_headers_cookies(org = 'ACL', year = year)
    url = f'https://www.aclweb.org/anthology/events/emnlp-{year}/'
    with requests.Session() as s:
        response = s.get(url, headers = headers)
        print(f'{year} status code: {response.status_code}')
    pdf_urls_dict = {}
    for node in etree.HTML(response.text).xpath('//a[contains(@href, ".pdf")]/../..//strong'):
        name = node.xpath('string(a)').strip()
        if name.startswith('Proceedings of') : continue
        url = 'https://www.aclweb.org' + node.xpath('a/@href')[0][:-1] + '.pdf'
        # print (url, name)
        if url not in pdf_urls_dict.values(): pdf_urls_dict[name] = url
    print (f'len: {len(pdf_urls_dict.items())}')
    return pdf_urls_dict

def get_EMNLP_papers(years = ['2019']):
    res_dict = {}
    for year in years:
        res_dict[f'EMNLP_{year}'] = get_EMNLP_all_pdf_urls(year)
    return res_dict

def get_EMNLP(from_year = 2014, to_year = 2020):
    EMNLP_pdfs_all = get_EMNLP_papers([str(i) for i in range(from_year, to_year)])
    _years = '_'.join([str(i) for i in range(from_year,to_year)])
    with open(f'./EMNLP_{_years}.json', 'w') as f:
        json.dump(EMNLP_pdfs_all, f)
    print('EMNLP DONE!')

if __name__ == "__main__":
    # get_ACL(from_year = 2014, to_year = 2020)
    # get_EMNLP(from_year = 2014, to_year = 2020)
    get_NAACL()