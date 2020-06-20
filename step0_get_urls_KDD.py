import requests, json
from lxml import etree 
from utils import get_headers_cookies

# pip install requests[socks] -U
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}
proxies = None

def get_all_after_2016(years = ['2017', '2018', '2019'], write_to_json = False):
    # only for 2017 2018 2019
    org = 'KDD'
    res_dict = {}
    for year in years:
        start_url = f'https://www.kdd.org/kdd{year}/accepted-papers'
        names_list = []
        urls_list_1 = []
        urls_list_2 = []
        urls_list_3 = []
        headers_1, cookies_1 = get_headers_cookies(org, which = 1)
        headers_2, cookies_2 = get_headers_cookies(org, which = 2)
        with requests.Session() as s:
            response1 = s.get(start_url, headers = headers_1, cookies = cookies_1, proxies=proxies)
            x_path = '//a[contains(@href, "/papers/view/")]' if year == '2017' else '//div[@class="media-body"]/span/a'
            for item in etree.HTML(response1.text).xpath(x_path):
                names_list.append(item.xpath('string(.)'))
                urls_list_1.append(item.xpath('@href')[0])

            print(len(urls_list_1))
            for url in urls_list_1:
                response2 = s.get(url, headers = headers_1, cookies = cookies_1, proxies=proxies)
                href = etree.HTML(response2.text).xpath('//a[contains(@href,"authorize")]/@href')[0]
                urls_list_2.append(href)

            print(len(urls_list_2))
            for url in urls_list_2:
                response3 = s.get(url, headers = headers_2, cookies = cookies_2, proxies=proxies, allow_redirects=True)
                code1 = response3.url.split('/')[-2]
                code2 = response3.url.split('/')[-1]
                pdf_download_url = f'https://dl.acm.org/doi/pdf/{code1}/{code2}?download=true'
                urls_list_3.append(pdf_download_url)

            print(len(urls_list_3))
            org_year = f'{org}_{year}'
            res_dict[org_year] = {}
            for name,url in zip(names_list,urls_list_3):
                res_dict[org_year][name] = url

    if not write_to_json: return res_dict
    temp = '_'.join(years)
    file_name = f'{org}_{temp}.json'
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(res_dict, f)
    print(f'DONE! write to: {file_name}')

if __name__ == "__main__":
    get_all_after_2016(write_to_json=True)