import os
import networkx as nx
import pandas as pd
import glob
import sys
import atexit
from json import dumps, loads


class Cliques():
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir
        self.cl_list = []
        self.current_id = 0

    def process_all(self, minid, maxid, run_counter):
        try:
            for id in range(minid, maxid + 1):
                print(id, ': ')
                # print('# of runs: %d'%run_counter)
                fpath, date = self.load_fpath(id)
                net = self.create_graph(fpath)
                self.process(net, date)
                self.current_id = id
                print(10 * '=', ' - cliques.py - run # %d - ' % run_counter, 10 * '=')
            fname = 'cliques_id%d-%d_rc%d.csv' % (minid, maxid, run_counter)
            self.write_out(fname)
        except KeyboardInterrupt:
            print('saving values..')
            fname = 'cliques_id%d-%d_rc%d.csv' % (minid, self.current_id, run_counter)
            self.write_out(fname)
            sys.exit(0)

    def process(self, net, date):
        u = net.to_undirected()
        cliques = list(nx.enumerate_all_cliques(u))
        if cliques == []:
            max_c = 0
        else:
            max_c = len(max(cliques, key=len))
        print('number of cliques:', len(cliques))
        print('max clique size: ', max_c)
        self.cl_list.append([date, max_c])

    def create_graph(self, fpath):
        net = nx.read_graphml(fpath)
        return net

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
        df = pd.DataFrame(self.cl_list, columns=['date', 'max_c'])
        df.to_csv(outdir, encoding='utf-8', sep=',', index=False)


if __name__ == "__main__":
    minid = 1000
    maxid = 1500
    indir = '/mnt/hdd_data/tmannh/bitcoin-weighted-network-heur_2s.256b/'
    outdir = '/mnt/hdd_data/tmannh/cliques/'

    def read_counter():
        return loads(open("counter_cliques.json", "r").read()) + 1 if os.path.exists("counter_cliques.json") else 0

    def write_counter():
        with open("counter_cliques.json", "w") as f:
            f.write(dumps(run_counter))

    run_counter = read_counter()
    atexit.register(write_counter)


# ---------------------------------------------------------- #

# ---------------------------------------------------------- #

    proc = Cliques(indir, outdir)
    proc.process_all(minid, maxid, run_counter)
