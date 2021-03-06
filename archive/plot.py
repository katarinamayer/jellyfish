# plot.py 
# plot average path counts and lengths from quick sampling of data

import matplotlib.pyplot as plt

hosts = [20, 30, 40, 50]
ecmp_path_nums = [2.03, 1.89, 2.09, 2.19]
ksp_path_nums = [8, 8, 8, 8]
dsp_path_nums = [2.77, 3.73, 3.77, 4.0]

ecmp_path_len = [2.9, 3.15, 3.19, 3.31]
ksp_path_len = [4.14, 4.3, 4.42, 4.45]
dsp_path_len = [3.3, 3.7, 3.77, 3.85]

fig = plt.figure()
fig, ax = plt.subplots(figsize=(8, 4.5))
servers = []
# for i in range(len(hosts)):
# 	servers.append(hosts[i]/2)

ax.plot(hosts, ecmp_path_nums, label='ECMP', marker='.')
ax.plot(hosts, ksp_path_nums, label='8-Shortest Paths', marker='.')
ax.plot(hosts, dsp_path_nums, label='8-Diverse Short Paths', marker='.')

plt.xlabel('Number of Hosts', fontsize=12)
plt.ylabel('Average # of Paths', fontsize=12)
plt.title('Sample Average # Paths', fontsize=11)
plt.xticks(hosts)

plt.ylim(1, 15)  
ax.legend()
plt.show()

fig = plt.figure()
fig, ax = plt.subplots(figsize=(8, 4.5))
servers = []
# for i in range(len(hosts)):
# 	servers.append(hosts[i]/2)

ax.plot(hosts, ecmp_path_len, label='ECMP', marker='.')
ax.plot(hosts, ksp_path_len, label='8-Shortest Paths', marker='.')
ax.plot(hosts, dsp_path_len, label='8-Diverse Short Paths', marker='.')

plt.xlabel('Number of Hosts', fontsize=12)
plt.ylabel('Average Path Length', fontsize=12)
plt.title('Sample Average Path Length', fontsize=11)
plt.xticks(hosts)
plt.ylim(2,5)

ax.legend()
plt.show()
