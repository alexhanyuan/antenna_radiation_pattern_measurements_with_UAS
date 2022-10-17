#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: rx_fft_mag_RTL
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time

class rx_fft_mag_RTL(gr.top_block):

    def __init__(self, RF_gain=10, filename='data_woo_ya', frequency=443000000, num_buffers=10, samp_rate=1000000):
        gr.top_block.__init__(self, "rx_fft_mag_RTL")

        ##################################################
        # Parameters
        ##################################################
        self.RF_gain = RF_gain
        self.filename = filename
        self.frequency = frequency
        self.num_buffers = num_buffers
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.offset = offset = 56848
        self.num_points = num_points = 81920
        self.m = m = 1024

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(frequency-200000, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_gain(RF_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(num_points, True, window.blackmanharris(num_points), True, 1)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, num_points)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, 512)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, num_points)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, num_points, 0)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_float, m, num_points, offset)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_points*num_buffers)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*512, './' + filename + '.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(num_points)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_head_0, 0))

    def get_RF_gain(self):
        return self.RF_gain

    def set_RF_gain(self, RF_gain):
        self.RF_gain = RF_gain
        self.rtlsdr_source_0.set_gain(self.RF_gain, 0)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open('./' + self.filename + '.bin')

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.rtlsdr_source_0.set_center_freq(self.frequency-200000, 0)

    def get_num_buffers(self):
        return self.num_buffers

    def set_num_buffers(self, num_buffers):
        self.num_buffers = num_buffers
        self.blocks_head_0.set_length(self.num_points*self.num_buffers)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.blocks_keep_m_in_n_0.set_offset(self.offset)

    def get_num_points(self):
        return self.num_points

    def set_num_points(self, num_points):
        self.num_points = num_points
        self.blocks_head_0.set_length(self.num_points*self.num_buffers)
        self.blocks_keep_m_in_n_0.set_n(self.num_points)

    def get_m(self):
        return self.m

    def set_m(self, m):
        self.m = m
        self.blocks_keep_m_in_n_0.set_m(self.m)


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--RF-gain", dest="RF_gain", type=intx, default=10,
        help="Set RF_gain [default=%(default)r]")
    parser.add_argument(
        "--filename", dest="filename", type=str, default='data_woo_ya',
        help="Set filename [default=%(default)r]")
    parser.add_argument(
        "--frequency", dest="frequency", type=intx, default=443000000,
        help="Set frequency [default=%(default)r]")
    parser.add_argument(
        "--num-buffers", dest="num_buffers", type=intx, default=10,
        help="Set num_buffers [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=intx, default=1000000,
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=rx_fft_mag_RTL, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(RF_gain=options.RF_gain, filename=options.filename, frequency=options.frequency, num_buffers=options.num_buffers, samp_rate=options.samp_rate)

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
