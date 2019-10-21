import os
import networkx as nx
import pandas as pd
import glob
import sys
import collections
import atexit
from json import dumps, loads


class Outdegree():
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir
        self.thelist = []
        self.deglist = []
        self.current_id = 0

    def process_all(self, minid, maxid, run_counter):
        try:
            for id in range(minid, maxid + 1):
                print(id, ': ')
                # print('# of runs: %d'%run_counter)
                fpath, date = self.load_fpath(id)
                self.outdeg(fpath)
                self.current_id = id
                print(10 * '=', ' - distOutdegree.py - run # %d - ' % run_counter, 10 * '=')
            self.process()
            fname = 'outdegree_id%d-%d_rc%d.csv' % (minid, maxid, run_counter)
            self.write_out(fname)
        except KeyboardInterrupt:
            print('saving values..')
            self.process()
            fname = 'outdegree_id%d-%d_rc%d.csv' % (minid, self.current_id, run_counter)
            self.write_out(fname)
            sys.exit(0)

    def process(self, net, date):
        dct = collections.defaultdict(list)
        for count, item in enumerate(self.deglist, start=1):
            for v in item.values():
                dct[v] += 1
                self.thelist = list(dct.items())

    def outdeg(self, fpath):
        net = nx.read_graphml(fpath)
        odegree = net.out_degree()
        self.deglist.append(odegree)

    def load_fpath(self, id):
        indir = self.indir
        g_id = 'graph_%s' % id
        fname = g_id + '*.graphml'
        fpath = list(glob.iglob(indir + fname))[0]
        print(fpath)
        fname = fpath.split('/')[-1]
        date = fname.split(' ')[1]
        return fpath, date

    def write_out(self, fname):
        print('write out:', fname)
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        outdir = self.outdir + fname
        df = pd.DataFrame(self.thelist, columns=['degree', 'count'])
        df.to_csv(outdir, encoding='utf-8', sep=',', index=False)


if __name__ == "__main__":
    minid = 1
    maxid = 1500
    indir = '/mnt/hdd_data/tmannh/bitcoin-weighted-network-heur_2s.256b/'
    outdir = '/mnt/hdd_data/tmannh/DegreeDist/'

    def read_counter():
        return loads(open("counter_outdegree.json", "r").read()) + 1 if os.path.exists("counter_outdegree.json") else 0

    def write_counter():
        with open("counter_outdegree.json", "w") as f:
            f.write(dumps(run_counter))

    run_counter = read_counter()
    atexit.register(write_counter)

    proc = Outdegree(indir, outdir)
    proc.process_all(minid, maxid, run_counter)
