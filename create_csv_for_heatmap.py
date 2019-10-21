import csv
import pandas as pd

indir = '//Users/Torben/Desktop/Python/consensus/Files/'
fname = 'fullmtm.csv'


theList = []


def csvreader(in_dir):
    with open(in_dir, 'r') as f:
        reader = csv.reader(f)
        l = list(reader)
        return l


mtm = csvreader(indir + fname)
mtm = [[i for i in subl] for subl in mtm]
print(mtm)


########
# following order : [in, core, out, ten, dis]

#                   t+1
#   mtm = [['11','12','13','14','15'],
# 			['21','22','23','24','25'],
# 		t	['31','32','33','34','35'],
# 			['41','42','43','44','45'],
# 			['51','52','53','54','55']]


theList.append(['IN', 'IN', mtm[0][0]])
theList.append(['IN', 'SCC', mtm[0][1]])
theList.append(['IN', 'OUT', mtm[0][2]])
theList.append(['IN', 'TEN', mtm[0][3]])
theList.append(['IN', 'DIS', mtm[0][4]])

theList.append(['SCC', 'IN', mtm[1][0]])
theList.append(['SCC', 'SCC', mtm[1][1]])
theList.append(['SCC', 'OUT', mtm[1][2]])
theList.append(['SCC', 'TEN', mtm[1][3]])
theList.append(['SCC', 'DIS', mtm[1][4]])

theList.append(['OUT', 'IN', mtm[2][0]])
theList.append(['OUT', 'SCC', mtm[2][1]])
theList.append(['OUT', 'OUT', mtm[2][2]])
theList.append(['OUT', 'TEN', mtm[2][3]])
theList.append(['OUT', 'DIS', mtm[2][4]])

theList.append(['TEN', 'IN', mtm[3][0]])
theList.append(['TEN', 'SCC', mtm[3][1]])
theList.append(['TEN', 'OUT', mtm[3][2]])
theList.append(['TEN', 'TEN', mtm[3][3]])
theList.append(['TEN', 'DIS', mtm[3][4]])

theList.append(['DIS', 'IN', mtm[4][0]])
theList.append(['DIS', 'SCC', mtm[4][1]])
theList.append(['DIS', 'OUT', mtm[4][2]])
theList.append(['DIS', 'TEN', mtm[4][3]])
theList.append(['DIS', 'DIS', mtm[4][4]])


outname = 'heatmap_max.csv'
df = pd.DataFrame(theList, columns=['var1', 'var2', 'probability'])
df.to_csv(indir + outname, index=False)  # , header=False
print(df)
