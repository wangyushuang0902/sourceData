import os
import glob
import shutil

root = '/home/wanwenkai/sourceData/mahimahi-traces/'

def main(provider, filen):
    global dst
    datap = os.path.join(root, 'doubleTraces')
    #filen = 'ATT-LTE-driving-2016-down.txt'
    datap = os.path.join(datap, filen)
    fd = open(datap, 'r')
    
    dst_root = os.path.join(root, provider)
    dst = os.path.join(dst_root, 'all')
    if not os.path.exists(dst):
        os.makedirs(dst)

    tL = []
    bL = []
    t_old = 0.0
    num = 0
    used = 0
    for line in fd.readlines():
        tb = line.split()
        t = float(tb[0])
        b = float(tb[1])
        if t <= 30.0 + 30.0*num:
            tL.append(t)
            bL.append(b)
        else:
            #if used == 0:
            throw = 0
            for b in bL:
                if b == 0.0:
                    throw = 1
            if throw == 1:
                tL = []
                bL = []
                tL.append(t)
                bL.append(b)
            else:
                bd = sum(bL)/(tL[-1]-30*num)
                
                if bd != 0.0:
                    #level = int(bd/700000)
                    #downlink = 'downlink_' + str(level*100000)
                    downlink = 'downlink_0'
                    dst_dir = os.path.join(dst, downlink)
                    #files = 'NewFile-HighDensity-4GMobile-ms'+str(num+1)+'.txt'
                    tmp = filen.split('.')
                    files = tmp[0] + str(num+1) + '.txt'
                    dst_file = os.path.join(dst_dir, files)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    if not os.path.isfile(dst_file):
                        wf = open(dst_file, 'a')
                        for i in range(len(tL)):
                            wf.write('%.2f %.2f\n'%(tL[i]-30*num, bL[i]))
                        wf.close()
                
                #used = 1
                tL = []
                bL = []
                tL.append(t)
                bL.append(b)

                #print downlink
                print '%s %.2f'%(files, bd)
            
        if t > 30*(num+1):
            num += 1
            used = 0

def tl(provider):
    p = 0.9
    #root = 'home/wanwenkai/sourceData/mahimahi-traces/' 
    fdir = os.path.join(root, provider)
    tp = os.path.join(fdir, provider + '-train')
    lp = os.path.join(fdir, provider + '-label')
    for dirs in os.listdir(dst):
        if dirs.startswith('downlink_'):
            dirp = os.path.join(dst, dirs)
            num = 0
            files_list = glob.glob(dirp + '/*.txt')
            file_num = len(files_list)
            train_num = p*file_num
            dst_tp = os.path.join(tp, dirs)
            dst_lp = os.path.join(lp, dirs)
            if not os.path.exists(dst_tp):
                os.makedirs(dst_tp)
            
            if not os.path.exists(dst_lp):
                os.makedirs(dst_lp)
            
            for files in os.listdir(dirp):
                num += 1
                filep = os.path.join(dirp, files)
                if num <= train_num:
                    dst_t = os.path.join(dst_tp, files)
                    shutil.copyfile(filep, dst_t)
                else:
                    dst_l = os.path.join(dst_lp, files)
                    double_to_single(filep, dst_l)
                    #shutil.copyfile(filep, dst_l)

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


def statistic(provider):
    fdir = os.path.join(root, provider)
    t = os.path.join(fdir, provider + '-train')
    l = os.path.join(fdir, provider + '-label')
    #print t
    sum_t = 0
    for dirs in os.listdir(t):
        #print dirs,
        #print ' ',
        d = os.path.join(t, dirs)
        files_list = glob.glob(d + '/*.txt')
        num = len(files_list)
        #print num
        sum_t += num
    print 'sum_trainfile_num = %d'%sum_t
    
    #print l
    sum_l = 0
    for dirs in os.listdir(l):
        #print dirs,
        #print ' ',
        d = os.path.join(l, dirs)
        files_list = glob.glob(d + '/*.txt')
        num = len(files_list)
        #print num
        sum_l += num
    print 'sum_labelfile_num = %d'%sum_l

if __name__ == '__main__':
    filen = 'TMobile-UMTS-driving-down.txt'
    #provider = 'ATT-4G'
    #provider = 'TMobile-3G'
    #provider = 'TMobile-4G'
    #provider = 'Verizon-3G'
    provider = 'Verizon-4G'
    #main(provider, 'ATT-LTE-driving-2016-down.txt')
    #main(provider, 'ATT-LTE-driving-down.txt')
    #main(provider, filen)
    #main(provider, 'TMobile-LTE-driving-down.txt')
    #main(provider, 'TMobile-LTE-short-down.txt')
    #main(provider, 'Verizon-EVDO-driving-down.txt')
    main(provider, 'Verizon-LTE-driving-down.txt')
    main(provider, 'Verizon-LTE-short-down.txt')
    tl(provider)
    statistic(provider)
