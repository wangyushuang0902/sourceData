import shutil
import os

def keepRuntime(filespath, files):
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
                file_name = files.split('.txt')[0] + '_' + str(num) + '.txt'
                interpath = os.path.join(temp, file_name)
                with open(interpath, 'a') as inter:
                    inter.write('%.2f %s\n'% (time-runtime*(num-1),byte_str))
                bd = sum_b/(time-runtime*(num-1))
            else:
                
                level = int(bd//100000)
                downlink = 'downlink_' + str(level*100000)
                dst_levelpath = os.path.join(dst_path, downlink)
                dst_filepath = os.path.join(dst_levelpath, file_name)
                if not os.path.exists(dst_levelpath):
                    os.makedirs(dst_levelpath)
                if not os.path.isfile(dst_filepath):
                    #os.remove(dst_filepath)
                    shutil.move(interpath, dst_levelpath)
                    print interpath
                    print '%.2f bytes/s' % bd
                
                #verify_level(dst_path, interpath, file_name, bd)
                sum_b = 0.0 
                num += 1
                #print num
    
def verify_level(dst_path, interpath, file_name, bd):
    level = int(bd//100000)
    downlink = 'downlink_' + str(level*100000)
    dst_levelpath = os.path.join(dst_path, downlink)
    dst_filepath = os.path.join(dst_levelpath, file_name)
    if not os.path.exists(dst_levelpath):
        os.makedirs(dst_levelpath)
    #if os.path.isfile(dst_filepath):
    #    os.remove(dst_filepath)
    shutil.move(interpath, dst_levelpath)

def countbd(readfile):
    fd = open(readfile, 'r');
    
    bandwidth = 0.0
    time1 = 0.0
    sum_b = 0.0
    for line in fd.readlines():
        info = line.split()
        if info[0] != '#':
            bandwidth_str = info[1]
            bandwidth = float(bandwidth_str)
            sum_b += bandwidth
            time1_str = info[0]
            time1 = float(time1_str)
    avgbd = sum_b/time1
    fd.close()

    return avgbd

def statistics(dst_path, levelnum):
    m = 0
    levelL = range(0, levelnum)
    for level in levelL:
        downlink = 'downlink_'+str(level*100000)
        for oklevel in os.listdir(dst_path):
            if oklevel == downlink:
                print oklevel,
                levelpath = os.path.join(dst_path, oklevel)
                n = 0
                for okfiles in os.listdir(levelpath):
                    okfilespath = os.path.join(levelpath, okfiles)
                    n += 1
                print ' %d' % n
                m += n
    oksum_num = m
    print ('sum filesnum = %d' % oksum_num)

def cutSession(runtime, datap, cuted_session):
    temp_train = os.path.join(cuted_session, 'train')
    temp_label = os.path.join(cuted_session, 'label')
    
    if not os.path.exists(temp_train):
        os.makedirs(temp_train)
    if not os.path.exists(temp_label):
        os.makedirs(temp_label)
    print temp_train
    print temp_label

    sum3600num = 0
    sumcutnum = 0
    
    for c in os.listdir(datap):       
        if c.endswith('oricuted'):
            sourceDir = os.path.join(datap, c) 
            print sourceDir
            for txt in os.listdir(sourceDir):
                filespath = os.path.join(sourceDir, txt)
                
                tL = []
                bL = []
                sum_b = 0.0
                end_time0 = 0.0
                num = 1
                for line in open(filespath):
                    tb = line.split()
                    if tb[0] != '#':
                        time_str = tb[0]
                        byte_str = tb[1]
                        time = float(time_str)
                        byte = float(byte_str)
                        sum_b += byte
                        if byte != 0.0:
                            end_time0 = time
                        
                        if time <= runtime*num:
                            tL.append(time)
                            bL.append(byte)
                                
                        elif bL[0] != 0.0 and bL[-1] != 0.0:
                            
                            file_name = txt.split('.txt')[0] + '_' + str(num) + '.txt'
                            
                            #put in train-set
                            if time <= 3*24*3600.0:
                                interpath = os.path.join(temp_train, file_name)
                            #put in label-set
                            else:
                                interpath = os.path.join(temp_label, file_name)
                            
                            with open(interpath, 'a') as inter:
                                for i in range(len(tL)):
                                    inter.write('%.2f %.2f\n'% (tL[i]-runtime*(num-1), bL[i]))
                            
                            bd = sum_b/(time-runtime*(num-1))

                            tL = []
                            bL = []
                            tL.append(time)
                            bL.append(byte)
                            sum_b = 0.0 
                            num += 1
                            sumcutnum += 1
                        else:
                            print '%d start%.2f end%.2f' % (num, bL[0], bL[-1])
                            tL = []
                            bL = []
                            sum_b = 0.0 
                            num += 1
                    #if sumcutnum > 8176:
                    #    break
                sum3600num += 1
                print ' %d' % (num-1)
    print 'complete file num = %d' % sum3600num
    print 'cut file num = %d' % sumcutnum
    print 'cut is done!'
   
def getFirst(providerp, firstp, cut_ftime):
    print providerp
    cuted = os.path.join(firstp, 'oricuted')
    
    if not os.path.exists(cuted):
        os.makedirs(cuted)
    print cuted
    #for item in os.listdir(providerp):
        #if item.endswith('origin'):
            #origin = os.path.join(providerp, item)
    for ori in os.listdir(providerp):
        if ori.endswith('readyCut'):
            ready_cut = os.path.join(providerp, ori)
            for f in os.listdir(ready_cut):
                orifile = os.path.join(ready_cut, f)
                print orifile,
                        
                cuted_file = os.path.join(cuted, 'first'+str(cut_ftime) + 'h-' + f)
                        
                fd = open(orifile, 'r')
                fa = open(cuted_file, 'a')
                for line in fd.readlines():
                    tb = line.split()
                    time = float(tb[0])
                    if time < cut_ftime*3600.0:
                        fa.write('%s' % line)
                    else:
                        break
                fa.close()
                fd.close()
                print ' aleady cut first %dh' % cut_ftime

def divideLevel(sto_dirp, double_nolevel):
    unitLevel = 131072
    
    for aset in os.listdir(double_nolevel):
        if aset.endswith('label'):
            print 'This is %s, please wait patiently!' % aset
            fileL = []
            bdL = []
            nolevel_train = os.path.join(double_nolevel, aset)

            for filen in os.listdir(nolevel_train):
                #print filen,
                filep = os.path.join(nolevel_train, filen)
                bd = countbd(filep)
                fileL.append(filep)
                bdL.append(bd)
            levelnum = int(max(bdL)/unitLevel)

            #div_set = sto_dirp.split('/')[-1]+'-30s-'+str(levelnum)+'level-'+ aset
            div_set = sto_dirp.split('/')[-1]+'-30s-label-doubleline'
            print div_set
            print 'maxbd = %.2fbyte/s (%.2fMbps)' % (max(bdL), max(bdL)*8/1024/1024)
            print 'unit of level = %.2fbyte/s (%.2fMbps)' % (unitLevel, unitLevel*8.0/1024.0/1024.0)
        
            divp = os.path.join(sto_dirp, div_set)
            for i in range(len(bdL)):
                level = bdL[i]//unitLevel
                if level > levelnum - 1:
                    level = levelnum - 1
                downlink = 'downlink_'+str(int(level*100000))
                dividep = os.path.join(divp, downlink)
                if not os.path.exists(dividep):
                    os.makedirs(dividep)
                divideFp = os.path.join(dividep, fileL[i].split('/')[-1]) 
                if aset == 'train':
                    shutil.copyfile(fileL[i], divideFp)
                else:
                    #double_to_single(fileL[i], divideFp)
                    shutil.copyfile(fileL[i], divideFp)
    
        statistics(divp, levelnum) 

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

if __name__ == '__main__':
    origin = '/home/wanwenkai/origin-trace'
    root = '/home/wanwenkai/sourceData'
    provider = 'TCP-3G'
    cut_ftime = 84  #h
    
    ori_pro = os.path.join(origin, provider)
    
    sto_p = os.path.join(root, provider)
    sto_dir = 'first' + str(cut_ftime) + 'h'
    sto_dirp = os.path.join(sto_p, sto_dir)
    
    session = 30   #s
    cuted_session = 'first'+str(cut_ftime)+'h-'+str(session)+'s-nolevel-doubleline'
    cuted_sessionp = os.path.join(sto_dirp, cuted_session)
   
    #please separate run the function as following
    #getFirst(ori_pro, sto_dirp, cut_ftime)
    cutSession(session, sto_dirp, cuted_sessionp)
    #divideLevel(sto_dirp, cuted_sessionp)
    #double_to_single(transfiles_path, dst_label_filespath):
