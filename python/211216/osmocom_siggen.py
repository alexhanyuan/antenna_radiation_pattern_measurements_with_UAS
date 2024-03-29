#!/usr/bin/env python3
#
# Copyright 2009,2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr
from gnuradio import analog
from gnuradio.gr.pubsub import pubsub
from osmosdr import osmocom_siggen_base as osmocom_siggen
import sys, math

try:
    from gnuradio.wxgui import gui, forms
    import wx
except ImportError:
    sys.stderr.write("Error importing GNU Radio's wxgui. Please make sure gr-wxgui is installed.\n")
    sys.exit(1)

class app_gui(pubsub):
    def __init__(self, frame, panel, vbox, top_block, options, args):
        pubsub.__init__(self)
        self.frame = frame      # Use for top-level application window frame
        self.panel = panel      # Use as parent class for created windows
        self.vbox = vbox        # Use as sizer for created windows
        self.tb = top_block     # GUI-unaware flowgraph class
        self.options = options  # Supplied command-line options
        self.args = args        # Supplied command-line arguments
        self.build_gui()

    # Event response handlers
    def evt_set_status_msg(self, msg):
        self.frame.SetStatusText(msg, 0)

    # GUI construction
    def build_gui(self):
        self.vbox.AddSpacer(3)
        self.vbox.AddStretchSpacer()
        ##################################################
        # Baseband controls
        ##################################################
        bb_vbox = forms.static_box_sizer(parent=self.panel, label="Baseband Modulation", orient=wx.VERTICAL, bold=True)
        self.vbox.Add(bb_vbox, 0, wx.EXPAND)
        sine_bb_hbox = wx.BoxSizer(wx.HORIZONTAL)
        sweep_bb_hbox = wx.BoxSizer(wx.HORIZONTAL)
        tone_bb_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.AddSpacer(5)
        self.vbox.AddStretchSpacer()
        #callback to show/hide forms
        def set_type(type):
            sine_bb_hbox.ShowItems(type == analog.GR_SIN_WAVE)
            sweep_bb_hbox.ShowItems(type == 'sweep')
            tone_bb_hbox.ShowItems(type == '2tone')
            self.vbox.Layout()
        self.tb.subscribe(osmocom_siggen.TYPE_KEY, set_type)
        #create sine forms
        sine_bb_hbox.AddSpacer(5)
        forms.text_box(
            parent=self.panel, sizer=sine_bb_hbox,
            label='Frequency (Hz)',
            ps=self.tb,
            key=osmocom_siggen.WAVEFORM_FREQ_KEY,
            converter=forms.float_converter(),
        )
        sine_bb_hbox.AddStretchSpacer()
        #create sweep forms
        sweep_bb_hbox.AddSpacer(5)
        forms.text_box(
            parent=self.panel, sizer=sweep_bb_hbox,
            label='Sweep Width (Hz)',
            ps=self.tb,
            key=osmocom_siggen.WAVEFORM_FREQ_KEY,
            converter=forms.float_converter(),
        )
        sweep_bb_hbox.AddStretchSpacer()
        forms.text_box(
            parent=self.panel, sizer=sweep_bb_hbox,
            label='Sweep Rate (Hz)',
            ps=self.tb,
            key=osmocom_siggen.WAVEFORM2_FREQ_KEY,
            converter=forms.float_converter(),
        )
        sweep_bb_hbox.AddStretchSpacer()
        #create 2tone forms
        tone_bb_hbox.AddSpacer(5)
        forms.text_box(
            parent=self.panel, sizer=tone_bb_hbox,
            label='Tone 1 (Hz)',
            ps=self.tb,
            key=osmocom_siggen.WAVEFORM_FREQ_KEY,
            converter=forms.float_converter(),
        )
        tone_bb_hbox.AddStretchSpacer()
        forms.text_box(
            parent=self.panel, sizer=tone_bb_hbox,
            label='Tone 2 (Hz)',
            ps=self.tb,
            key=osmocom_siggen.WAVEFORM2_FREQ_KEY,
            converter=forms.float_converter(),
        )
        tone_bb_hbox.AddStretchSpacer()
        forms.radio_buttons(
            parent=self.panel, sizer=bb_vbox,
            choices=osmocom_siggen.waveforms.keys(),
            labels=osmocom_siggen.waveforms.values(),
            ps=self.tb,
            key=osmocom_siggen.TYPE_KEY,
            style=wx.NO_BORDER | wx.RA_HORIZONTAL,
        )
        bb_vbox.AddSpacer(5)
        bb_vbox.Add(sine_bb_hbox, 0, wx.EXPAND)
        bb_vbox.Add(sweep_bb_hbox, 0, wx.EXPAND)
        bb_vbox.Add(tone_bb_hbox, 0, wx.EXPAND)
        set_type(self.tb[osmocom_siggen.TYPE_KEY])

        ##################################################
        # Frequency controls
        ##################################################
        fc_vbox = forms.static_box_sizer(parent=self.panel,
                                         label="Center Frequency",
                                         orient=wx.VERTICAL,
                                         bold=True)
        fc_vbox.AddSpacer(3)

        # First row of frequency controls (center frequency)
        freq_hbox = wx.BoxSizer(wx.HORIZONTAL)
        fc_vbox.Add(freq_hbox, 0, wx.EXPAND)
        fc_vbox.AddSpacer(5)

        # Second row of frequency controls (freq. correction)
        corr_hbox = wx.BoxSizer(wx.HORIZONTAL)
        fc_vbox.Add(corr_hbox, 0, wx.EXPAND)
        fc_vbox.AddSpacer(3)

        # Add frequency controls to top window sizer
        self.vbox.Add(fc_vbox, 0, wx.EXPAND)
        self.vbox.AddSpacer(5)
        self.vbox.AddStretchSpacer()

        freq_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=freq_hbox,
            label='Center Frequency (Hz)',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.TX_FREQ_KEY,
        )
        freq_hbox.AddSpacer(5)

        try:
            forms.slider(
                parent=self.panel, sizer=freq_hbox,
                proportion=2,
                ps=self.tb,
                key=osmocom_siggen.TX_FREQ_KEY,
                minimum=self.tb[osmocom_siggen.FREQ_RANGE_KEY].start(),
                maximum=self.tb[osmocom_siggen.FREQ_RANGE_KEY].stop(),
                num_steps=101,
            )
            freq_hbox.AddSpacer(3)
        except:
            pass

        corr_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=corr_hbox,
            label='Freq. Correction (ppm)',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.FREQ_CORR_KEY,
        )
        corr_hbox.AddSpacer(5)

        forms.slider(
            parent=self.panel, sizer=corr_hbox,
            proportion=2,
            ps=self.tb,
            key=osmocom_siggen.FREQ_CORR_KEY,
            minimum=-100,
            maximum=+100,
            num_steps=2010,
            step_size=0.1,
        )
        corr_hbox.AddSpacer(3)

        ##################################################
        # Amplitude controls
        ##################################################
        amp_vbox = forms.static_box_sizer(parent=self.panel,
                                          label="Amplitude",
                                          orient=wx.VERTICAL,
                                          bold=True)
        amp_vbox.AddSpacer(3)

        # First row of amp controls (ampl)
        lvl_hbox = wx.BoxSizer(wx.HORIZONTAL)
        amp_vbox.Add(lvl_hbox, 0, wx.EXPAND)
        amp_vbox.AddSpacer(5)

        self.vbox.Add(amp_vbox, 0, wx.EXPAND)
        self.vbox.AddSpacer(5)
        self.vbox.AddStretchSpacer()

        lvl_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=lvl_hbox,
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.AMPLITUDE_KEY,
            label="Level (0.1-1.0)",
        )
        lvl_hbox.AddSpacer(5)
        forms.log_slider(
            parent=self.panel, sizer=lvl_hbox,
            proportion=2,
            ps=self.tb,
            key=osmocom_siggen.AMPLITUDE_KEY,
            min_exp=-1,
            max_exp=0,
            base=10,
            num_steps=100,
        )
        lvl_hbox.AddSpacer(3)

        for gain_name in self.tb.get_gain_names():
            range = self.tb[osmocom_siggen.GAIN_RANGE_KEY(gain_name)]
            gain = self.tb[osmocom_siggen.GAIN_KEY(gain_name)]

            #print gain_name, gain, range.to_pp_string()
            if range.start() < range.stop():
                gain_hbox = wx.BoxSizer(wx.HORIZONTAL)
                amp_vbox.Add(gain_hbox, 0, wx.EXPAND)
                amp_vbox.AddSpacer(3)

                gain_hbox.AddSpacer(3)
                forms.text_box(
                    parent=self.panel, sizer=gain_hbox,
                    proportion=1,
                    converter=forms.float_converter(),
                    ps=self.tb,
                    key=osmocom_siggen.GAIN_KEY(gain_name),
                    label=gain_name + " Gain (dB)",
                )
                gain_hbox.AddSpacer(5)
                forms.slider(
                    parent=self.panel, sizer=gain_hbox,
                    proportion=2,
                    ps=self.tb,
                    key=osmocom_siggen.GAIN_KEY(gain_name),
                    minimum=range.start(),
                    maximum=range.stop(),
                    step_size=range.step(),
                )
                gain_hbox.AddSpacer(3)

        ##################################################
        # Bandwidth controls
        ##################################################
        try:

            bw_range = self.tb[osmocom_siggen.BWIDTH_RANGE_KEY]
            #print bw_range.to_pp_string()
            if bw_range.start() < bw_range.stop():
                bwidth_vbox = forms.static_box_sizer(parent=self.panel,
                                                     label="Bandwidth",
                                                     orient=wx.VERTICAL,
                                                     bold=True)
                bwidth_vbox.AddSpacer(3)
                bwidth_hbox = wx.BoxSizer(wx.HORIZONTAL)
                bwidth_vbox.Add(bwidth_hbox, 0, wx.EXPAND)
                bwidth_vbox.AddSpacer(3)

                self.vbox.Add(bwidth_vbox, 0, wx.EXPAND)
                self.vbox.AddSpacer(5)
                self.vbox.AddStretchSpacer()

                bwidth_hbox.AddSpacer(3)
                forms.text_box(
                    parent=self.panel, sizer=bwidth_hbox,
                    proportion=1,
                    converter=forms.float_converter(),
                    ps=self.tb,
                    key=osmocom_siggen.BWIDTH_KEY,
                    label="Bandwidth (Hz)",
                )
                bwidth_hbox.AddSpacer(5)
                forms.slider(
                    parent=self.panel, sizer=bwidth_hbox,
                    proportion=2,
                    ps=self.tb,
                    key=osmocom_siggen.BWIDTH_KEY,
                    minimum=bw_range.start(),
                    maximum=bw_range.stop(),
                    step_size=bw_range.step(),
                )
                bwidth_hbox.AddSpacer(3)

        except RuntimeError:
            pass

        ##################################################
        # DC Offset controls
        ##################################################

        dc_offset_vbox = forms.static_box_sizer(parent=self.panel,
                                         label="DC Offset Correction",
                                         orient=wx.VERTICAL,
                                         bold=True)
        dc_offset_vbox.AddSpacer(3)
        # First row of sample rate controls
        dc_offset_hbox = wx.BoxSizer(wx.HORIZONTAL)
        dc_offset_vbox.Add(dc_offset_hbox, 0, wx.EXPAND)
        dc_offset_vbox.AddSpacer(3)

        # Add frequency controls to top window sizer
        self.vbox.Add(dc_offset_vbox, 0, wx.EXPAND)
        self.vbox.AddSpacer(3)

        dc_offset_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=dc_offset_hbox,
            label='Real',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.DC_OFFSET_REAL
        )
        dc_offset_hbox.AddSpacer(3)

        forms.slider(
            parent=self.panel, sizer=dc_offset_hbox,
            proportion=3,
            minimum=-1,
            maximum=+1,
            step_size=0.001,
            ps=self.tb,
            key=osmocom_siggen.DC_OFFSET_REAL
        )
        dc_offset_hbox.AddSpacer(3)

        dc_offset_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=dc_offset_hbox,
            label='Imag',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.DC_OFFSET_IMAG
        )
        dc_offset_hbox.AddSpacer(3)

        forms.slider(
            parent=self.panel, sizer=dc_offset_hbox,
            proportion=3,
            minimum=-1,
            maximum=+1,
            step_size=0.001,
            ps=self.tb,
            key=osmocom_siggen.DC_OFFSET_IMAG
        )
        dc_offset_hbox.AddSpacer(3)

        ##################################################
        # IQ Imbalance controls
        ##################################################

        iq_balance_vbox = forms.static_box_sizer(parent=self.panel,
                                         label="IQ Imbalance Correction",
                                         orient=wx.VERTICAL,
                                         bold=True)
        iq_balance_vbox.AddSpacer(3)
        # First row of sample rate controls
        iq_balance_hbox = wx.BoxSizer(wx.HORIZONTAL)
        iq_balance_vbox.Add(iq_balance_hbox, 0, wx.EXPAND)
        iq_balance_vbox.AddSpacer(3)

        # Add frequency controls to top window sizer
        self.vbox.Add(iq_balance_vbox, 0, wx.EXPAND)
        self.vbox.AddSpacer(3)

        iq_balance_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=iq_balance_hbox,
            label='Mag',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.IQ_BALANCE_MAG
        )
        iq_balance_hbox.AddSpacer(3)

        forms.slider(
            parent=self.panel, sizer=iq_balance_hbox,
            proportion=3,
            minimum=-1,
            maximum=+1,
            step_size=0.001,
            ps=self.tb,
            key=osmocom_siggen.IQ_BALANCE_MAG
        )
        iq_balance_hbox.AddSpacer(3)

        iq_balance_hbox.AddSpacer(3)
        forms.text_box(
            parent=self.panel, sizer=iq_balance_hbox,
            label='Phase',
            proportion=1,
            converter=forms.float_converter(),
            ps=self.tb,
            key=osmocom_siggen.IQ_BALANCE_PHA
        )
        iq_balance_hbox.AddSpacer(3)

        forms.slider(
            parent=self.panel, sizer=iq_balance_hbox,
            proportion=3,
            minimum=-1,
            maximum=+1,
            step_size=0.001,
            ps=self.tb,
            key=osmocom_siggen.IQ_BALANCE_PHA
        )
        iq_balance_hbox.AddSpacer(3)

        ##################################################
        # Sample Rate controls
        ##################################################
        sam_hbox = forms.static_box_sizer(parent=self.panel,
                                          label="Sample Rate",
                                          orient=wx.HORIZONTAL,
                                          bold=True)
        self.vbox.Add(sam_hbox, 0, wx.EXPAND)
        self.vbox.AddSpacer(5)
        self.vbox.AddStretchSpacer()
        sam_hbox.AddStretchSpacer(20)
        forms.static_text(
            parent=self.panel, sizer=sam_hbox,
            label='Sample Rate (sps)',
            ps=self.tb,
            key=osmocom_siggen.SAMP_RATE_KEY,
            converter=forms.float_converter(),
        )
        sam_hbox.AddStretchSpacer(20)

def main():
    try:
        # Get command line parameters
        (options, args) = osmocom_siggen.get_options()

        # Create the top block using these
        tb = osmocom_siggen.top_block(options, args)

        # Create the GUI application
        app = gui.app(top_block=tb,                     # Constructed top block
                      gui=app_gui,                      # User interface class
                      options=options,                  # Command line options
                      args=args,                        # Command line args
                      title="osmocom Signal Generator", # Top window title
                      nstatus=1,                        # Number of status lines
                      start=True,                       # Whether to start flowgraph
                      realtime=True)                    # Whether to set realtime priority

        # And run it
        app.MainLoop()

    except (RuntimeError, e):
        print (e)
        sys.exit(1)

# Make sure to create the top block (tb) within a function: That code
# in main will allow tb to go out of scope on return, which will call
# the decontructor on radio device and stop transmit.  Whats odd is that
# grc works fine with tb in the __main__, perhaps its because the
# try/except clauses around tb.
if __name__ == "__main__": main()
