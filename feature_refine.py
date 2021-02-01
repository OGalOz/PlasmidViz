#python3
#This file takes the list of features and adds in the gaps and removes
# the features people don't want to see
"""
Add removable features to config.json
Add in gap features
Add new ids
"""


def refine_features(py_feat_fp):


    return 0




"""
This function is designed to create a list of ids of length n.
Inputs:
    n (int)
Outputs:
    id_list: (list) list of IDs in format dldldl where d is a digit, and l is a letter.
"""
def create_id_list(n):
    id_list = []
    for i in range(n):
        new_id = create_new_id()
        while new_id in id_list:
            new_id = create_new_id()
        id_list.append(new_id)
    return id_list

def create_new_id():
        new_id = "{}{}{}{}{}{}".format(
                random.choice([str(k) for k in range(10)]),
                random.choice(string.ascii_letters),
                random.choice([str(k) for k in range(10)]),
                random.choice(string.ascii_letters),
                random.choice([str(k) for k in range(10)]),
                random.choice(string.ascii_letters))
        return new_id

