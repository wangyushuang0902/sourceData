import argparse
import os

def allFiles():
    print 'start'
    _path = '/home/wanwenkai/sourceData/mahimahi-traces/singleTraces/'
    dpath = '/home/wanwenkai/sourceData/mahimahi-traces/doubleTraces/'
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
            double_path = os.path.join(dpath, '%s-down.txt'%file_name.split('.down')[0])
            todouble(file_path, double_path)
        if file_name.endswith('.up'):
            print file_name
            file_path = os.path.join(_path, file_name)
            double_path = os.path.join(dpath, '%s-up.txt'%file_name.split('.up')[0])
            todouble(file_path, double_path)

def todouble(file_path, double_path):
    i = 0
    time_old = 0
    pact = 0
    ft = open(file_path,'r')
    for line in ft.readlines():
        i+=1
        time_new = int(line)
        pact += 1
        if time_new >= time_old + 100:
            with open(double_path,'a') as bwf:
                time = time_new/1000.0
                bw = pact*1500.0
                bwf.write('%.3f %.1f\n' % (time,bw))
                pact = 0
            time_old = time_new

    if pact != 0:
        with open(double_path,'a') as bwf:
            time = time_new/1000.0
            bw = pact*1500.0
            bwf.write('%.3f %.1f\n' % (time,bw))

    avbw = i*1500.0/(time)
    print avbw,'byte/s'

if __name__ == '__main__':
    #allFiles()
    _path = '/home/wanwenkai/sourceData/'
    file_path = '/home/wanwenkai/sourceData/mahimahi-traces/singleTraces/ATT-LTE-driving.up'
    file_name = 'ATT-LTE-driving.up'
    double_path = os.path.join(_path, '%s-up.txt'%file_name.split('.up')[0])
    todouble(file_path, double_path)
