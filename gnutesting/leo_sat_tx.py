#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import gnuradio.leo



from gnuradio import qtgui

class leo_sat_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "leo_sat_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.satellite_tx_antenna = satellite_tx_antenna = gnuradio.leo.antenna.dipole_antenna.make(5, 435.769e6, 3, 0)
        self.satellite_rx_antenna = satellite_rx_antenna = gnuradio.leo.antenna.dipole_antenna.make(5, 435.765e6, 3, 0)
        self.variable_satellite_0 = variable_satellite_0 = gnuradio.leo.satellite.make('UPSAT', '1 25544U 98067A   18268.52547184  .00016717  00000-0  10270-3 0  9019', '2 25544  51.6373 238.6885 0003885 206.9748 153.1203 15.53729445 14114', 435e6, 435e6, 27, satellite_tx_antenna, satellite_rx_antenna, 12, 190, 1200)
        self.tracker_tx_antenna = tracker_tx_antenna = gnuradio.leo.antenna.yagi_antenna.make(0,435.765e6, 0, 0, 2.35)
        self.tracker_rx_antenna = tracker_rx_antenna = gnuradio.leo.antenna.yagi_antenna.make(0,435.769e6, 2, 0, 0)
        self.variable_tracker_0 = variable_tracker_0 = gnuradio.leo.tracker.make(variable_satellite_0, 35.3333, 25.1833, 0, '2018-09-25T15:48:25.0000000Z', '2018-09-25T15:58:35.0000000Z', 1e6, 435e6, 435e6, 37, tracker_tx_antenna, tracker_rx_antenna, 1, 210, 19200)
        self.variable_leo_model_def_0 = variable_leo_model_def_0 = gnuradio.leo.model.leo_model.make(variable_tracker_0, 1, 5,
          													0, 7,
          													1, 3,
          													True, 7.5, 0, 25)
        self.samp_rate_tx = samp_rate_tx = 1e6
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_gr_complex, 1, '10.0.0.2', 2000,1)
        self.leo_channel_model_0 = gnuradio.leo.channel_model.make(80000, variable_leo_model_def_0, 1, 0, '')
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=2,
            mod_code="gray",
            differential=True,
            samples_per_symbol=64,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1000)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 100e-6, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.leo_channel_model_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.leo_channel_model_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.leo_channel_model_0, 0), (self.blocks_add_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "leo_sat_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_satellite_tx_antenna(self):
        return self.satellite_tx_antenna

    def set_satellite_tx_antenna(self, satellite_tx_antenna):
        self.satellite_tx_antenna = satellite_tx_antenna
        self.satellite_tx_antenna.set_pointing_error(0)

    def get_satellite_rx_antenna(self):
        return self.satellite_rx_antenna

    def set_satellite_rx_antenna(self, satellite_rx_antenna):
        self.satellite_rx_antenna = satellite_rx_antenna
        self.satellite_rx_antenna.set_pointing_error(0)

    def get_variable_satellite_0(self):
        return self.variable_satellite_0

    def set_variable_satellite_0(self, variable_satellite_0):
        self.variable_satellite_0 = variable_satellite_0

    def get_tracker_tx_antenna(self):
        return self.tracker_tx_antenna

    def set_tracker_tx_antenna(self, tracker_tx_antenna):
        self.tracker_tx_antenna = tracker_tx_antenna
        self.tracker_tx_antenna.set_pointing_error(0)

    def get_tracker_rx_antenna(self):
        return self.tracker_rx_antenna

    def set_tracker_rx_antenna(self, tracker_rx_antenna):
        self.tracker_rx_antenna = tracker_rx_antenna
        self.tracker_rx_antenna.set_pointing_error(0)

    def get_variable_tracker_0(self):
        return self.variable_tracker_0

    def set_variable_tracker_0(self, variable_tracker_0):
        self.variable_tracker_0 = variable_tracker_0

    def get_variable_leo_model_def_0(self):
        return self.variable_leo_model_def_0

    def set_variable_leo_model_def_0(self, variable_leo_model_def_0):
        self.variable_leo_model_def_0 = variable_leo_model_def_0

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=leo_sat_tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
