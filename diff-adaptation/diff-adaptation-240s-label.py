import os

def main():
    txt240s = 'diff-adaptation-level4-1.txt'
    
    txt30s_dir = '/home/wanwenkai/sourceData/TCP-3G/first84h/30s/first84h-30s-6level-label'

    txtL = ['downlink_100000/first84h-NewFile-HighDensity-CUHK-ms_9709.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_9501.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_10000.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_9000.txt',\
            'downlink_200000/first84h-NewFile-HighDensity-CUHK-ms_9726.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_10002.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_9001.txt',\
            'downlink_500000/first84h-NewFile-HighDensity-CUHK-ms_9502.txt']
    
    for t in range(len(txtL)):
        txt30sp = os.path.join(txt30s_dir, txtL[t])
        
        fd = open(txt30sp, 'r')
        for line in fd.readlines():
            time = int(line) + 30000*t 
            with open(txt240s, 'a') as tf:
                tf.write('%d\n' % time)
        fd.close()

if __name__ == '__main__':
    main()
