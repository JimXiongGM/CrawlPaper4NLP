from multiprocessing.dummy import Pool
import requests, json
from lxml import etree
from utils import get_headers_cookies

# pip install requests[socks] -U
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
proxies = None


def get_AAAI_urls(years, write_to_json = False):
    org = 'AAAI'
    res_dict = {}
    for year in years:
        start_url = f'https://www.aaai.org/Library/AAAI/aaai{year[-2:]}contents.php'
        names_list = []
        urls_list_1 = []
        pdf_download_url = []
        headers, cookies = get_headers_cookies(org = org, year=year, which = 1)
        with requests.Session() as s:
            response1 = s.get(start_url, headers = headers, cookies = cookies, proxies=proxies)
            x_path = '//a[contains(@href, "/paper/view/")]' if year != '2019' else '//a[text()="PDF"]/@href/../../a[1]'
            for item in etree.HTML(response1.text).xpath(x_path):
                name = item.xpath('text()')[0]
                names_list.append(name)
                urls_list_1.append(item.xpath('@href')[0].strip())

            print(len(urls_list_1))
            
            # multi-threadings
            def _get_pdf_url(zip_args):
                url = zip_args[0]
                headers = zip_args[1]
                cookies = zip_args[2]
                proxies = zip_args[3]
                import requests, time
                for retry in range(10):
                    with requests.Session() as s:
                        try:
                            response2 = s.get(url, headers = headers, cookies = cookies, proxies=proxies, allow_redirects=True, timeout = 30)
                            href = etree.HTML(response2.content).xpath('//a[contains(text(), "PDF")]/@href')[0]
                            return href
                        except IndexError:
                            if retry == 3: return f'ERROR :NO XPATH PDF: {url}'
                        except :
                            if retry == 3: return f'ERROR :response2 {url}'
                        time.sleep(1)
            # zip with urls_list_1
            if year != '2019':
                _url_list = [i.replace('view', 'viewPaper').replace('http://', 'https://') for i in urls_list_1]
            else:
                _url_list = [i.replace('http://', 'https://') for i in urls_list_1]

            _headers = [get_headers_cookies(org = org, year = year, which = 2, code = i.split('/')[-1])[0] for i in urls_list_1]
            _cookies = [get_headers_cookies(org = org, year = year, which = 2, code = i.split('/')[-1])[1] for i in urls_list_1]
            _proxies = [proxies for _ in urls_list_1]

            zip_args = zip(_url_list, _headers, _cookies, _proxies)
            with Pool(16) as pool:
                iters = pool.imap(_get_pdf_url, zip_args)
                for it in iters:
                    if 'ERROR ' in str(it): print(it)
                    else: pdf_download_url.append(it)

            print(len(pdf_download_url))
            org_year = f'{org}_{year}'
            res_dict[org_year] = {}
            for name,url in zip(names_list,pdf_download_url):
                res_dict[org_year][name] = url

    if not write_to_json: return res_dict
    temp = '_'.join(years)
    file_name = f'{org}_{temp}.json'
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(res_dict, f)
    print(f'DONE! write to: {file_name}')

def combine_json(years = [], write_to_json = True):
    res_dict = {}
    for year in years:
        with open(f'AAAI_{year}.json', 'r', encoding='utf8') as f1:
            res_dict.update(json.load(f1))
    if not write_to_json: return res_dict
    temp = '_'.join(years)
    org = 'AAAI'
    file_name = f'{org}_{temp}.json'
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(res_dict, f)
    print(f'DONE! write to: {file_name}')



if __name__ == "__main__":
    years = [str(i) for i in range(2014,2020)]
    for year in years:
        get_AAAI_urls([year], write_to_json = True)
    combine_json(years)
    