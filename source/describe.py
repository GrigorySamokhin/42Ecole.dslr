import numpy as np
import pandas as pd
import csv
import sys

class DesribeDataset():
    def __init__(self, dataset):

        self.dataset_all = self.open_file(dataset)
        self.dataset_len = len(self.dataset_all)
        self.num_features = self.compute_num_feat()
        self.dataset_num = self.compute_dataset_num()
        self.m = self.dataset_num.shape[0]
        self.n = self.dataset_num.shape[1]

    def open_file(self, dataset):

        dataset_all = []

        with open(dataset, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                dataset_all += [row]
        return np.array(dataset_all)

    def compute_num_feat(self):

        numeric_features = []

        n_features = len(self.dataset_all[0])
        for i in range(n_features):
            try:
                fl = float(self.dataset_all[1][i])
                numeric_features.append(i)
            except:
                pass
        return numeric_features


    def compute_dataset_num(self):

        dataset_num = []

        for i in range(1, self.dataset_len):
            dataset_num.append(np.array(self.dataset_all[i, self.num_features]))
        dataset_num = np.array(dataset_num)
        return dataset_num

    def count_mean(self):
        counts = []
        means = []

        for j in range(self.n):
            count = 0
            mean = 0

            for i in range(self.m):
                try:
                    num = float(self.dataset_num[i, j])
                    count += 1
                    mean += num
                except:
                    pass
            counts.append(count)
            means.append(mean / count)
        return ['count'] + counts, ['mean'] + means

    def std(self, counts, means):
        stds = []

        for j in range(self.n):
            var = 0
            for i in range(self.m):
                try:
                    num = float(self.dataset_num[i, j])
                    var += (num - means[j])**2
                except:
                    pass
            stds.append((var / (counts[j]-1))**(1/2))
        return ['std'] + stds

    def refactor(self, colmn):
        ref = []
        for i in range(len(colmn)):
            try:
                ref.append(float(colmn[i]))
            except:
                pass
        return sorted(ref)

    def describe_quantile(self, column_sort, sample, qrt):

        count = self.count[1:]
        i = qrt * (count[sample] + 1)
        i = count[sample] - 1 if qrt == 1 else i
        i = 0 if qrt == 0 else i
        if np.floor(i) == i:
            val_qrt = column_sort[int(i)]
        else:
            i = int(np.floor(i))
            val_qrt = (column_sort[i+1] + column_sort[i]) * 0.5

        return val_qrt

    def compute_quantiles(self):
        all_q = []

        for qrt in [0, 1/4, 2/4, 3/4, 1]:
            for sample in range(self.n):
                all_q.append(self.describe_quantile(
                    self.refactor(self.dataset_num[:, sample]),
                    sample,
                    qrt)
                )
        return ['min'] + all_q[:14], ['25%'] + all_q[14:28], \
                    ['50%'] + all_q[28:42], ['75%'] + all_q[42:56], ['max'] + all_q[56:]

    def describe(self):
        self.count, mean = self.count_mean()
        std = self.std(self.count[1:], mean[1:])
        min_v, low, med, high, max_v \
            = self.compute_quantiles()
        indexes = [''] + list(self.dataset_all[0, self.num_features])
        df = pd.DataFrame(
            np.array([self.count, mean, std, min_v, low, med, high, max_v]),
            columns=indexes
        )
        df.set_index('', inplace=True)
        print(df)

describe = DesribeDataset(sys.argv[1])
describe.describe()
