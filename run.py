import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow
import numpy as np
model = tensorflow.keras.models.load_model('BiModel1.hdf5')

fileTypes = [ 'pdf', 'html', 'bmp', 'jpg', 'rtf', 'png', 'doc', 'txt', 'xls', 'gif', 'xml', 'ps', 'csv', 'gz']
X = []

with open('run.csv') as testing_data:
    line = testing_data.readline().rstrip()
    data = np.asarray([ float(x) for x in line.split(',') ])
    X.append(data[:])

ans = model.predict(x=np.asarray(X))[0].tolist()
index = ans.index(max(ans))
print(fileTypes[index])