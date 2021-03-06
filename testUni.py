import sys
import numpy as np
import trainUni
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import matplotlib.pyplot as plt

fileTypes = [ 'pdf', 'html', 'jpg', 'png', 'doc', 'txt', 'xls', 'gif', 'xml', 'ps', 'csv']

def test(training_file, testing_file):
    X,y = trainUni.process_training_examples(training_file)
    X_test, y_test = trainUni.process_training_examples(testing_file)

    acc_list = []

    lin_svm = trainUni.train_linear_svm(X, y)
    linear_svm_accuracy = test_with(lin_svm, X_test, y_test)
    print("LinearSVM accuracy = {}%".format(100 * linear_svm_accuracy))
    acc_list.append(linear_svm_accuracy)

    rbf_svm = trainUni.train_rbf_svm(X, y)
    rbf_svm_accuracy = test_with(rbf_svm, X_test, y_test)
    print("RBF-SVM accuracy = {}%".format(100 * rbf_svm_accuracy))
    acc_list.append(rbf_svm_accuracy)

    mlp_accuracy = trainUni.mlp(X, y, X_test, y_test, "uniModel"+sys.argv[1]+".hdf5")
    acc_list.append(mlp_accuracy)

    ff = open("results/Uni"+sys.argv[1]+".csv", 'a')
    line = ','.join([ str(x) for x in acc_list ])
    ff.write(line + "\r\n")

    #Print SVM confusion matrix
    # y_pred = rbf_svm.predict(X_test)
    # cm = plot_confusion_matrix(rbf_svm, X_test, y_test)
    # print(cm)
    # plt.matshow(cm)
    # plt.title('Confusion matrix for SVM Classification of File Fragment Types')
    # plt.colorbar()
    # plt.ylabel('True File Type')
    # plt.xlabel('Predicted File Type')
    # plt.show()

def test_with(classifier, X, y):
    correct_count = 0
    for i in range(len(y)):
        test_vec = np.reshape(X[i], (1, -1), order = 'C')
        label = y[i]
        expected_label = classifier.predict(test_vec)
        if label == expected_label:
            correct_count += 1
    return float(correct_count) / len(y)

if __name__ == "__main__":
    print("Training data: {}\tTesting data: {}".format(sys.argv[1], sys.argv[1]))
    test('csvs/train'+sys.argv[1]+".csv", 'csvs/test'+sys.argv[1]+".csv")