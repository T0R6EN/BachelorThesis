import os
import networkx as nx
import csv
import pandas as pd
import glob
import datetime


class BowtieProcessor():
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir
        self.theList = []

    def process_all(self, minid, maxid):
        for id in range(minid, maxid + 1):
            print(id)
            indir = self.indir
            g_id = 'graph_%s' % id
            subdir = [x[0] for x in os.walk(indir)]
            dirnames = [x.split(os.path.sep)[-1] for x in subdir[1:]]
            sdirnames = sorted(dirnames, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
            print(10 * '*-')
            print(sdirnames[id - 1])
            date = sdirnames[id - 1]

            fpath = indir + date + '/'

            corepath, inpath, outpath, tenpath, dispath, wccpath, time = self.load_filepaths(
                fpath, g_id, id)

            corel = self.read_in(corepath)
            inl = self.read_in(inpath)
            outl = self.read_in(outpath)
            tenl = self.read_in(tenpath)
            disl = self.read_in(dispath)
            wccl = self.read_in(wccpath)
            self.process(corel, inl, outl, tenl, disl, wccl, g_id, date)
            msg_str = "processed network = %s/%s " % (id, maxid)
            print(msg_str)

        self.create_table()

    def process(self, corel, inl, outl, tenl, disl, wccl, g_id, date):

        size_net = len(corel) + len(inl) + len(outl) + len(tenl) + len(disl)
        if size_net < 100:
            pass
        else:
            rsCore = len(corel) / size_net
            rsWCC = len(wccl) / size_net
            rsIN = len(inl) / size_net
            rsOUT = len(outl) / size_net
            rsTEN = len(tenl) / size_net
            rsDIS = len(disl) / size_net

            c_sum = sum([rsCore, rsIN, rsOUT, rsTEN, rsDIS])

            # theList: [Date, scc, in, etc..]
            self.theList.append([date, rsCore, rsIN, rsOUT, rsTEN, rsDIS, rsWCC, c_sum])

    def read_in(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            l = list(reader)
            return l

        net = nx.read_graphml(path)
        return net

    def load_filepaths(self, fpath, g_id, id):  # only works when starting from graph 1
        bpaths = sorted(list(glob.iglob(fpath + g_id + '*.csv')))
        corepath = bpaths[1]
        inpath = bpaths[3]
        outpath = bpaths[4]
        tenpath = bpaths[5]
        dispath = bpaths[2]
        wccpath = bpaths[6]
        fn = corepath.split('/')[-1]
        time = fn.split('@')[1]
        time = time.split('.')[0]

        # fname= "segment_%s.graphml" % id
        # fpath = indir + fname
        return corepath, inpath, outpath, tenpath, dispath, wccpath, time

    def create_table(self):
        theList = self.theList
        df = pd.DataFrame(theList, columns=['date', 'scc', 'in',
                                            'out', 'ten', 'dis', 'wcc', 'c_sum'])

        df.to_csv(self.outdir)


if __name__ == "__main__":

    indir = '//Users/Torben/Desktop/Python/consensus/bowtie_csv_files/'
    outdir = '//Users/Torben/Desktop/Python/consensus/bowtie_datetime_table/'

    minid = 1
    maxid = 7

    proc = BowtieProcessor(indir, outdir)
    proc.process_all(minid, maxid)
