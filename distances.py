import os
import csv
import pandas as pd
import glob


deltaT = [i + 1 for i in range(3)]

Thelist = []


def distance(m1, m2):
    x = [(j1, j2) for i1, i2 in zip(m1, m2) for j1, j2 in zip(i1, i2)]
    summation = sum((tup[0] - tup[1])**2 for tup in x)
    if summation != 0:
        D = (summation**(1 / 2)) / 5**2
    else:
        D = 0.0
    return D


def csv_writer(out_dir, list_to_save):
    with open(out_dir, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in list_to_save:
            writer.writerow([val])


def csvreader(in_dir):
    with open(in_dir, 'r') as f:
        reader = csv.reader(f)
        l = list(reader)
        return l


for delta in deltaT:
    indir = "/Users/Torben/Desktop/Python/consensus/t_matrices/delta_t_%d/" % (delta)
    Dlist = []

    fdirs = glob.glob(indir + '/*')
    fnames = [x.split(os.path.sep)[-1] for x in fdirs]
    # print(fnames, sep='\n')

    sfnames = sorted(fnames)

    for m1, m2 in zip(sfnames, sfnames[1:]):
        date1 = m1.split('@')[1].split('-')
        date2 = m2.split('@')[1].split('-')
        # print(date1[3])
        startdte = '%s-%s-%s' % (date1[0], date1[1], date1[2])
        enddte = '%s-%s-%s' % (date2[3], date2[4], date2[5])

        mdir1 = indir + m1
        trans_matrix1 = csvreader(mdir1)
        trans_matrix1 = [[int(i) for i in subl] for subl in trans_matrix1]

        mdir2 = indir + m2
        trans_matrix2 = csvreader(mdir2)
        trans_matrix2 = [[int(i) for i in subl] for subl in trans_matrix2]

        prob_m1 = [[item / sum(subl) if sum(subl) != 0 else item for item in subl]
                   for subl in trans_matrix1]

        prob_m2 = [[item / sum(subl) if sum(subl) != 0 else item for item in subl]
                   for subl in trans_matrix2]

        # print('probability matrix: ', prob_m1, '\n', prob_m2)

        # Distance
        D = distance(prob_m1, prob_m2)

        Subl = [startdte, delta, D]

        Thelist.append(Subl)


df = pd.DataFrame(Thelist, columns=['date', 'deltaT', 'distance'])
print(df)
df.to_csv('DistanceDF.csv', encoding='utf-8', sep=',', index=False)
