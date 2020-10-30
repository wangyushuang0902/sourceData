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

def cut(runtime, datap, temp):
    if not os.path.exists(temp):
        os.makedirs(temp)
    sum3600num = 0
    sumcutnum = 0
    #for transport in os.listdir(datap):       
        #if not transport.endswith('.py'):
            #print transport
            #transportp = os.path.join(datap, transport) 
    for txt in os.listdir(datap):
        if txt.endswith('.txt'):
            print txt,
            filespath = os.path.join(datap, txt)
            tL = []
            bL = []
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
                        tL.append(time)
                        bL.append(byte)
                    elif len(tL)!=0 and len(tL)>runtime*5:
                        file_name = txt.split('.txt')[0] + '_' + str(num) + '.txt'
                        interpath = os.path.join(temp, file_name)
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
                        tL = []
                        bL = []
                        sum_b = 0.0 
                        num += 1
            sum3600num += 1
            print ' %d' % (num-1)
    print 'complete file num = %d' % sum3600num
    print 'cut file num = %d' % sumcutnum
    print 'cut is done!'
   
def getFirst24h(datap, first24hp):
    if not os.path.exists(first24hp):
        os.makedirs(first24hp)
    
    for filen in os.listdir(datap):
        print filen
        filep = os.path.join(datap, filen)
        file24p = os.path.join(first24hp, 'first6h-'+filen)
        fd = open(filep, 'r')
        fa = open(file24p, 'a')
        for line in fd.readlines():
            tb = line.split()
            time = float(tb[0])
            if time < 6*3600.0:
                fa.write('%s' % line)
            else:
                break
        fa.close()

def divideLevel(doublelineSource):
    #levelnum = 11
    fileL = []
    bdL = []
    for filen in os.listdir(doublelineSource):
        #print filen,
        filep = os.path.join(doublelineSource, filen)
        bd = countbd(filep)
        fileL.append(filep)
        bdL.append(bd)
    print 'maxbd = %.2fbyte/s (%.2fMbps)' % (max(bdL), max(bdL)*8/1024/1024)
    #unitLevel = int(max(bdL)/levelnum)
    unitLevel = 131072
    levelnum = int(max(bdL)/unitLevel)
    print 'unit of level = %.2fbyte/s (%.2fMbps)' % (unitLevel, unitLevel*8.0/1024.0/1024.0)

    currentPath = os.getcwd()
    divp = os.path.join(currentPath, '2.85h-30s-doubleline-'+str(levelnum)+'level')
    for i in range(len(bdL)):
        level = bdL[i]//unitLevel
        if level > levelnum - 1:
            level = levelnum - 1
        downlink = 'downlink_'+str(int(level*100000))
        dividep = os.path.join(divp, downlink)
        if not os.path.exists(dividep):
            os.makedirs(dividep)
        divideFp = os.path.join(dividep, fileL[i].split('/')[-1]) 
        shutil.copyfile(fileL[i], divideFp)
    statistics(divp, levelnum) 

if __name__ == '__main__':
    #datap = '/home/wanwenkai/sourceData/TCP-3G/original-doubleline/' 
    first24hp = '/home/wanwenkai/sourceData/Mahimahi/original-trace-doubleline/'
    temp = '/home/wanwenkai/sourceData/Mahimahi/2.85h-30s-doubleline-nolevel/'
    #please separate run the function as following
    #getFirst24h(datap, first24hp)
    #cut(30, first24hp, temp)
    divideLevel(temp)
