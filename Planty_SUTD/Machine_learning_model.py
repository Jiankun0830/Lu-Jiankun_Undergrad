from sklearn.model_selection import train_test_split
from sklearn import neighbors, datasets
from sklearn.metrics import confusion_matrix
import numpy as np
import pickle
import random
import json

def get_metrics(actual_targets, predicted_targets, labels):
    '''
        a function that takes in two arrays representing actual targets and prediicted targets respectively and
        returns a dictionary containing the confusion matrix, accuracy, sensitivity and false positive rate
    '''
    c_matrix = confusion_matrix(actual_targets, predicted_targets, labels)
    total = float(sum(sum(c_matrix)))
    correct_predictions = float(c_matrix[0][0] + c_matrix[1][1])
    correct_positives = float(c_matrix[1][1])
    total_negatives = float(sum(c_matrix[0, :]))
    total_positives = float(sum(c_matrix[1, :]))
    false_positives = float(c_matrix[0][1])

    output = {
        'confusion matrix': c_matrix,
        'total records': int(total),
        'accuracy': round(correct_predictions / total, 3),
        'sensitivity': round(correct_positives / total_positives, 3),
        'false positive rate': round(false_positives / total_negatives, 3)}
    return output

def normalize_minmax(data):
    """
        a function that takes in one numpy arrays, normalize it using the min/max normalization and returns the normalized array.
    """
    size = data.shape

    if (len(size) == 1):
        columns = 1
    else:
        columns = size[1]

    for i in range(columns):
        maximum = np.max(data[:, i])
        minimum = np.min(data[:, i])
        denominator = maximum - minimum

        data[:, i] = (data[:, i] - minimum) / denominator

    return data



def knn_classifier_full(bunchobject, feature_list, size = 0.2, seed = random.randint(1,5000)):
    '''
        find the best k and save a model that decide whether to water or not
    '''
    data = bunchobject['data'][:, feature_list]
    target = bunchobject['target']
    data = normalize_minmax(data)

    data_train, data_part2, target_train, target_part2 = train_test_split( data , target , test_size = size, random_state = seed )
    data_validation, data_test, target_validation, target_test = train_test_split( data_part2 , target_part2 , test_size = 0.5, random_state = seed )

    acc = [0]
    confm = [{}]
    for k in range(1,20):
        clf = neighbors.KNeighborsClassifier(k)
        clf.fit(data_train, target_train)
        target_predicted = clf.predict(data_validation)
        results = get_metrics(target_validation, target_predicted, [0, 1])
        confm.append(results)
        acc.append(results['accuracy'])

    best_k = acc.index(max(acc))
    best_confm = confm[best_k]
    clf = neighbors.KNeighborsClassifier(best_k)
    clf.fit(data_train, target_train)
    target_predicted = clf.predict(data_test)
    results = get_metrics(target_test, target_predicted, [0, 1])

    out_results = {
        'best k': best_k,
        'validation set':best_confm,
        'test set':results,
    }
    file = open('model.pickle','wb')
    pickle.dump(clf,file)
    file.close()
    return out_results

#get the data for machine learning
mydata = open("Planty_database.json", "r")
bunchobject = json.loads(mydata.readline())
mydata.close()
for i in bunchobject:
    bunchobject[i] = np.array(bunchobject[i])
#specifying that the first 3 features are included in the model
features = range(3)
print(knn_classifier_full(bunchobject=bunchobject, feature_list=features))

#rename the model with best accuracy as model_final and use in our final product