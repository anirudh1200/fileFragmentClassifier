import sys
import numpy as np
import train
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def test(training_file, testing_file):
    X,y = train.process_training_examples(training_file)
    X_test, y_test = train.process_training_examples(testing_file)

    lin_svm = train.train_linear_svm(X, y)
    linear_svm_accuracy = test_with(lin_svm, X_test, y_test)
    print("LinearSVM has classification accuracy of {}%".format(100 * linear_svm_accuracy))

    rbf_svm = train.train_rbf_svm(X, y)
    rbf_svm_accuracy = test_with(rbf_svm, X_test, y_test)
    print("RBF-SVM has classification accuracy of {}%".format(100 * rbf_svm_accuracy))

    nbc = train.train_naive_bayes(X, y)
    nb_accuracy = test_with(nbc, X_test, y_test)
    print("Multinomial Naive Bayes has classification accuracy of {}%".format(100 * nb_accuracy))

    lda = train.train_lda(X, y)
    lda_accuracy = test_with(lda, X_test, y_test)
    print("LDA has classification accuracy of {}%".format(100 * lda_accuracy))

    #Print SVM confusion matrix
    y_pred = lin_svm.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    plt.matshow(cm)
    plt.title('Confusion matrix for SVM Classification of File Fragment Types')
    plt.colorbar()
    plt.ylabel('True File Type')
    plt.xlabel('Predicted File Type')
    plt.show()

def test_with(classifier, X, y):
    correct_count = 0
    for i in range(len(y)):
        test_vec = np.reshape(X[i], (1, -1), order = 'C')
        label = y[i]
        expected_label = classifier.predict(test_vec)
        if label == expected_label:
            correct_count += 1
    return float(correct_count) / len(y)

def print_usage():
    print("Usage: {} training_data.csv testing_data.csv".format(sys.argv[0]))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(0)
    print("Training data: {}\tTesting data: {}".format(sys.argv[1], sys.argv[2]))
    test(sys.argv[1], sys.argv[2])
