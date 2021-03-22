import os
import numpy as np
import cut
import doubleToSingle

def cutSession(cut_dl, origin, provider, duration, session):
    print 'Begin slicing every %ds!' % session

    originp = os.path.join(origin, provider)
    
    allbdL = []
    if provider == 'SMT-3G':
        if not isinstance(duration, int):
            print 'error:the duration of SMT-3G must be int!'

        origindl = os.path.join(originp, 'original-doubleline')
        
        hourtxt = os.path.join(originp, '122h.txt')
        hourList = open(hourtxt, 'r')
        hnum = 0
        for line in hourList.readlines():
            if hnum >= duration:
                break
            info = line.split()
            name = info[0]
            #seq = int(name.split('_')[-1])
            for fil in os.listdir(origindl):
                if fil == name:
                    print '%d %s' % (hnum, fil)
                    origindlf = os.path.join(origindl, fil)
                    
                    cut_dl_h = os.path.join(cut_dl, str(hnum))
                    if not os.path.exists(cut_dl_h):
                        os.makedirs(cut_dl_h)
                    bdL = cut.cutLabel(origindlf, session, cut_dl_h)
    
            hnum += 1
    
    elif provider == 'Mahimahi':
        origindl = os.path.join(originp, 'original-doubleline')
        for fil in os.listdir(origindl):
            if fil.endswith('txt'):
                ori_dl_f = os.path.join(origindl, fil)
                bdL = cut.cutLabel(ori_dl_f, session, cut_dl)
   
    elif provider == 'HSDPA-3G':
        origin_dl = os.path.join(originp, 'original-doubleline')
        for trans in os.listdir(origin_dl):
            print '%s ' % trans,
            origin_dl_tr = os.path.join(origin_dl, trans)
            cut_dl_tr = os.path.join(cut_dl, trans)
            if not os.path.exists(cut_dl_tr):
                os.makedirs(cut_dl_tr)

            for fil in os.listdir(origin_dl_tr):
                ori_dl_tr_f = os.path.join(origin_dl_tr, fil)
                bdL = cut.cutLabel(ori_dl_tr_f, session, cut_dl_tr)
                allbdL.extend(bdL)
        print 'sumnum=%d max=%.2f avg=%.2f var=%.2f' % (len(allbdL),\
                max(allbdL), np.mean(allbdL), np.var(allbdL))

    else:
        print 'error:no this provider!'


def double_to_single(cut_dl, provider, druation):
    print 'Begin double to single!'
    cut_sl = os.path.join(cut_dl.split('double')[0], 'label')
    if not os.path.exists(cut_sl):
        os.makedirs(cut_sl)
     
    if provider == 'SMT-3G':
        hL = range(duration)
        for h in hL:
            cut_dl_h = os.path.join(cut_dl, str(h))
            cut_sl_h = os.path.join(cut_sl, str(h))
            print h
            if not os.path.exists(cut_sl_h):
                os.makedirs(cut_sl_h)

            for fil in os.listdir(cut_dl_h):
                double_f = os.path.join(cut_dl_h, fil)
                single_f = os.path.join(cut_sl_h, fil)
                doubleToSingle.doubleToSingle(double_f, single_f) 
    
    elif provider == 'Mahimahi':
        for fil in os.listdir(cut_dl):
            double_f = os.path.join(cut_dl, fil)
            single_f = os.path.join(cut_sl, fil)
            doubleToSingle.doubleToSingle(double_f, single_f) 
    
    elif provider == 'HSDPA-3G':
        #hL = range(duration)
        for tran in os.listdir(cut_dl):
            cut_dl_tr = os.path.join(cut_dl, tran)
            cut_sl_tr = os.path.join(cut_sl, tran)
            print tran
            if not os.path.exists(cut_sl_tr):
                os.makedirs(cut_sl_tr)

            for fil in os.listdir(cut_dl_tr):
                double_f = os.path.join(cut_dl_tr, fil)
                single_f = os.path.join(cut_sl_tr, fil)
                doubleToSingle.doubleToSingle(double_f, single_f) 
    else:
        print 'error:no this provider!'

if __name__ == '__main__':
    origin = '/home/wanwenkai/origin-trace'
    root = '/home/wanwenkai/sourceData'
    
    provider = 'HSDPA-3G'
    duration = 'all'    #int h or str all
    session = 30    #s
    
    cut_dl = os.path.join(root, provider, 'first'+str(duration)+'h',str(session)+'s', 'doubleline')
    if not os.path.exists(cut_dl):
        os.makedirs(cut_dl)
    
    cutSession(cut_dl, origin, provider, duration, session)
    double_to_single(cut_dl, provider, duration)
