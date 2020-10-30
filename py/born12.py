from os import path 

def main():
    
    #trace_path = "/home/wanwenkai/pqsaSimulator/wang/simulator_scripts/verify_sourceData/downlink_1500000/12mbpsdoubleline.txt"
    
    trace_path = "12mbpsdoubleline.txt"
    time = 0.0
    time_all = 300
    bw = 157286.4
    
    print 'Hello World'
    with open(trace_path,'a') as trace:
        for line in range(time_all):
            trace.write('%.3f %.1f\n' % (time, bw))
            time += 0.1

if __name__ == '__main__':
    main()
