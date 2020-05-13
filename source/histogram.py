import pandas as pd
import matplotlib.pyplot as plt
import numpy
import os

def print_hist(dataset):

    houses = list(dataset['Hogwarts House'].value_counts().index)
    classes = list(dataset.columns[6:])

    for class_score in classes:
        for house in houses:
            dataset[dataset['Hogwarts House'] == house][class_score].hist()
            plt.title(class_score)
            plt.legend(houses)

        plt.show()


if __name__ == '__main__':
    dataset = pd.read_csv(os.path.join('..', 'data', 'dataset_train.csv'))
    print_hist(dataset)
