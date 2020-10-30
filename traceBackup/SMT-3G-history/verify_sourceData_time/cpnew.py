import os
import shutil

txt = '/home/wanwenkai/sourceData/verify_sourceData_time/bd.txt'
dstp = '/home/wanwenkai/sourceData/verify_sourceData_new/'
soup = '/home/wanwenkai/sourceData/verify_sourceData_time/'
fd = open(txt, 'r')
for line in fd.readlines():
    nb = line.split()
    name = nb[0]
    bd = float(nb[1])
    sou = os.path.join(soup, name)
    if bd <= 100000:
        d = 'downlink_0/' + name
    elif bd <= 200000:
        d = 'downlink_100000/' + name
    elif bd <= 300000:
        d = 'downlink_200000/' + name
    elif bd <= 400000:
        d = 'downlink_300000/' + name
    elif bd <= 500000:
        d = 'downlink_400000/' + name
    elif bd <= 600000:
        d = 'downlink_500000/' + name
    elif bd <= 700000:
        d = 'downlink_600000/' + name
    elif bd <= 800000:
        d = 'downlink_700000/' + name
    elif bd <= 900000:
        d = 'downlink_800000/' + name
    elif bd <= 1000000:
        d = 'downlink_900000/' + name
    else:
        d = 'downlink_1000000/' + name

    
    dst = os.path.join(dstp, d)
    print dst
    shutil.copy(sou, dst)



