import math
import matplotlib.pyplot as plt
import pylab
import os
import numpy as np
telemetry = open('telemetry.txt', 'w')
telemetry.write('T, R, w, alfa, M, Fvert, Fhor , Vvert, Vhor, av, ah\n')
telemetry.close()

joka = open('1-2.txt', 'w')
joka.close()
def save(name='', fmt='png'):
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(fmt)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)
def m(module):
    if (module == 'RN_1'):
        return mRN_1 + ms1
    if (module == 'RN_2'):
        return mRN_2 + ms2
    if (module == 'RN_3'):
        return mRN_3
    if (module == 'LK'):
        return mLK
    if (module == 'LM'):
        return mLM
x=[]
y=[]
a=[]
i = 0
def angle(alfa, R, Vv, Vh, T, Fdv, Fcb, Ft, av, ah, M, Fhor):
    H = R / 1000 - 6375
    dm=0
    if(T>151):
        dm=1238.5
    if H > 20 and H < 60:
        if(alfa<math.pi/3):
           return dh
        else:
            return 0
    else:
        if H>80 and alfa!=0:
            t1 = (M/dm)*(1-math.exp(-(dm*Vh/(Fdv*math.sin(alfa)))))
            t2 = tpad(R, Vv, Vh, Fdv, dm, alfa, M)
            if(t1>t2):
                return -dh
            else:
                if t1!=t2:
                    return dh
                else:
                    return 0
        else:
            return  dh/10



def tpad(R, Vv, Vh, Fdv, dm, alfa, M):
    r = R
    t2 = 0
    v = Vv
    v2 = Vh
    while v > 0:
        m = M - dm * t2
        Fv = Fdv * math.cos(alfa) + m * math.pow(Vh / r, 2) * (r) - GM * m / (math.pow(r, 2))
        Fh = Fdv * math.sin(alfa)
        avert = Fv / m
        ahor = Fh / m
        r += v * 1 + avert / 2
        v += avert
        v2 += ahor
        t2 += 1
    return t2


def ro(H):
    if (H <= 70):
        if (H < 5):
            return 0.001225
        if (5 < H < 10):
            return 0.007421
        if (10 < H < 15):
            return 0.0004176
        if (15 < H < 20):
            return 0.0001916
        if (20 < H < 25):
            return 0.00008801
        if (25 < H < 30):
            return 0.0000405
        if (30 < H < 35):
            return 0.000018
        if (35 < H < 40):
            return 0.00000839
        if (40 < H < 45):
            return 0.000004
        if (45 < H < 50):
            return 0.000002
        if (50 < H < 55):
            return 0.000001
        if (55 < H < 60):
            return 0.000000565
        if (60 < H < 65):
            return 0.0000003095
        if (65 < H < 70):
            return 0.0000001
        if (70 < H < 75):
            return 0.000000084
    else:
        return 0


ms1 = 135000
ms2 = 37600
mRN_1 = 2145000 - ms1  # массы частей корабля
mRN_2 = 458700 - ms2
mRN_3 = 120000
mLK = 5500 + 22500
mLM = 15000

Rocket = ['RN_1', 'RN_2', 'RN_3', 'LK', 'LM']
M = m('RN_1') + m('RN_2') + m('RN_3') + m('LK') + m('LM')
print(M, ' ', M-mRN_1-ms1)
GM = 9.81 * (math.pow(6375000, 2))
R = 6375000
w = 0

