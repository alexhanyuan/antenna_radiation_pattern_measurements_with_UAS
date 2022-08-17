import rx_mag
from datetime import datetime
import sys
import argparse
import multiprocessing

parser = argparse.ArgumentParser()
parser.add_argument('--frequency', type=int, default=445900000, help='Tune frequency in Hz')
parser.add_argument('--samp_rate', type=int, default=1000000, help='Sample rate in Hz (default = 1M)')
parser.add_argument('--num_samps', type=int, default=10000, help='Number of samples (default = 10k)')
parser.add_argument('--RF_gain', type=int, default=20, help='HackRF RF gain (default = 20)')
parser.add_argument('--wav_scaling', type=float, default=0.5, help='Amplitude scaling in .wav, should not need to be changed (default = 0.5)')
parser.add_argument('--position', type=int, default=0, help='Position identifier (filenaming only)')

args = parser.parse_args()
args.filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '_freq_' + str(args.frequency) + '_fs_' + str(args.samp_rate) + str(args.position)

# run grc flowgraph
rx_mag.main(options=args)