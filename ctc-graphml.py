# from __future__ import print_function
# -*- coding: utf-8 -*-

from sequential import SequentialAnaliser
import os
import os.path
import pickle
import optparse
import networkx as nx


# ======================================================= #


class AddressAppearance(SequentialAnaliser):

    def __init__(self, save_each, period=None, ecur=None, heuristic="heur_0"):

        self.heuristic = heuristic

        self.pickled_directory = "/Volumes/LargeFiles/Python/UH-%s-%s" % (ecur, self.heuristic)
        SequentialAnaliser.__init__(
            self, save_each, ecur=ecur, pickled_dir=self.pickled_directory)

        cfg = pickle.load(open("%s/config-1_500000.pickle" % (self.pickled_directory)))
        self.final_no_users = cfg["n_users"]

        self.period = period
        minBlock = str(options.min_blk / 1000) + 'k'
        maxBlock = str(options.max_blk / 1000) + 'k'
        self.out_dir = "/Users/Torben/Desktop/Python/consensus/graphmlfiles/%s_gml_%s-%s_%s.%s" % (
            self.currency, minBlock, maxBlock, self.heuristic, self.period)
        self.file_out = open("/Users/Torben/Desktop/Python/consensus/%s_gml_%s-%s_%s.%s.info" %
                             (self.currency, minBlock, maxBlock, self.heuristic, self.period), "w")

        self.net = nx.DiGraph()

        self.cycle_count = 0
        self.last_time = None
        self.name = 0

    def process(self, blk):
        self.current_cycle = self.update_cycle()
        if self.last_time is None:
            self.last_time = 2
        # print(options.max_blk)
        all_transactions = blk.short_transactions[1:]
        for (transaction_hash, transaction_fee, transaction_size, transaction_input, transaction_output) in all_transactions:
            try:
                [(input_user, qty)] = transaction_input
                for t_out in range(len(transaction_output)):
                    self.net.add_edge(input_user, transaction_output[t_out][0])
            except:
                print "ERROR LOADING", blk.block_id

    def get_segment(self):

        # segment_int = self.period -1
        if self.period == '1b':
            segment_int = 0
        if self.period == '2b':
            segment_int = 1
        if self.period == '4b':
            segment_int = 3
        if self.period == '8b':
            segment_int = 7
        if self.period == '16b':
            segment_int = 15
        if self.period == '32b':
            segment_int = 31
        if self.period == '64b':
            segment_int = 63
        if self.period == '128b':
            segment_int = 127
        if self.period == '256b':
            segment_int = 255
        if self.period == '512b':
            segment_int = 511
        if self.period == '1024b':
            segment_int = 1023
        if self.period == '2048b':
            segment_int = 2047
        if self.period == '4096b':
            segment_int = 4095
        if self.period == '8192b':
            segment_int = 8191
        if self.period == '16384b':
            segment_int = 16383

        return segment_int

    def update_cycle(self, **kwargs):
        if self.last_time is None:
            return

        if self.cycle_count < self.get_segment():
            self.cycle_count += 1

        else:
            self.build_graph()

    def build_graph(self, **kwargs):
        self.name += 1
        out_dir = self.out_dir
        fout = 'segment_' + str(self.name) + '.graphml'
        # key = str(self.name)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        print >> self.file_out, "%s/%s" % (out_dir, fout)
        # print("%s/%s" % (out_dir, fout), file=self.file_out)
        self.file_out.flush()
        nx.write_graphml(self.net, "%s/%s" % (out_dir, fout))
        # nx.draw(self.net, with_labels=True)
        # plt.show()
        self.net.clear()
        # print 25 * '-*-*'
        self.cycle_count = 0
        return self.cycle_count

        #########################################################################################
        #########################################################################################


def parse_command_line():
    from optparse import OptionParser

    parser = optparse.OptionParser()

    parser.add_option("--min-blk", type="int", action='store', dest="min_blk",
                      default=1, help="minimum block number to process")

    parser.add_option("--max-blk", type="int", action='store', dest="max_blk",
                      default=None, help="maximum block number to process")

    parser.add_option("--save-each", type="int", action='store', dest="save_each",
                      default=1, help="saves and updates status every SAVE_EACH")

    parser.add_option("--period", action='store', dest="period",
                      default="day", help="type of time-aggregation")

    parser.add_option("--heuristic", action='store', dest='heuristic',
                      default=None, help="run for given heuristic")

    parser.add_option("--curr", action='store', dest="currency", default=None,
                      help="which currency is being analysed")

    parser.add_option("--minimum-wealth", type="float", action='store', dest="minimum_wealth",
                      default=1e-4, help="minimum wealth non trimmed")

    options, args = parser.parse_args()

    if options.max_blk is None:
        blk_1 = load_id(options.currency, 1)
        options.max_blk = blk_1.heur_0["blk_max"]

    options.sinks_filename = "%s_sinks.pickle.gz" % (options.heuristic)

    return options, args


if __name__ == "__main__":

    options, args = parse_command_line()
    proc = AddressAppearance(options.save_each,  options.period,
                             ecur=options.currency, heuristic=options.heuristic)
    proc.minimum_wealth = options.minimum_wealth

    proc.process_all(options.min_blk, options.max_blk)