Vh = 403
Vv = 0
alfa = 0
T = 0
av = 0
ah = 0
dh: float = (math.pi / 180)
Ft = GM * M / (math.pow(R, 2))
Fcb = M * math.pow(Vh / R, 2) * (R)
Fcopr = 0.0
x11111= True
x22222 = True
x33333 = True
plot = open('plot.txt', 'w')
plot.close()
v=[]
h=[]
t=[]
while R <= (6375 + 1000) * 1000 and w <= math.sqrt(GM / ((6375 + 185) * 1000)):
    T = T + 1
    telemetry = open('telemetry.txt', 'a')
    Fdv = 0
    plot = open('plot.txt', 'a')
    if mRN_1 > 0: #рассчет тяги
        Fdv = 34350000
        mRN_1 = mRN_1 - 34350000 / 2580
        M = m('RN_1') + m('RN_2') + m('RN_3') + m('LK') + m('LM')
    else:
        ms1 = 0
        mRN_1 = 0
        if x11111:
            telemetry.write("\n Сброс первой разгонной ступени \n ")
            x11111 = False
        Rocket = Rocket[1:4]
        M = m('RN_1') + m('RN_2') + m('RN_3') + m('LK') + m('LM')
        if(mRN_2 >= 0 and x22222):
            Fdv=6645000
            mRN_2 = mRN_2-1238.5
        else:
            Fdv=0
            mRN_2=0
            if  x22222:
                telemetry.write("\n Сброс Второй разгонной ступени \n ")
                x22222 = False
            Rocket = Rocket[1:3]

    if Vh >= math.sqrt(GM/R):
        Fdv=0
        telemetry.write('\n корабль на орбите\n')
        break
    if R/1000 - 6375 < 0:
        telemetry.write('корабль упал \n')
        break
    mRN_1i = mRN_1
    wi = w
    Ri = R
    alfai = alfa
    Vvi = Vv
    Vhi = Vh
    Fcb = M * math.pow(Vh , 2) / (R)
    Ft = GM * M / (math.pow(R, 2))
    Fvert = Fcb + Fdv * math.cos(alfa) - Ft - math.pow(10.1 / 2, 2) * 0.1 * ro(R / 1000 - 6375) / 2 * math.cos(alfa)
    Fhor = Fdv * math.sin(alfa) - math.pow(10.1 / 2, 2) * 0.1 * ro(R / 1000 - 6375) / 2 * math.sin(alfa)
    av = Fvert / M
    ah = Fhor / M
    Vh = Vhi + 1*ah * 1
    Vv = Vvi + av * 1
    R = Ri + av * 1 * 1 / 2 + Vvi * 1
    w = wi + (Vh - 403) / R + ah * 1 * 1 / (2 * R)
    s1 = ''
    s1 = str(T) + '    H=' + str(R / 1000 - 6375) + "   w=" + str(w) + '  alfa=' + str(round(alfa/(math.pi / 180))) + '   M=' + str(
        M) + '     Fv=' + str(Fvert) + '   Fh=' + str(Fhor) + '   Vv=' + str(Vv) + '   Vh=' + str(Vh) + '  av=' + str(
        av) + '     ah=' + str(ah) + '  Fcb=' + str(Fcb) + "  Ft=" + str(Ft) + '  Fdv=' + str(Fdv * math.cos(alfa)) + '\n'
    plot.write(str(T) + ' ' + str(R / 1000 - 6375) +'\n')
    x.append(R*math.cos(w)/1000)
    y.append(R*math.sin(w)/1000)
    v.append(Vv)
    t.append(T)
    h.append(R / 1000 - 6375)
    a.append(round(alfa/(math.pi / 180)))
    telemetry.write(s1)
    telemetry.close()
    alfa = alfa + angle(alfa, R, Vv, Vh, T, Fdv, Fcb, Ft, av, ah, M, Fhor)
M = m('RN_3') + m('LK') + m('LM')

joka = open('1-2.txt', 'w')
joka.write(str(M)+' '+str(R/1000-6375))
plot.close()

stromn1 = open('plot.txt', 'r')
s = stromn1.read()
mv1 = s.split('\n')
x1=[]
y1=[]
for i in range(0, 360):
    x1.append(6350*math.sin(i/180*math.pi))
    y1.append(6350 * math.cos(i/180*math.pi))
for i in range(0, 360):
    x.append(R*math.cos(w+i/180*math.pi)/1000)
    y.append(R* math.sin(w+i/180*math.pi)/1000)
for i in range(0, len(mv1)):
    mv1[i].split(' ')
fig = plt.figure(figsize=(9, 10))
plt.ylabel(u'Y, км ')
plt.xlabel(u'Х, км')
plt.title('trajectory')
g1 = plt.plot(x, y)
g2 = plt.plot(x1, y1)
plt.grid(True)
g3 = g1 + g2
plt.savefig(fname = 'trajectory', fmt='png')
plt.show(g1+g2)
plt.autoscale
plt.grid(True)
plt.title('h(t)')
plt.ylabel(u'Высота, км ')
plt.xlabel(u'Время, сек')
g1 = plt.plot(t, h)
plt.savefig(fname = 'h(t)', fmt='png')
plt.show()
plt.title('v(t)')
plt.ylabel(u'Вертикальная скорость, м/с ')
plt.xlabel(u'Время, с')
plt.grid(True)
g1 = plt.plot(t, v)
plt.savefig(fname = 'v(t)', fmt='png')
plt.show()
plt.title('alfa(t)')
plt.ylabel(u'Угол, градусы ')
plt.xlabel(u'Время, с')
plt.grid(True)
g1 = plt.plot(t, a)
plt.savefig(fname = 'alfa(t)', fmt='png')
plt.show()

joka.close()
telemetry.write(str(mRN_2)+'\n')
print(GM)
