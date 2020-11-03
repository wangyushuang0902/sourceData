import os

def main():
    path = '/home/wanwenkai/sourceData/TCP/first84h/first84h-30s-80level-train'
    print 'train bandwidth 0'
    sumi = 0
    sum0 = 0
    sum0end = 0
    dL = range(80)
    for d in dL:
        down = 'downlink_' + str(d*100000)
        j = 0 
        k = 0
        dfile = 0
        downlink = os.path.join(path, down)
        if os.path.exists(downlink):
            print down,
            for f in os.listdir(downlink):
                filep = os.path.join(downlink, f)
                find = 0
                end_zero = 0.0
                for line in open(filep):
                    info = line.split()
                    time = float(info[0])
                    byte = float(info[1])
                    if byte == 0.0:
                        find = 1
                    else:
                        end_zero = time
                dfile += 1
                if find == 1:
                    j += 1
                if end_zero <= 29.9:
                    k += 1
            print ' %d' % dfile,
            if j != 0: 
                print '  %d  %.2f    %d  %.2f' % (j, round(j*1.0/dfile, 2), k, round(k*1.0/j, 2))
            else:
                print '  %d  %.2f    %d  0.0' % (j, round(j*1.0/dfile, 2), k)
        
        sumi += dfile
        sum0 += j
        sum0end += k
    print 'sum = %d' % sumi
    print 'sum0 = %d ratio = %.2f' % (sum0, round(sum0*1.0/sumi, 2))
    print 'sum0end = %d ratio = %.2f' % (sum0end, round(sum0end*1.0/sum0, 2))


if __name__ == '__main__':
    main()

