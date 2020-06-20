from utils import yield_tuples, clean_text, read_pdf
import json, os, re, time, logging, sys, traceback
# from multiprocessing import Pool
from pathos.pools import ProcessPool as Pool
from pdfminer.high_level import extract_text
import pdfminer


def count_keywords_in_one_pdf(file_tuple,
                              keywords_list,
                              use_cashed=True
                              ):
    
    # for multi-process
    from utils import yield_tuples, clean_text, read_pdf
    import json, os, re, time, logging, sys, traceback
    # from multiprocessing import Pool
    from pathos.pools import ProcessPool as Pool
    from pdfminer.high_level import extract_text
    import pdfminer


    if file_tuple[1].startswith('Proceedings'):
        return None
    org, year = file_tuple[0].split('_')
    name = re.sub(r'[\\/:*?"<>|]', " ", file_tuple[1].strip())

    if not (os.path.exists(f'cleaned_data/{org}/{file_tuple[0]}/{name}.pdf')
            and use_cashed):
        if not os.path.exists(f'cleaned_data/{org}/{file_tuple[0]}'):
            os.makedirs(f'cleaned_data/{org}/{file_tuple[0]}')
        
        # some pdfs cant be downloaded. just skip.
        pdf_file_name = f'{org}/{file_tuple[0]}/{name}.pdf'
        pdf_text = read_pdf(pdf_file_name)
        if 'ERROR ' in pdf_text: return pdf_text

        pdf_text = clean_text(pdf_text)
        with open(f'cleaned_data/{org}/{file_tuple[0]}/{name}.txt',
                  'w',
                  encoding='utf8') as cash_file:
            cash_file.write(pdf_text)
    else:
        with open(f'cleaned_data/{org}/{file_tuple[0]}/{name}.txt',
                  'rb') as cash_file:
            pdf_text = cash_file.read()

    key_words_counts = {k: pdf_text.count(k) for k in keywords_list}
    one_line = [name, org, year]
    one_line.extend([key_words_counts[k] for k in key_words_counts.keys()])
    return one_line

from tqdm import tqdm
def run_count(keywords_list, url_path, use_cashed=True, process_num=8):

    if len(keywords_list) == 0: return None
    keywords_list = [
        clean_text(i)
        for i in sorted(set(keywords_list), key=keywords_list.index)
    ]
    res = [['Name', 'Org', 'Year']]
    res[0].extend(keywords_list)

    with open(url_path,'r') as f:
        pdf_tuples_list = [i for i in yield_tuples(json.load(f))]

    keywords_list = [keywords_list for _ in pdf_tuples_list]

    errs = []
    with tqdm(total=len(pdf_tuples_list), ncols=80) as pbar:
        with Pool(process_num) as pool:
            pool_iter = pool.imap(count_keywords_in_one_pdf, pdf_tuples_list, keywords_list)
            for r in pool_iter:
                # print(r)
                if 'ERROR' in str(r): errs.append(r)
                elif r: res.append(r) # not None
                pbar.update()

    if len(errs) != 0:
        time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        with open(f'FIND ERR_{time_now}.log', 'w', encoding='utf8') as err_file:
            for i in errs:
                err_file.write(f'{i}\n')
    return res


# write to excel
def write_to_excel(res):
    from openpyxl import Workbook
    wb = Workbook()
    sheet = wb.create_sheet('result', index=0)
    for line in res:
        sheet.append(line)
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    wb.save(f'res_{time_now}.xlsx')


def main(url_path = 'ACL_pdfs_all.json'):
    keywords_list = ['Free917', 'WebQuestions', 'QALD', 'Factoid Questions', 'QuAD', 'New York Times Corpus', 'Semval-2010', 'FewRel', 'TACRED', 'CoNLL04']
    
    start_time = time.time()
    res = run_count(keywords_list, url_path, use_cashed=True, process_num=4)
    write_to_excel(res)
    end_time = time.time()
    time.sleep(0.3)
    print(f'\ntime cost: {end_time - start_time:0.4f} s')




if __name__ == "__main__":
    # main(url_path = 'ACL_2014_2015_2016_2017_2018_2019.json.json') # OK
    main(url_path = 'EMNLP_pdfs_all.json')
