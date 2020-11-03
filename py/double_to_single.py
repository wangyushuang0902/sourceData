
def doubleToSingle(transfiles_path, dst_label_filespath):
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
    print sum_b/time_new

if __name__ == '__main__':
    double = '/home/wanwenkai/sourceData/first84h-NewFile-HighDensity-4GMobile-ms_1897.txt'
    single = '/home/wanwenkai/sourceData/first84h-NewFile-HighDensity-4GMobile-ms_1897.trace'
    doubleToSingle(double, single)
