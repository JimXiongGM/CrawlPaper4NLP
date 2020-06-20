from utils import org_years_dict, listdir
import json, requests



def bulk_insert2ES(org, bulk_size = 100, json_file_folder = './txt2ES_json'):
    
    json_file_paths = []
    listdir(json_file_folder, json_file_paths, ['.json'])
    
    for path in json_file_paths:
        if path.split('\\')[-1].split('_')[0] != org: continue
    
        with open(path, 'r') as f1:
            bulk_content_lines = f1.readlines()
        
        url = f'http://localhost:9200/{org.lower()}/_bulk?pretty&refresh'
        headers = {'Content-Type': 'application/json'}
        for _index in range(0, len(bulk_content_lines), bulk_size*2):
            data = ''.join(bulk_content_lines[_index: _index + bulk_size*2]) + '\n'
            r = requests.post(url = url, headers = headers, data=data)
    print(f'{org} DONE!')
    return True

if __name__ == "__main__":
    bulk_insert2ES(org = 'ACL', bulk_size = 300)
    bulk_insert2ES(org = 'EMNLP', bulk_size = 300)
    bulk_insert2ES(org = 'AAAI', bulk_size = 300)
    bulk_insert2ES(org = 'ICLR', bulk_size = 300)
    bulk_insert2ES(org = 'ICML', bulk_size = 300)
    bulk_insert2ES(org = 'KDD', bulk_size = 300)
    bulk_insert2ES(org = 'NIPS', bulk_size = 300)
    bulk_insert2ES(org = 'NAACL', bulk_size = 300)
    bulk_insert2ES(org = 'IJCAI', bulk_size = 300)

    # bulk insert
    # for key in org_years_dict.keys():
    #     bulk_insert2ES(org = key, bulk_size = 300)

    # insert ADD file
    # for key in org_years_dict.keys():
    #     bulk_insert2ES(org = key, bulk_size = 1, json_file_folder = './papers_data_by_hand_good')

