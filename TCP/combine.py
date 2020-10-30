import os
import shutil
import glob

def main():
    tcp_3G = '/home/wanwenkai/sourceData/TCP-3G/first84h/'
    tcp_4G = '/home/wanwenkai/sourceData/TCP-4G/first84h/'
    tcp = '/home/wanwenkai/sourceData/TCP/first84h/'

    tcp_3G_train = os.path.join(tcp_3G, 'first84h-30s-8level-train')
    tcp_3G_label = os.path.join(tcp_3G, 'first84h-30s-6level-label')
    tcp_4G_train = os.path.join(tcp_4G, 'first84h-30s-80level-train')
    tcp_4G_label = os.path.join(tcp_4G, 'first84h-30s-36level-label')
    
    tcpL = []
    tcpL.append(tcp_3G_train)
    tcpL.append(tcp_3G_label)
    tcpL.append(tcp_4G_train)
    tcpL.append(tcp_4G_label)

    tcp_trainn = 'first84h-30s-80level-train'
    tcp_labeln = 'first84h-30s-36level-label'
    tcp_train = os.path.join(tcp, tcp_trainn)
    tcp_label = os.path.join(tcp, tcp_labeln)
    '''
    for tcpset in tcpL:
        if tcpset.endswith('train'):        
            for downlink in os.listdir(tcpset):
                dp = os.path.join(tcpset, downlink)
                dstdp = os.path.join(tcp_train, downlink)
                if not os.path.exists(dstdp):
                    os.makedirs(dstdp)
                for txt in os.listdir(dp):
                    filep = os.path.join(dp, txt)
                    dstfilep = os.path.join(dstdp, txt)
                    shutil.copyfile(filep, dstfilep)
        if tcpset.endswith('label'):
            for downlink in os.listdir(tcpset):
                dp = os.path.join(tcpset, downlink)
                dstdp = os.path.join(tcp_label, downlink)
                if not os.path.exists(dstdp):
                    os.makedirs(dstdp)
                for txt in os.listdir(dp):
                    filep = os.path.join(dp, txt)
                    dstfilep = os.path.join(dstdp, txt)
                    shutil.copyfile(filep, dstfilep)
    ''' 
    statistics(tcp_train, 80)
    statistics(tcp_label, 36)
    
    #allfileL = glob.glob(tcp + '*.txt')
    #print len(allfileL)

def statistics(path, level_num):
    print path.split('/')[-1]
    
    dL = range(level_num)
    #print dL
    sum_files = 0
    for d in dL:
        downlink = 'downlink_' + str(d*100000)
        downlinkdir = os.path.join(path, downlink)
        allfileL = glob.glob(downlinkdir + '/*.txt')
        if len(allfileL) != 0:
            print downlink,
            print ' %d' % len(allfileL)
        sum_files += len(allfileL)
    print 'sum files = %d' % sum_files

if __name__ == '__main__':
    #combine TCP-3G and TCP-4G
    main()

