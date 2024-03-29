import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC


def find_acc_rf():
    data=pd.read_csv(r"C:\Users\fzuha\Desktop\zeugar\project\PycharmProjects\PycharmProjects1\PycharmProjects\alzher\static\features.csv")

    #   Extract attributes and labels
    attributes = data.values[1:, 0:5]
    labels = data.values[1:, 5]

    #   Split attributes and labels
    X_train, X_test, Y_train, Y_test = train_test_split(attributes, labels, test_size=0.2)
    svm=LinearSVC()
    svm.fit(X_train, Y_train)

    #   Predict result
    pred=svm.predict(X_test)

    print("Original Result\t\tPredicted Result")
    for i in range(len(pred)):
        print(Y_test[i], "\t\t", pred[i])

    #   Find accuracy score
    acc=accuracy_score(Y_test, pred)
    print("\nAccuracy : ", round(acc*100, 2), "%")

find_acc_rf()