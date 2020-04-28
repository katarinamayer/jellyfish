# process.py
# Last revised 4/26/20
# Script to process and output results for 1 round of experiments

from tabulate import tabulate
from os import path

def process_eight_conn(filepath):
	printIDline = True
	transfer = []
	bandwidth = []
	latency = []

	with open(filepath) as f:
		for line in f:
			if line.startswith('[ ID]') and printIDline == True:
				#print(line)
				printIDline = False

			if line.startswith('[SUM]'):
				#print(line)
				line_ = line.split()

				t = float(line_[3])
				transfer.append(t) # MBits/sec
				
				b = float(line_[5])
				bandwidth.append(b) # MBits/sec

			else:
				
				line = line.split()
				if len(line) == 12 and line[11] == 'us':
					#print(line)
					cwnd_rtt = line[10].split('/')
					latency.append(float(cwnd_rtt[1]))
					#print(cwnd_rtt[1])

		av_transfer = average(transfer)
		av_bandwidth = average(bandwidth)
		av_latency = average(latency)
		#av_latency = ''

		return av_transfer, av_bandwidth, av_latency


def process_single_conn(filepath):
	transfer = []
	bandwidth = []
	latency = []

	with open(filepath) as f:
		for line in f:
			if line.startswith('[  3] 0.00'):
				#print(line)
				line_ = line.split()

				t = float(line_[4])
				transfer.append(t) # MBits/sec
				
				b = float(line_[6])
				bandwidth.append(b) # MBits/sec

				cwnd_rtt = line_[10].split('/')
				latency.append(float(cwnd_rtt[1]))

		av_transfer = average(transfer)
		av_bandwidth = average(bandwidth)
		av_latency = average(latency)

		return av_transfer, av_bandwidth, av_latency


def average(lst):
	return sum(lst) / len(lst)


def results_table(results):

	print(tabulate([['ECMP', results[0][0], results[0][1], results[0][2]], ['8-Shortest Paths', results[1][0], results[1][1], results[1][2]], ['8-Diverse Short Paths', results[2][0], results[2][1], results[2][2]]], headers=['Average Transfer (Mbytes)', 'Average Throughput (Mbits/sec)', 'Average RTT (us)']))


def read_file(filepath):
	if path.exists(filepath):
		if 'eight' in filepath:
			return [x for x in process_eight_conn(filepath)]
		if 'single' in filepath:
			return [x for x in process_single_conn(filepath)]
	else:
		return ['', '', '']


def main():
	
	results = []
	ecmp_results = read_file('perftest/results/ecmp_eight.txt')
	results.append(ecmp_results)

	ksp_results = read_file('perftest/results/ksp_eight.txt')
	results.append(ksp_results)

	dsp_results = read_file('perftest/results/dsp_eight.txt')
	results.append(dsp_results)

	print("\n10 Client/Server Flows, 8 Parallel Connections:")
	results_table(results)

	results_1 = []
	ecmp_1_results = read_file('perftest/results/ecmp_single.txt')
	results_1.append(ecmp_1_results)

	ksp_1_results = read_file('perftest/results/ksp_single.txt')
	results_1.append(ksp_1_results)

	dsp_1_results = read_file('perftest/results/dsp_single.txt')
	results_1.append(dsp_1_results)

	print("\n10 Client/Server Flows, Single Connection:")
	results_table(results_1)


if __name__ == '__main__':
    main()
