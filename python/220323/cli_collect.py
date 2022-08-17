import rx_fft_mag
from datetime import datetime
import sys
import textwrap
import argparse
import multiprocessing

parser = argparse.ArgumentParser(
    prog='CLI received power recorder',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\
         additional info:
             blah blah info
         '''))
parser.add_argument('--frequency', type=int, default=446000000, help='Receive frequency in Hz. SDR will tune 200kHz lower.')
parser.add_argument('--RF_gain', type=int, default=32, help='HackRF RF gain (default = 32)')
parser.add_argument('--position', type=int, default=0, help='Position identifier (filenaming only)')

parser.add_argument('--samp_rate', type=int, default=1000000, help='Sample rate in Hz (default = 1M). Probably do not change this, it will break things.')
parser.add_argument('--num_buffers', type=int, default=10, help='Number of buffers (default = 10)')

args = parser.parse_args()
args.filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '_freq_' + str(args.frequency) + '_fs_' + str(args.samp_rate) + str(args.position)

# run grc flowgraph
rx_fft_mag.main(options=args)