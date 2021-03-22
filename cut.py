import os
import numpy as np

def cutLabel(ori_dl_f, runtime, cut_dl_h):
    tL = []
    bL = []
    sum_b = 0.0
    num = 1
    bdL = []
    for line in open(ori_dl_f):
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
                                
            else:   
                txt = ori_dl_f.split('/')[-1]
                file_name = txt.split('.txt')[0] + '_' + str(num) + '.txt'
                #print file_name            
                #if time <= 3*24*3600.0:
                    #interpath = os.path.join(temp_train, file_name)
                interpath = os.path.join(cut_dl_h, file_name)
                            
                with open(interpath, 'a') as inter:
                    for i in range(len(tL)):
                        inter.write('%.2f %.2f\n'% (tL[i]-runtime*(num-1), bL[i]))
                            
                bd = round((sum_b/(time-runtime*(num-1)))*8/1024/1024, 2)
                bdL.append(bd)

                tL.append(time)
                bL.append(byte)
                
                tL = []
                bL = []
                sum_b = 0.0 
                num += 1
                
    return bdL

