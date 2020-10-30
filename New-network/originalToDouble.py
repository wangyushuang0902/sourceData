import os
import shutil

def main(root, datap):
    doubledir = 'original-doubleline'
    doublep = os.path.join(root, doubledir)
    if os.path.exists(doublep):
        shutil.rmtree(doublep)
    
    for style in os.listdir(datap):
        if not style.endswith('.md'):
            print style
            stylep = os.path.join(datap, style)
            double_trans = os.path.join(doublep, style) 
            if not os.path.exists(double_trans):
                os.makedirs(double_trans)
            #j = 0
            for filen in os.listdir(stylep):
                #if j > 0:
                #    break
                print filen
                filep = os.path.join(stylep, filen)
                double_filep = os.path.join(double_trans, filen+'.txt')
                fd = open(filep, 'r')
                ad = open(double_filep, 'a')
                #ts = 0.0
                sum_b = 0.0
                for line in fd.readlines():
                    info = line.split()
                    ts = float(info[0])
                    b = round(float(info[1]), 2)*1024.0*1024.0/8.0
                    sum_b += b
                    for k in range(5):  
                        ts += 0.1
                        ad.write('%.2f %.1f\n' % (ts, b/5.0))
                bd = sum_b/ts
                ad.write('# avarage throughput = %.2fbyte/s (%.2fMbps)' % (bd, bd*8.0/1024.0/1024.0))
                ad.close()
                fd.close()
                #j += 1

if __name__ == "__main__":
    root = '/home/wanwenkai/sourceData/New-Network/'
    datap = os.path.join(root, 'New-Network-original')
    main(root, datap)
