
#!/usr/bin/python

__author__ = 'Javier Lopez Punzano'

import subprocess, sys
from math import sqrt


thres = []
impostors_scr = []
clients_scr = []
ROC = []

def readImpostors(file):
    impostors = 0
    for line in open(file):
        columns = line.split()
        thres.append(columns[1])
        impostors_scr.append(columns[1])
        impostors += 1
    print "Numero de impostores: " , impostors
    return impostors

def readClients(file):
    clients = 0
    for line in open(file):
        columns = line.split()
        thres.append(columns[1])
        clients_scr.append(columns[1])
        clients += 1
    print "Numero de clientes: " , clients
    return clients


def getRocPoints():
    for thr in thres:
        vp, vn, fn, fp = 0, 0, 0, 0
        for clscor in clients_scr:
            if clscor > thr:
                vp += 1
            else:
                fn += 1
        for impscor in impostors_scr:
            if impscor > thr:
                fp += 1
            else:
                vn += 1
        s = float( vp / float(vp + fn))
        e = float(vn /  float(vn + fp))
        ROC.append([1 - e, s])


def getDprime():
    impmean, impvar = meanvar(impostors_scr)
    clmean, clvar = meanvar(clients_scr)
    dprime = (clmean - impmean)/sqrt(clvar + impvar)
    print "D-prime value : ", dprime
    return dprime

def meanvar(x):
    n, mean, var = len(x), 0, 0
    for a in x:
        mean = float(mean) + float(a)
    mean = mean / float(n)
    for a in x:
        var = var + (float(a) - float(mean))**2
    var = var / float(n)
    return mean, var

def trapezoidalAUC():
    auc = 0
    for i in range(len(ROC)-1):
        auc = auc + 0.5 * ((1.0 - ROC[i][0]) + (1.0-ROC[i+1][0])) * (ROC[i+1][1] - ROC[i][1])
    auc *= -100
    print "Area Under the Curve : " , auc
    return auc

def usage():
    print "Usage: <Roc.py> <clients_file> <impostors_file>"
    exit(1)


def printCurve():
    saveout = sys.stdout
    f = open('curvepoints.dat', 'w')
    sys.stdout = f
    for point in ROC:
        print point[0], point[1]
    sys.stdout.flush()
    sys.stdout = saveout
    f.close()

    gnuplot = subprocess.Popen(['gnuplot' ],shell=True,stdin=subprocess.PIPE,)
    gnuplot.stdin.write('set term png; ')
    gnuplot.stdin.write('set out \'ROC.png\' \n')
    gnuplot.stdin.write('set grid \n')
    gnuplot.stdin.write('set multiplot \n ')
    gnuplot.stdin.write('set xrange [0:1] \n ')
    gnuplot.stdin.write('set yrange [0:1] \n')
    gnuplot.stdin.write('set xlabel "FPR (1 - Esp) \n')
    gnuplot.stdin.write('set ylabel "TPR (Sen) \n')
    gnuplot.stdin.write('set style line 1 lc 4 lt 4 lw 0.1 ps 0.1 ; \n')
    gnuplot.stdin.write('set x2label  \"AUC: %s\"  \n' % (trapezoidalAUC()))
    gnuplot.stdin.write('set key outside  top center title \"D-prime: %s\ ";  \n ' % (getDprime()))
    gnuplot.stdin.write('show label\n')
    gnuplot.stdin.write('plot \'curvepoints.dat\' u 1:2 w lp ls 1 notitle "ROC Curve" \n') 
    gnuplot.stdin.flush()
 


if __name__ == '__main__':
    
    if len(sys.argv) < 3 or len(sys.argv) > 3  :
        usage()
    nclients =  readClients(sys.argv[1])
    nimpostors = readImpostors(sys.argv[2])
    #Lista con todos los umbrales ordenados y sin repetir
    thres = sorted(list(set(thres)))
    getRocPoints()
    printCurve()
    exit(0)



