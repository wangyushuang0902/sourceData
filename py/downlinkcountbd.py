#!/usr/bin/env python
import os 

datapath = '/home/wanwenkai/pqsaSimulator/wang/simulator_scripts/verify_sourceData/'
downlink = 'downlink_1000000'

def main():
    #fd = open("30doubleline.txt");
    #fd = open("downlink_1500000/12mbpsdoubleline.txt");
    path = os.path.join(datapath, downlink)
    for files in os.listdir(path):
        trace = os.path.join(path, files)
        fd = open(trace)
        bandwidth = 0.0
        time1 = 0.0
        sum_b = 0.0
        for line in fd.readlines():
    
            if line[0] != '#':
                tb = line.split()
                bandwidth_str = tb[1]
                bandwidth = float(bandwidth_str)
                sum_b += bandwidth
                time1_str = tb[0]
                time1 = float(time1_str)


    #mbit = sum_b*8/(1024*1024)
    #bd = mbit/time1
        bd = sum_b/time1
        print (files + '   %.2f bytes/s'% bd)

if __name__ == '__main__':
    main()
