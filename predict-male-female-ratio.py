import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def main():


    # reads df from file
    df = pd.read_csv('university_ranking.csv', index_col=0)  

    # removes rows with a missing value
    df.dropna(how='any', inplace=True)

    # columns of interest as features
    coi = ['no_student', 
           'year',
           'score_teaching', 
           'score_research', 
           'score_citation', 
           'score_int_outlook']

    # np.array features
    x = np.array(df[coi])

    # np.array labels
    y = np.array(df['male'])

    # the classifier we use
    clf = DecisionTreeClassifier()

    # splits data into training and testing data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # trains classifier
    clf.fit(x_train, y_train)

    # prints accuracy of classifier
    accuracy = clf.score(x_test, y_test)
    print(accuracy)


if __name__ == "__main__":
    main()
