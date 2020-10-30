import shutil
import os

def cut0(temp):
    for filen in os.listdir(temp):
        if not filen.startswith('no'):

            cut = 0
            filep = os.path.join(temp, filen)
            fd = open(filep, 'r')
            t_old = 0.0
        
            for line in fd.readlines():
                tb = line.split()
                t = float(tb[0])
            
                if cut == 0:
                    if t-t_old > 2.0:
                        print filen,
                        dst_filen = 'no'+filen
                        dst_filep = os.path.join(temp, dst_filen)
                        os.rename(filep, dst_filep)    
                        print ' cut! delta=%.2f t_old=%.2f t=%.2f'%(t-t_old,t_old,t)
                        cut = 1
                t_old = t
        
            if cut == 0:
                if t < 29.0:
                    print filen,
                    dst_filen = 'no'+filen
                    dst_filep = os.path.join(temp, dst_filen)
                    os.rename(filep, dst_filep)    
                    print ' cut! t=%.2f'%t


def keepRuntime(filespath, files, way):
    temp = '/home/wanwenkai/sourceData/mahimahi-traces/temp/'
    if not os.path.exists(temp):
        os.makedirs(temp)

    sum_b = 0.0
    num = 1
    for line in open(filespath):
        tb = line.split()
        if tb[0] != '#':
            time_str = tb[0]
            byte_str = tb[1]
            time = float(time_str)
            byte = float(byte_str)
            sum_b += byte
            if time <= runtime*num:
                file_name = files.split('.txt')[0] + str(num) + '.txt'
                interpath = os.path.join(temp, file_name)
                with open(interpath, 'a') as inter:
                    inter.write('%.2f %s\n'% (time-runtime*(num-1),byte_str))
                bd = sum_b/(time-runtime*(num-1))
            else:
                #print interpath,
                #print ' %.2f bytes/s' % bd
                sum_b = 0.0 
                num += 1
                #print num
    cut0(temp)
    nolevel(temp)

def nolevel(temp):
    dst = '/home/wanwenkai/sourceData/mahimahi-traces/mahi-30/nolevel/downlink_0'
    if not os.path.exists(dst):
        os.makedirs(dst)
    for filen in os.listdir(temp):
        if not filen.startswith('no'):
            filep = os.path.join(temp, filen)
            shutil.copy(filep, dst) 


def verify_level(delta, source):
    dst = '/home/wanwenkai/sourceData/mahimahi-traces/mahi-30'
    for d in os.listdir(dst):
        if d.startswith('downlink'):
            dp = os.path.join(dst, d)
            shutil.rmtree(dp)
    dst = os.path.join(dst, 'level')
    for filen in os.listdir(source):
        if not filen.startswith('no'):
            filep = os.path.join(source, filen)
            bd = countbd(filep)
            level = int(bd//delta)
            downlink = 'downlink_' + str(level*delta)
            dst_lp = os.path.join(dst, downlink)
            dst_filep = os.path.join(dst_lp, filen)
            if not os.path.exists(dst_lp):
                os.makedirs(dst_lp)
            #if os.path.isfile(dst_filepath):
            #    os.remove(dst_filepath)
            shutil.copy(filep, dst_filep)

def countbd(readfile):
    fd = open(readfile);
    
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
    avgbd = sum_b/time1
    return avgbd

def statistics(dst_path):
    m = 0
    for oklevel in os.listdir(dst_path):
        print oklevel
        levelpath = os.path.join(dst_path, oklevel)
        n = 0
        for okfiles in os.listdir(levelpath):
            okfilespath = os.path.join(levelpath, okfiles)
            print okfiles + '  ',
            countbd(okfilespath)
            n += 1
        print ('files num = %d\n' % n)
        m += n
    oksum_num = m
    print ('oksum filesnum = %d' % oksum_num)

def main():
    #dst_datadir = 'mahimahi-traces-' + str(int(runtime))
    #dst_path = os.path.join(path, dst_datadir)
    i = 0
    sum_num = 0
    for txt in os.listdir(datapath):
        if i >= 0:
            if txt.endswith('.txt'):
                print txt
                filespath = os.path.join(datapath, txt)
                #print filespath
                keepRuntime(filespath, txt, 1)
            #verify_level(dst_path, interpath, bd)
            #l += 1
        i += 1
        #sum_num += l 
    #print ('sum filesnum = %d'% sum_num)
    #print ('classify is done!\n')
    
    #statistics(dst_path)
    
if __name__ == '__main__':
    #global datapath, dst_path, runtime
    datapath = '/home/wanwenkai/sourceData/mahimahi-traces/doubleTraces/' 
    runtime = 30.0     #s
    dst_rootpath = '/home/wanwenkai/sourceData/mahimahi-traces/'
    dst_dir = 'mahi-doubleTraces-' + str(int(runtime))
    dst_path = os.path.join(dst_rootpath, dst_dir)
    #main()
    delta = 100000 #byte/s
    temp = '/home/wanwenkai/sourceData/mahimahi-traces/temp'
    verify_level(delta, temp) 
    #filespath = '/home/wanwenkai/sourceData/mahimahi-traces/traces/ATT-LTE-driving-2016-down.txt'
    #txt = 'ATT-LTE-driving-2016-down.txt'
    #print txt
    #keepRuntime(filespath, txt, 1)
    #statistics(dst_path)
