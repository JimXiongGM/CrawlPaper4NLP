import requests,os 
from utils import get_headers_cookies, simple_clean_text

proxies = {'http': 'socks5://127.0.0.1:1080','https': 'socks5://127.0.0.1:1080'}

# 手动处理AAAI的遗漏情况
def _dw(name , url):
    urls = []
    urls.append(url)
    # urls.append(url.replace('AAAI', 'IAAI'))
    urls.append(url.replace('IAAI', 'EAAI'))

    for _url in urls:
        headers, cookies = get_headers_cookies('AAAI', '2014', 3)    
        r = requests.get(_url, headers=headers, proxies = proxies)
        print(f'len: {len(r.content)}.\t{name} ')
        if len(r.content) > 100: return r.content
    print(f'ERROR : {name} {urls}')
    return False


folder = './papers_data'

def test():
    with open('DownLoad_Errors_2020-01-25_14-55-10.log', 'r', encoding='utf-8') as f:
        err_file = f.read().strip().replace('ERROR AFTER RETRY:', '').split('\n')
    for line in err_file:
        line = line[1:-2].split('\', \'')
        org_year = line[0]
        org = org_year.split('_')[0]
        pdf_name = simple_clean_text(line[1])
        url = line[2].strip()
        
        # print(pdf_name, url)
        # break
        res = _dw(pdf_name, url)
        if not res: continue
        if not os.path.exists(f'{folder}/{org}/{org_year}'): os.makedirs(f'{folder}/{org}/{org_year}')
        file_name = f'{folder}/{org}/{org_year}/{pdf_name}.pdf'
        with open(file_name, 'wb') as f1:
            f1.write(res)
    print('DONE! ')
    return None

if __name__ == "__main__":
    test()


