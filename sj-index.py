import os
import networkx as nx
import pandas as pd
from collections import defaultdict
import glob


class Concentration():
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir
        self.clist = []

    def get_var_value(filename="varstore.dat"):
        with open(filename, "a+") as f:
            val = int(f.read() or 0) + 1
            f.seek(0)
            f.truncate()
            f.write(str(val))
        return val

    def process_all(self, minid, maxid):
        print('process_all')
        run_counter = self.get_var_value()
        for id in range(minid, maxid + 1):
            print(id)
            fpath = self.load_fpath(id)
            print(fpath)
            net = self.create_graph(fpath)
            self.process(net)
        fname = 'concentration_id%d-%d_rc%d.csv' % (minid, maxid, run_counter)
        self.write_out(fname)

    def process(self, net):
        print('process: ')
        dct = defaultdict(list)
        l = [[v, w['qty']] for u, v, w in net.edges(data=True)]
        for subl in l:
            senderweight = subl[1]
            dct[subl[0]].append(senderweight)
        for key in dct:
            top = 0
            bottom = 0
            for weight in dct[key]:
                top += weight
                bottom += weight**2
            top = top**2
            s = top / bottom
            self.clist.append([key, s])

        def create_graph(self, fpath):
            net = nx.read_graphml(fpath)
            return net

        def load_fpath(self, id):
            print('load_fpath')
            indir = self.indir
            g_id = 'graph_%s' % id
            fname = g_id + '*.graphml'
            fpath = list(glob.iglob(indir + fname))[0]
            print(fpath)
            return fpath

        def write_out(self, fname):
            print('write out:', fname)
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
            outdir = self.outdir + fname
            df = pd.DataFrame(self.clist, columns=['node', 'concentration'])
            df = df.assign(prob=df.concentration.map(df.concentration.value_counts(normalize=True)))
            print(df)
            df.to_csv(outdir, encoding='utf-8', sep=',', index=False)


if __name__ == "__main__":

    indir = '/mnt/hdd_data/tmannh/bitcoin-weighted-network-heur_2s.256b/'
    outdir = '/mnt/hdd_data/tmannh/c_tables/'

    minid = 1
    maxid = 1500
    proc = Concentration(indir, outdir)
    proc.process_all(minid, maxid)
