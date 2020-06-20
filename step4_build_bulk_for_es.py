from utils import read_pdf, listdir, org_years_dict, curlmd5, time_out_wrap, gen_files_path_from_dict, split_path, clean_text
import json, os, re, shutil, collections
from tqdm import tqdm
from multiprocessing import Pool
# from pathos.multiprocessing import Pool
import time, traceback

manual_processing_folder = '/home/d/github_work/find_papers_by_datasets/papers_data_by_hand'

cant_dw_list = ['Binarized Back-Propagation Training Binarized Neural Networks with Binarized Gradients.pdf',
               'TV Advertisement Scheduling by Learning Expert Intentions.pdf',
               'Whole Page Optimization with Global Constraints.pdf']

def _dumps_pdf(file_path):

    def __dumps_pdf(file_path):
        try:
            json_body = {}
            json_body['Organization'] = file_path.split('/')[4]
            json_body['Name'] = file_path.split('/')[-1].split('.pdf')[0]
            json_body['Year'] = file_path.split('/')[5].split('_')[1]
            json_body['Text'] = read_pdf(file_path)
            if json_body['Text'].startswith('ERROR '): return json_body['Text']

            json_start = '{"index":{"_id":\"' + curlmd5(json_body['Name']) + '\"}}'

            json_body = json_start + '\n' + json.dumps(json_body) + '\n'
            return json_body
        except:
            traceback.print_exc()
            return f'ERROR : {file_path}'
        
    # add timeout err
    return time_out_wrap(100, __dumps_pdf, file_path)


def dumps_pdf(org, years, file_paths, folder_name = 'pdf_es_json', use_multi = True, auto_gen = False):
    
    file_paths = [i for i in file_paths if i.split('/')[-3] == org]

    start_time = time.time()
    res_json_text = []
    res_err = []    

    if not os.path.exists(folder_name): os.mkdir(folder_name)
    if use_multi:
        pbar = tqdm(total = len(file_paths), ncols = 100, desc = f'multi mode: {org}')
        with Pool(4) as pool:
            pool_iter = pool.imap(_dumps_pdf, file_paths)
            for i,r in enumerate(pool_iter):
                if not r.startswith('ERROR '):
                    res_json_text.append(r)
                else:
                    res_err.append(r)
                    print(r)
                pbar.update()
    
    # for test
    else:
        for file_path in tqdm(file_paths, ncols = 100, desc = f'single mode: {org}'):
            r = _dumps_pdf(file_path)
            if not r.startswith('ERROR '):
                res_json_text.append(r)
            else:
                print(r)
    
    # res
    _years = '_'.join(years)        
    with open(f'./{folder_name}/{org}_{_years}.json', 'w', encoding='utf8') as f:
        for i in res_json_text:
            f.write(i)

    # err
    _years = '_'.join(years)        
    with open(f'./{folder_name}/ERR_{org}_{_years}.txt', 'w', encoding='utf8') as f:
        for i in res_err:
            f.write(i)    
    
    end_time = time.time()
    print(f'time cost: {end_time - start_time:.1f}s.')

    # auto-gen err pdf-txt pair files for mamul processing/
    if auto_gen:
        with open(f'./{folder_name}/ERR_{org}_{_years}.txt', 'r', encoding='utf8') as f:
            t = f.read()
        patten = re.compile(r'/home/d/(.*?).pdf')  # papers_data/ACL/ACL_2018/xxxxx
        res1 = patten.findall(t)
        for path in res1:
            folder, org, org_year, name = path.split('/')
            pdf_name = name + '.pdf'
            if pdf_name in cant_dw_list: continue
            new_foolder = folder + '_by_hand'
            
            if not os.path.exists(f'{new_foolder}'): os.makedirs(f'{new_foolder}')
            
            _file_from = f'/home/d/{folder}/{org}/{org_year}/{pdf_name}'
            _file_to = f'{new_foolder}/{org_year}@@@{pdf_name}'
            shutil.copy(_file_from, _file_to)
            txt_name = name + '.txt'
            with open(f'{new_foolder}/{org_year}@@@{txt_name}', 'w') as f:
                f.write('')

    return None


def add_from_txt(txt_folder_name = r'..\..\papers_data'):


    file_paths = []
    listdir(txt_folder_name, file_paths, ['.txt'])
    start_time = time.time()
    res_json_text = []
    org_years = collections.defaultdict(set)   # for json name.
    for txt_file_path in tqdm(file_paths, ncols = 100, desc = f'process txts'):
        folder_name, org, org_year, file_name = split_path(txt_file_path)
        
        name = file_name.split('.txt')[0]
        year = org_year.split('_')[1]

        json_body = {}
        json_body['Organization'] = org
        json_body['Name'] = name
        json_body['Year'] = year

        with open(txt_file_path, 'r', encoding='utf8') as f:
            json_body['Text'] = clean_text(f.read())

        json_start = '{"index":{"_id":\"' + curlmd5(json_body['Name']) + '\"}}'
        json_body = json_start + '\n' + json.dumps(json_body) + '\n'
        res_json_text.append([org, json_body])
        org_years[org].add(year)
    
    out_folder = 'txt2ES_json'
    if not os.path.exists(out_folder): os.mkdir(out_folder)
    for _org in org_years.keys():
        org_years[_org] = '_'.join(sorted(org_years[_org]))
        with open(f'./{out_folder}/{_org}_{org_years[_org]}.json', 'w', encoding='utf8') as f:
            for __org, _json_body in res_json_text:
                if __org == _org: f.write(_json_body)
 
    
    end_time = time.time()
    print(f'time cost: {end_time - start_time:.2f}s.')
    return None



if __name__ == "__main__":

    # check first
    # from utils import check_all_pdfs
    # check_all_pdfs(path = '/home/d/papers_data/')
    # exit()
    
    # from utils import check_all_pdfs

    # bad_count = check_all_pdfs('/home/d/papers_data/')
    # print(f'bad_count: {bad_count}')
    
    # # all files' path
    # file_paths = gen_files_path_from_dict(json_files_path = './url_json/', base_url = '../../papers_data')

    # dumps_pdf('ACL', org_years_dict['ACL'], file_paths)
    # dumps_pdf('AAAI', org_years_dict['AAAI'], file_paths)
    # dumps_pdf('EMNLP', org_years_dict['EMNLP'], file_paths)
    # dumps_pdf('ICLR', org_years_dict['ICLR'], file_paths)
    # dumps_pdf('ICML', org_years_dict['ICML'], file_paths)
    # dumps_pdf('KDD', org_years_dict['KDD'], file_paths)
    # dumps_pdf('NIPS', org_years_dict['NIPS'], file_paths)
    # dumps_pdf('IJCAI', org_years_dict['IJCAI'], file_paths)
    
    add_from_txt()
