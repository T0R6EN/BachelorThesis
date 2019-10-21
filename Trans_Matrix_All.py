import os
import csv
import pandas as pd
import time
import glob
import datetime


class Bowtie():
    def __init__(self, indir, outdir):

        self.indir = indir
        self.outdir = outdir
        self.theList = []
        self.trans_matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.current_id = 0

    def process_all(self, minid, maxid, delta, start):
        for d in range(delta):
            print('delta = %d' % (d + 1))

        try:
            for id in range(minid, maxid + 1):
                # print(10*'*-')

                indir = self.indir
                g_id = 'graph_%s' % id
                subdir = [x[0] for x in os.walk(indir)]
                # print(subdir)
                dirnames = [x.split(os.path.sep)[-1] for x in subdir[1:]]
                sdirnames = sorted(
                    dirnames, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
                print(sdirnames[id - 1])
                date = sdirnames[id - 1]
                try:
                    date2 = sdirnames[id + d]
                except:
                    print('no new lists to add as l2')
                fpath = indir + date + '/'
                fpath2 = indir + date2 + '/'
                corepath, inpath, outpath, tenpath, dispath, corepath2, inpath2, outpath2, tenpath2, dispath2 = self.load_filepaths(
                    fpath, fpath2)
                corel = self.read_in(corepath)
                inl = self.read_in(inpath)
                outl = self.read_in(outpath)
                tenl = self.read_in(tenpath)
                disl = self.read_in(dispath)
                # wccl = self.read_in(wccpath)
                corel2 = self.read_in(corepath2)
                inl2 = self.read_in(inpath2)
                outl2 = self.read_in(outpath2)
                tenl2 = self.read_in(tenpath2)
                disl2 = self.read_in(dispath2)
                # wccl2 = self.read_in(wccpath2)
                self.process(corel, inl, outl, tenl, disl, corel2, inl2,
                             outl2, tenl2, disl2, g_id, date, date2, d)
                self.current_id = id
                msg_str = "------------ processed network = %s/%s delta = %d ---------------" % (
                    id, maxid, d + 1)
                print(msg_str)
            trans_matrix = [[item / sum(subl) if sum(subl) != 0 else item for item in subl]
                            for subl in self.trans_matrix]
            fname = "matrix_delta_%d" % (d + 1)
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
            outdir = self.outdir + fname
            self.save_matrix(outdir, trans_matrix)
            end = time.time()
            t = (end - start) / 60
            print('time used: %d') % t

        except KeyboardInterrupt:
            trans_matrix = [[item / sum(subl) if sum(subl) != 0 else item for item in subl]
                            for subl in trans_matrix]
            fname = "matrix_delta_%d" % (d + 1)
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
            outdir = outdir + fname
            self.save_matrix(outdir, trans_matrix)
            end = time.time()
            t = (end - start) / 60
            print('time used: %d') % t

    def process(self, corel, inl, outl, tenl, disl,  corel2, inl2, outl2, tenl2, disl2, g_id, date, date2, d):
        start1 = time.time()

        l1 = [inl, corel, outl, tenl, disl]
        l2 = [inl2, corel2, outl2, tenl2, disl2]

        for count, seg in enumerate(l1):
            for count2, seg2 in enumerate(l2):
                for i in seg:
                    if i in seg2:
                        self.trans_matrix[count2][count] += 1

        end1 = time.time()
        # print('transition matrix @%s/%s:'%(date, date2))
        print('time used: %d s' % (end1 - start1))

    def read_in(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            l = list(reader)
            return l

    def load_filepaths(self, fpath, fpath2):  # only works when starting from graph 1
        # print('load_fpath')

        f = sorted(list(glob.iglob(fpath + '*.csv')))
        s = sorted(list(glob.iglob(fpath2 + '*.csv')))

        if any("@" in s for s in f):
            corepath = f[1]
            inpath = f[3]
            outpath = f[4]
            tenpath = f[5]
            dispath = f[2]
            # wccpath =f[6]
            corepath2 = s[1]
            inpath2 = s[3]
            outpath2 = s[4]
            tenpath2 = s[5]
            dispath2 = s[2]
            # wccpath2 = s[6]

        else:
            corepath = f[4]
            inpath = f[2]
            outpath = f[3]
            tenpath = f[5]
            dispath = f[1]
            # wccpath =f[6]
            corepath2 = s[4]
            inpath2 = s[2]
            outpath2 = s[3]
            tenpath2 = s[5]
            dispath2 = s[1]
            # wccpath2 = s[6]

        return corepath, inpath, outpath, tenpath, dispath, corepath2, inpath2, outpath2, tenpath2, dispath2

    def save_matrix(self, outdir, trans_matrix):
        df = pd.DataFrame(trans_matrix)
        df.to_csv(outdir, index=False, header=False)
        print(df)


if __name__ == "__main__":

    indir = '/mnt/hdd_data/tmannh/bowtiecsv/'
    outdir = '/mnt/hdd_data/tmannh/trans_matrix/'

    minid = 1
    maxid = 1541
    delta = 1
    proc = Bowtie(indir, outdir)
    start = time.time()
    proc.process_all(minid=minid, maxid=maxid, start=start, delta=delta)
