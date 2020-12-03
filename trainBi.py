import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

import numpy as np
import pandas as pd
import sys
from sklearn import svm
# from sklearn.neural_network import MLPClassifier
import tensorflow
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

TRAINING_DATA_FILE = "train.csv"
NUM_CATEGORIES = 13

fileTypes = [ 'pdf', 'html', 'bmp', 'jpg', 'rtf', 'png', 'doc', 'txt', 'xls', 'gif', 'xml', 'ps', 'csv']

def process_training_examples(filename):
    X = []
    y = []
    with open(filename, 'r') as training_data:
        while True:
            line = training_data.readline().rstrip()
            if line == "":
                break
            data = np.asarray([ float(x) for x in line.split(',')[:-1] ])
            X.append(data[:])
            y.append(line.split(',')[-1])
    print("We have now processed all {} training examples".format(len(y)))
    return X, y

def train_linear_svm(X, y):
    clf = svm.LinearSVC(penalty='l2', loss='squared_hinge', dual=False, C=100.0)
    clf.fit(X, y)
    return clf

def train_rbf_svm(X, y):
    clf = svm.SVC(kernel="rbf", C=100.0)
    clf.fit(X, y)
    return clf

def mlp(X, y, X_test, y_test, modelName):
    y_testOG = y_test[:]
    X = np.asarray(X)
    X_test = np.asarray(X_test)
    model = Sequential()
    model.add(Dense(1024, input_shape=(256*256,), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(13, activation='softmax'))
    model.summary()

    f = lambda y : fileTypes.index(y)
    y = [f(i) for i in y]
    y = np.asarray(y)
    y = to_categorical(y, 13)
    y_test = [f(i) for i in y_test]
    y_test = to_categorical(y_test, 13)

    checkpoint = ModelCheckpoint(
        modelName,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        period=1,
        verbose=1
    )   
    model.compile(
        tensorflow.keras.optimizers.Adam(lr=0.00025, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    model.fit(
        X,
        y,
        epochs=1,
        validation_data=(X_test, y_test),
        callbacks=[checkpoint],
        verbose=1
    )
    
    model = tensorflow.keras.models.load_model(modelName)
    y_pred = list(np.argmax(model.predict(X_test), axis=-1))
    y_testOG = [f(i) for i in y_testOG]
    # con_mat = tensorflow.math.confusion_matrix(labels=y_test, predictions=y_pred).np()
    # con_mat_norm = np.around(con_mat.astype('float'))
    # con_mat_df = pd.DataFrame(con_mat_norm,index = classes, columns = classes)
    # print(con_mat_df)

    score = model.evaluate(X_test, y_test)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1]*100)
    return score[1]