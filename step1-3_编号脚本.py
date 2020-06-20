import os, re, json
def listdir(path, list_name, extension_name = ['.pdf']):  
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            listdir(file_path, list_name, extension_name)  
        elif os.path.splitext(file_path)[1] in extension_name:  
            list_name.append(file_path) 

def rename2order(folder_path = './'):
    all_paths = []
    pdf2txt = {}
    listdir(folder_path, all_paths, extension_name = ['.pdf'])
    # 获取org_year
    dirname_set = set([os.path.dirname(path) for path in all_paths])
    # print(dirname_set)
    for dirname in dirname_set:
        index = 1
        for path in all_paths:
            if not path.startswith(dirname): continue
            pdf_name = os.path.basename(path)
            to_path = path.replace(pdf_name, f'@{index}@.pdf')
            index += 1
            pdf2txt[path] = to_path
            os.rename(path, to_path)
    with open('./pdf2txt.json', 'w', encoding='utf8') as f:
        json.dump(pdf2txt, f)
    print('rename2order DONE')


def rename2name(json_path = './pdf2txt.json'):
    with open(json_path, 'r', encoding='utf8') as f:
        txt2pdf = json.loads(f.read().replace('.pdf"', '.txt"'))

    for _to, _from in txt2pdf.items():
        os.rename(_from, _to)
    print('rename2name DONE')


def remove_pdf(folder_path = './'):
    all_paths = []
    listdir(folder_path, all_paths, extension_name = ['.pdf'])
    for path in all_paths:
        os.remove(path)
    print('remove_pdf DONE')    

if __name__ == "__main__":
    # rename2order('./test/')
    rename2name('./papers_data')
    # remove_pdf('./test/')