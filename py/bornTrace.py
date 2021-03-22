import os
import math

MTU= 1500

def consSingleline():
    bd = 12 #Mbit/s
    trace = '/home/wanwenkai/sourceData/self-born/singleline/'+str(bd)+'Mbps.trace'

    duration = 30000 #ms
    
    ret = 0.0
    for t in range(duration):
        #sumbyte = (math.sin(2*math.pi/1000.0*t)+1)*(12*1024*1024/8/1000) + ret
        sumbyte = bd*1024*1024.0/8/1000 + ret
        npacket = int(sumbyte/MTU)
        ret = float(sumbyte%MTU)
        
        if npacket != 0:
            for n in range(npacket):
                with open(trace,'a') as bwf:
                    bwf.write('%d\n' % t)
    
    fd = open(trace, 'r')
    npack = 0
    for line in fd.readlines():
        npack += 1
        time = float(line)
    fd.close()

    bd = (npack*MTU*8.0/1024/1024)/(time/1000) #Mbit/s
    print 'fluc single line %.2fMbit/s' % bd

def flucSingleline():
    trace = '/home/wanwenkai/sourceData/self-born/singleline/fluc50-100.trace'

    duration = 30000 #ms
    
    i = 0
    ret = 0.0

    for t in range(duration):
        if t % 500 == 0:
            i += 1 
        if i%2 == 0:
            sumbyte = (100*1024*1024/8/1000) + ret
        else:
            sumbyte = (50*1024*1024/8/1000) + ret

        npacket = int(sumbyte/MTU)
        ret = float(sumbyte%MTU)
        
        if npacket != 0:
            for n in range(npacket):
                with open(trace,'a') as bwf:
                    bwf.write('%d\n' % t)
    
    fd = open(trace, 'r')
    npack = 0
    for line in fd.readlines():
        npack += 1
        time = float(line)
    fd.close()

    bd = (npack*MTU*8.0/1024/1024)/(time/1000) #Mbit/s
    print 'fluc single line %.2fMbit/s' % bd

def consDoubleline():
    bd = 6 #Mbit/s
    
    trace = '/home/wanwenkai/sourceData/self-born/doubleline/6Mbps.txt'
    duration = 30000 #ms
    
    ret = 0.0
    for t in range(duration):
        if t%100 == 0: 
            pointbyte = bd*1024*1024.0/8/1000 * 100 
            with open(trace,'a') as bwf:
                bwf.write('%.2f %.f\n' % (t*1.0/1000, pointbyte))
    
    fd = open(trace, 'r')
    pointbyteL = []
    for line in fd.readlines():
        info = line.split()
        time = float(info[0])
        byte = float(info[1])
        pointbyteL.append(byte)
    fd.close()

    bd = (sum(pointbyteL)*8.0/1024/1024)/time #Mbit/s
    print 'constant double line %.2fMbit/s' % bd
    

def main():
    #consDoubleline()
    consSingleline()
    #flucSingleline()

if __name__=="__main__":
    main()
