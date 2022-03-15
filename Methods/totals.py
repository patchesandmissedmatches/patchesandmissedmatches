import pickle
from pprint import pprint


def read_totals(repo_file, mainline):
    with open('Repos_totals/' + str(repo_file) + '_' + mainline.split('/')[0] + '_' + mainline.split('/')[1] + '_totals.pkl', 'rb') as f:
        return pickle.load(f)

def print_totals(dict_file):
    pprint(dict_file)
    
    
"""
    We need to get the final final decision for each PR based on the number of ED and MO there are. 
    We will also store the number of non-existant files and files with other extensions than the code can handle
"""
def final_class(result_dict): 
    total_ED = 0
    total_MO = 0
    total_SP = 0
    total_NE = 0
    total_OE = 0
    total_E = 0
    total_NA = 0

    pr_classes = {}

    for pr in result_dict:
        pr_classes[pr] = {
            'total_ED' : 0,
            'total_MO' : 0,
            'total_SP' : 0,
            'total_NE' : 0,
            'total_OE' : 0,
            'total_E'  : 0,
            'total_NA' : 0,
            'total_ERROR' : 0,
            'class': ''
        }

        total_ED = 0
        total_MO = 0
        total_SP = 0
        total_NE = 0
        total_OE = 0
        total_E  = 0
        total_NA = 0
        total_ERROR = 0
                    
        for file in result_dict[pr]:
            try:
                class_ = result_dict[pr][file]['result']['patchClass']
                if class_ == 'OTHER EXT':
                    total_OE += 1
                elif class_ == 'NOT EXISTING':
                    total_NE += 1
                elif class_ == 'MO':
                    total_MO += 1
                elif class_ == 'ED':
                    total_ED += 1
                elif class_ == 'SP':
                    total_SP += 1
                elif class_ == 'NA':
                    total_NA += 1
                elif class_ == 'ERROR':
                    total_ERROR += 1
            except:
                total_ERROR += 1
            total_E += 1
            
            
        if total_MO==0 and total_ED==0 and total_SP==0:
            _max = total_NA
            _max_title = 'NA'
            ultimate_class = 'NA'
            if _max < total_OE:
                _max = total_OE
                ultimate_class = 'CC'
                _max_title = 'CC'
            if _max < total_NE:
                _max = total_NE
                ultimate_class = 'NE'
                _max_title = 'NE'
            if _max < total_ERROR:
                _max = total_ERROR
                ultimate_class = 'ERROR'
                _max_title = 'ERROR'
        else:
            _max = total_ED
            _max_title = 'ED'
            ultimate_class = 'ED'
            if _max < total_MO:
                _max = total_MO
                ultimate_class = 'MO'
                _max_title = 'MO'
            if _max < total_SP:
                _max = total_SP
                ultimate_class = 'SP'
                _max_title = 'SP'
            
            if total_MO == total_ED:
                _max = total_SP
                ultimate_class= 'SP'
                _max_title = 'SP'
        
        pr_classes[pr] = {
                'totals':
                    {
                        'total_ED' : total_ED,
                        'total_MO' : total_MO,
                        'total_SP' : total_SP,
                        'total_NE' : total_NE,
                        'total_OE' : total_OE,
                        'total_E'  : total_E,
                        'total_NA' : total_NA,
                        'total_ERROR': total_ERROR
                    },
            'class': ultimate_class
        }
    return pr_classes

def count_all_classifications(pr_classes):
    all_classes = {}

    all_classes['MO']=0
    all_classes['ED']=0
    all_classes['SP']=0
    all_classes['CC']=0
    all_classes['NA']=0
    all_classes['NE']=0
    all_classes['ERROR']=0
    
    for i in pr_classes:
        v = pr_classes[i]['class']
        if v ==  'NE':
            all_classes['NE'] += 1
        elif v == 'NA':
            all_classes['NA'] += 1
        elif v == 'SP':
            all_classes['SP'] += 1
        elif v == 'MO':
            all_classes['MO'] += 1
        elif v == 'ED':
            all_classes['ED'] += 1
        elif v == 'CC':
            all_classes['CC'] += 1
        elif v == 'ERROR':
            all_classes['ERROR'] += 1
    return all_classes