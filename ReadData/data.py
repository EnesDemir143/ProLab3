import time

import pandas as pd

start = time.time()
df = pd.read_excel("/Users/enesdemir/Desktop/ProLab3/Data/PROLAB 3 - GÜNCEL DATASET.xlsx",nrows=1000)
end = time.time()