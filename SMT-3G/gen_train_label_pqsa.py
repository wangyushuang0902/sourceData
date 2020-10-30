#!/usr/bin/env python
import shutil
import os 
import glob
#from fraction import Fraction

def double_to_single(transfiles_path, dst_label_filespath):
    sum_b = 0.0
    ret = 0.0
    time_old = 0.0
    for line in open(transfiles_path):
        tb = line.split()
        bandwidth_str = tb[1]
        time1_str = tb[0]
        time_new = float(time1_str)
        byte = float(bandwidth_str)
        sum_b += byte
        #num_packets
        ret += byte/1500
        if ret >=1.0:
            num_packets =int(ret)    
            #print num_packets
            ret = ret-num_packets
        else:
            continue
        delta_pactime = (time_new - time_old)/num_packets
        #print delta_pactime
        for i in range(num_packets):
            time_w = time_old + delta_pactime*( i+ 1)
            with open(dst_label_filespath,'a') as trace:
                time = time_w*1000
                trace.write('%d\n' % time)
        time_old = time_new
    #print sum_b/time_new

def statistics(dst_path, okdir, tr_or_la):
    print('\n' + okdir)
    m = 0
    levelL = range(0, 5)
    for level in levelL:
        downlink = 'downlink_'+str(level*100000)
        for oklevel in os.listdir(dst_path):
            if oklevel == downlink:
                print oklevel,
                levelpath = os.path.join(dst_path, oklevel)
                n = 0
                for okfiles in os.listdir(levelpath):
                    okfilespath = os.path.join(levelpath, okfiles)
            #countbd(okfilespath, tr_or_la)
                    n += 1
                print ' %d' % n
                m += n
    oksum_num = m
    print ('sum filesnum = %d' % oksum_num)

def countbd(okfilespath, tr_or_la):
    sum_b = 0.0
    pac_num = 0
    for line in open(okfilespath):
        pac_num += 1
        if tr_or_la == 0:
            tb = line.split()
            if tb[0] != '#':
                time_str = tb[0]
                byte_str = tb[1]
                time_s = float(time_str)
                byte = float(byte_str)
                sum_b += byte
    if tr_or_la == 0:
        bd = sum_b/time_s
    else:
        time_ms = float(line)
        bd = (pac_num*1500.0)/(time_ms/1000.0)
    print ('%.2f bytes/s' % bd)

def main(root, datadir, p):
    train_dir = 'first24h-30s-5level' + '-train'
    label_dir = 'first24h-30s-5level' + '-label'
    dst_trainpath = os.path.join(root, train_dir)
    dst_labelpath = os.path.join(root, label_dir)
    path = os.path.join(root, datadir)
    for downlink in os.listdir(path):
        #print downlink
        if downlink.startswith('downlink_'):
            downlink_path = os.path.join(path, downlink)
            dst_train_level_path = os.path.join(dst_trainpath, downlink)
            if not os.path.exists(dst_train_level_path):
                os.makedirs(dst_train_level_path)
            dst_label_level_path = os.path.join(dst_labelpath, downlink)
            if not os.path.exists(dst_label_level_path):
                os.makedirs(dst_label_level_path)

            files_list = glob.glob(downlink_path + '/*.txt')
            files_num = len(files_list)
            #print ('files num = %d' % files_num)
            train_num = int(p*files_num) + 1
            i = 0
            for files in os.listdir(downlink_path):
                #print files,
                i += 1
                filespath = os.path.join(downlink_path, files)
                if i <= train_num:
                    dst_train_files_path = os.path.join(dst_train_level_path, files)
                    shutil.copyfile(filespath, dst_train_files_path)
                else:
                    dst_label_files_path = os.path.join(dst_label_level_path, files)
                    double_to_single(filespath, dst_label_files_path)
                    #shutil.copyfile(filespath, dst_label_files_path)
    statistics(dst_trainpath, train_dir, 0)
    statistics(dst_labelpath, label_dir, 1)

if __name__ == '__main__':
    root = '/home/wanwenkai/sourceData/SMT-3G'
    datadir = 'first24h-30s-doubleline-5level'
    p = 0.67   #2/3
    main(root, datadir, p)
