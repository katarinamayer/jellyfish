import pickle
from tabulate import tabulate

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

ecmp = load_obj('../routes/pickled/ecmp_test.pkl')
ksp = load_obj('../routes/pickled/ksp_test.pkl')
dsp = load_obj('../routes/pickled/dsp_test.pkl')

def average_num_paths(d):
	paths = []
	for key in d:
		num_paths = len(d[key])
		paths.append(num_paths)

	return sum(paths) / len(paths)

def average_path_length(d):
	path_lens = []
	for key in d:
		num_paths = len(d[key])
		total_path_len = 0
		for path in d[key]:
			total_path_len += len(path)

		av_len = total_path_len/num_paths
		path_lens.append(av_len)

	return sum(path_lens) / len(path_lens)


ecmp_num_paths = average_num_paths(ecmp)
dsp_num_paths = average_num_paths(dsp)
ksp_num_paths = average_num_paths(ksp)

ecmp_path_lens = average_path_length(ecmp)
ksp_path_lens = average_path_length(ksp)
dsp_path_lens = average_path_length(dsp)

print(tabulate([['ECMP', ecmp_num_paths, ecmp_path_lens], ['K-Shortest Paths', ksp_num_paths, ksp_path_lens], ['K-Diverse Short Paths', dsp_num_paths, dsp_path_lens]], headers=['Average # Paths', 'Average Path Length']))

