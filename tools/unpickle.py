import sys
import pickle
import numpy as np

filename = sys.argv[1]

with open(filename, 'rb') as f:
    img_array = pickle.load(f)

print(f"Array dimensions: {img_array.shape}")
# print(img_array)
# txtfile_path = "../logs/unpickle.txt"
# with open(txtfile_path, 'w') as file:
#     file.write(np.array2string(img_array, separator=',', threshold=sys.maxsize))
