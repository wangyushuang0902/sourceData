import os
import shutil

def main(root, datap):
    doubledir = 'original-doubleline'
    doublep = os.path.join(root, doubledir)
    if os.path.exists(doublep):
        shutil.rmtree(doublep)
    
    for transport in os.listdir(datap):
        if not transport.endswith('.md'):
            transportp = os.path.join(datap, transport)
            double_trans = os.path.join(doublep, transport) 
            if not os.path.exists(double_trans):
                os.makedirs(double_trans)
            #j = 0
            for filen in os.listdir(transportp):
                #if j > 0:
                #    break
                filep = os.path.join(transportp, filen)
                double_filep = os.path.join(double_trans, filen.split('.')[0]+'-'+filen.split('.')[1]+'.txt')
                fd = open(filep, 'r')
                ad = open(double_filep, 'a')
                ts = 0.0
                sum_b = 0.0
                for line in fd.readlines():
                    info = line.split()
                    delta_ts = float(info[-1])/1000.0
                    b = float(info[4])
                    sum_b += b
                    for k in range(10):  
                        ts += delta_ts/10.0
                        ad.write('%.2f %.1f\n' % (ts, b/10.0))
                bd = sum_b/ts
                ad.write('# avarage throughput = %.2fbyte/s (%.2fMbps)' % (bd, bd*8/1024/1024))
                ad.close()
                fd.close()
                #j += 1

if __name__ == "__main__":
    root = '/home/wanwenkai/sourceData/HSDPA-3G/'
    datap = os.path.join(root, 'HSDPA-3G-original')
    main(root, datap)
