#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time

class rx_mag(gr.top_block):

    def __init__(self, RF_gain=32, filename='data_woo_ya', frequency=446000000, num_samps=10000, samp_rate=1000000, wav_scaling=50):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.RF_gain = RF_gain
        self.filename = filename
        self.frequency = frequency
        self.num_samps = num_samps
        self.samp_rate = samp_rate
        self.wav_scaling = wav_scaling

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frequency-200000, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(RF_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('./' + filename + '.wav', 1, samp_rate, 16)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_ff(wav_scaling, 1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_samps)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_head_0, 0))

    def get_RF_gain(self):
        return self.RF_gain

    def set_RF_gain(self, RF_gain):
        self.RF_gain = RF_gain
        self.osmosdr_source_0.set_gain(self.RF_gain, 0)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_wavfile_sink_0.open('./' + self.filename + '.wav')

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_source_0.set_center_freq(self.frequency-200000, 0)

    def get_num_samps(self):
        return self.num_samps

    def set_num_samps(self, num_samps):
        self.num_samps = num_samps
        self.blocks_head_0.set_length(self.num_samps)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_wav_scaling(self):
        return self.wav_scaling

    def set_wav_scaling(self, wav_scaling):
        self.wav_scaling = wav_scaling
        self.blocks_multiply_const_xx_0.set_k(self.wav_scaling)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--RF-gain", dest="RF_gain", type=intx, default=32,
        help="Set RF_gain [default=%(default)r]")
    parser.add_argument(
        "--filename", dest="filename", type=str, default='data_woo_ya',
        help="Set filename [default=%(default)r]")
    parser.add_argument(
        "--frequency", dest="frequency", type=intx, default=446000000,
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--num-samps", dest="num_samps", type=intx, default=10000,
        help="Set num_samps [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=intx, default=1000000,
        help="Set samp_rate [default=%(default)r]")
    parser.add_argument(
        "--wav-scaling", dest="wav_scaling", type=eng_float, default="50.0",
        help="Set wav_scaling [default=%(default)r]")
    return parser


def main(top_block_cls=rx_mag, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(RF_gain=options.RF_gain, filename=options.filename, frequency=options.frequency, num_samps=options.num_samps, samp_rate=options.samp_rate, wav_scaling=options.wav_scaling)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
