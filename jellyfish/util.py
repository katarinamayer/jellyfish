# Last revised 4/23/20
# Auxillary functions for Jellyfish

from __future__ import division
import pickle
import pdb
import os
import networkx as nx
import random
from itertools import islice
import matplotlib.pyplot as plt


def save_obj(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj,f,protocol=0)
        

def load_obj(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def transform_paths_dpid(paths_file_name, maxLen):
	all_paths = load_obj(paths_file_name)
	table = {}
	for key, value in all_paths.items():
		key_dpid = (switch_to_dpid(key[0]), switch_to_dpid(key[1]))
		table[key_dpid] = []
		reversed_key = (switch_to_dpid(key[1]), switch_to_dpid(key[0]))
		table[reversed_key] = []
		for path in value[:maxLen]:
			transformed_path = list(map(switch_to_dpid, path))
			table[key_dpid].append(transformed_path)
			table[reversed_key].append(transformed_path[::-1])
	return table

def switch_to_dpid(switchIndex):
	return str(switchIndex) + "_1"

