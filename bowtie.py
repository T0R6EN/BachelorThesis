import os
import random
import networkx as nx
import csv
import glob


class Bowtie():
    def __init__(self, indir, outdir):

        self.indir = indir
        self.outdir = outdir

    def process_all(self, minid, maxid):

        for id in range(minid, maxid + 1):
            print(id)
            fpath, g_id, date = self.load_fpath(id)
            print(fpath)
            net = self.create_graph(fpath)
            self.process(net, g_id, date)

    def process(self, net, g_id, date):

        allnodes = list(nx.nodes(net))
        fname = g_id + '-allnodes.csv'
        self.write_out(fname, allnodes, date)

        scc = list(max(nx.strongly_connected_components(net), key=len))
        fname = g_id + '-scc.csv'
        self.write_out(fname, scc)

        not_core = self.list_substractor(allnodes, scc)
        random_scc_node = random.choice(scc)
        del scc, allnodes

        wcc = list(max(nx.weakly_connected_components(net), key=len))
        fname = g_id + '-wcc.csv'
        self.write_out(fname, wcc)
        del wcc

        # in:
        i = []
        for node in not_core:
            if nx.has_path(net, node, random_scc_node) is True:
                i.append(node)
        IN = list(i)
        del i
        not_core_i = self.list_substractor(not_core, IN)
        del not_core
        fname = g_id + '-in.csv'
        self.write_out(fname, IN)
        del IN

        # out:
        o = []
        for node in not_core_i:
            if nx.has_path(net, random_scc_node, node):
                o.append(node)
        out = list(o)
        del o
        not_core_i_o = self.list_substractor(not_core_i, out)
        del not_core_i
        fname = g_id + '-out.csv'
        self.write_out(fname, out)
        del out

        # tendrils:
        t = []
        unet = net.to_undirected()
        for node in not_core_i_o:
            if nx.has_path(unet, node, random_scc_node) is True:
                t.append(node)
        ten = list(t)
        del t
        fname = g_id + '-ten.csv'
        self.write_out(fname, ten)

        # disconnected:
        dis = self.list_substractor(not_core_i_o, ten)
        del ten, not_core_i_o
        fname = g_id + '-dis.csv'
        self.write_out(fname, dis)
        del dis

    def list_substractor(self, l1, l2):
        slist = list(set(l1) - set(l2))
        return slist

    def create_graph(self, fpath):
        print('create_graph')
        net = nx.read_graphml(fpath)
        return net

    def load_fpath(self, id):
        print('load_fpath')
        indir = self.indir
        g_id = 'graph_%s' % id
        fname = g_id + '*.graphml'
        fpath = list(glob.iglob(indir + fname))[0]
        print(fpath)
        fn = fpath.split('/')[-1]
        date = fn.split(' ')[1]
        print(date)

        # fname= "segment_%s.graphml" % id
        # fpath = indir + fname
        return fpath, g_id, date

    def write_out(self, fname, l, date):
        print('write out:', fname)
        outdir = self.outdir + '%s/' % (date)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        outdir = outdir + fname

        with open(outdir, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in l:
                writer.writerow([val])


if __name__ == "__main__":

    indir = '//Users/Torben/Desktop/Python/consensus/weightedgraphml/'
    outdir = '//Users/Torben/Desktop/Python/consensus/bowtie/'

    minid = 1330
    maxid = 1953
    proc = Bowtie(indir, outdir)
    proc.process_all(minid, maxid)
