import argparse
import os

def allFiles():
    print 'start'
    _path = '/home/wanwenkai/sourceData/mahimahi-traces/traces/'
    print 'read _path'
    for file_name in os.listdir(_path):
    #dst_datadir = 'verify_sourceData_' + str(int(runtime))
        '''
        if file_name.endswith('down.txt'):
            file_path = os.path.join(_path, file_name)
            os.remove(file_path)
        '''
        if file_name.endswith('.down'):
            print file_name
            file_path = os.path.join(_path, file_name)
            double_path = os.path.join(_path, '%s-down.txt'%file_name.split('.down')[0])
            todouble(file_path, double_path)

def todouble(file_path, double_path):
    #exist = os.path.exists(file_path)
    #if exist == True:
    #    with open(file_path,'r') as bwf:
    #        bwf.truncate()
    i = 0
    ts_old = 0
    tpnum = 1
    tpnum_max = 0
    tpnum_max_100 = 0
    gra = 0
    ft = open(file_path,'r')
    for line in ft.readlines():
        i+=1
        ts_new = int(line)
        
        if ts_new == ts_old:
            tpnum += 1
        else:
            tpnum = 1
        if ts_old != 0:
            if tpnum == 1:
                gra = ts_old%100.0
                if gra == 0.0:
                   # print gra
                    if tpnum_max_100 != 0: 
                        with open(double_path,'a') as bwf:
                            time = ts_old/1000.0
                            bw = tpnum_max_100*1500.0
                            bwf.write('%.3f %.1f\n' % (time,bw))
                            tpnum_max_100 = 0
                else:
                    tpnum_max_100 += tpnum_max 

        tpnum_max = tpnum
        ts_old = ts_new
 
    with open(double_path,'a') as bwf:
        time = ts_old/1000.0
        bw = tpnum_max_100*1500.0
        bwf.write('%.3f %.1f\n' % (time,bw))
    
    avbw = i*1500.0/(time)
    print avbw,'byte/s'

if __name__ == '__main__':
    #allFiles()
    _path = '/home/wanwenkai/sourceData/'
    file_path = '/home/wanwenkai/sourceData/proUDP_386750.txt'
    file_name = 'proUDP_386750.txt'
    double_path = os.path.join(_path, '%s.trace'%file_name.split('.txt')[0])
    todouble(file_path, double_path)
