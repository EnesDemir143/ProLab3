import time
from dis import UNKNOWN

import pandas as pd

class Author:
    def __init__(self,name="Unknown"):
        self.name = name
        self.article= set();




if __name__=='__main__':

    start = time.time()
    df = pd.read_excel("/Users/enesdemir/Desktop/ProLab3/Data/PROLAB 3 - DATASET.xlsx")
    end = time.time()

    ids=set()
    authorsObjects=[]

    for id,name in zip(df["orcid"],df["author_name"]):
        if id not in ids:
            ids.add(id)
            authorsObjects.append(Author(name))



    print(len(authorsObjects))
    print(len(ids))


