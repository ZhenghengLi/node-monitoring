#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='desc')
parser.add_argument("csvfile")
parser.add_argument("-s", dest="start_time", type=int, default=-1)
parser.add_argument("-l", dest="span_sec", type=int, default=-1)
parser.add_argument("-t", dest="title", type=str, default='CPU load')
parser.add_argument("-y", dest="ylim", type=int, default=30)
args = parser.parse_args()


attr_list = ['user', 'system', 'idle', 'iowait',
             'irq', 'softirq', 'steal', 'guest']

csv_fields = ['unixtime'] + attr_list + ['memory']

with open(args.csvfile, 'r') as fin:
    reader = csv.DictReader(fin, fieldnames=csv_fields)
    # skip header
    next(reader)
    data = list(reader)

if args.start_time < 0:
    args.start_time = float(data[0]['unixtime'])
if args.span_sec < 0:
    args.span_sec = float(data[-1]['unixtime']) - args.start_time

deltatime = []      # unixtime - args.start_time
cpu_user = []       # user
cpu_system = []     # system
cpu_softirq = []    # softirq
cpu_total = []      # 100 - idle

print('scanning data ...')
for row in data:
    cur_delta = float(row['unixtime']) - args.start_time
    if (cur_delta < 0 or cur_delta > args.span_sec):
        continue
    print(row)
    deltatime.append(cur_delta)
    cpu_user.append(float(row['user']))
    cpu_system.append(float(row['system']))
    cpu_softirq.append(float(row['softirq']))
    cpu_total.append(100 - float(row['idle']))

print('start_time:', args.start_time)
print('span_sec:', args.span_sec)

plt.figure(figsize=(12, 7))
plt.plot(deltatime, cpu_total, linewidth=2)
plt.plot(deltatime, cpu_user, linewidth=2)
plt.plot(deltatime, cpu_system, linewidth=2)
plt.plot(deltatime, cpu_softirq, linewidth=2)

plt.ylim(0, args.ylim)
plt.xlabel('delta time (s)', fontsize=18)
plt.ylabel('cpu usage (%)', fontsize=18)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(['total', 'user', 'system', 'softirq'], prop={'size': 18})
plt.title(args.title, fontsize=18)
plt.grid()

plt.show()
