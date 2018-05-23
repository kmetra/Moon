import math

telemetry = open('telemetry.txt', 'w')
telemetry.write('T, R, w, alfa, M, Fvert, Fhor , Vvert, Vhor, av, ah\n')
telemetry.close()


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
def angle(alfa, R, Vv, Vh, T, Fdv, Fcb, Ft):
    if R / 1000 - 6375 > 60 :
        if(Fdv*math.cos(alfa)+Fcb-Ft>0):
            if(alfa/(math.pi/180)<45):
                return  dh


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
mLM = 150000

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
dh = (math.pi / 180)
Ft = GM * M / (math.pow(R, 2))
Fcb = M * math.pow(Vh / R, 2) * (R)
Fcopr = 0.0
x11111= True
x22222 = True
x33333 = True
while R <= (6375 + 1000) * 1000 and w <= math.sqrt(GM / ((6375 + 185) * 1000)):
    T = T + 1
    telemetry = open('telemetry.txt', 'a')
    Fdv = 0
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
            Fdv=5115000
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
    Vh = Vhi + ah * 1
    Vv = Vvi + av * 1
    R = Ri + av * 1 * 1 / 2 + Vvi * 1
    w = wi + Vh / R + ah * 1 * 1 / (2 * R)
    s1 = ''
    s1 = str(T) + '    H=' + str(R / 1000 - 6375) + "   w=" + str(w) + '  alfa=' + str(round(alfa/(math.pi / 180))) + '   M=' + str(
        M) + '     Fv=' + str(Fvert) + '   Fh=' + str(Fhor) + '   Vv=' + str(Vv) + '   Vh=' + str(Vh) + '  av=' + str(
        av) + '     ah=' + str(ah) + '  Fcb=' + str(Fcb) + "  Ft=" + str(Ft) + '  Fdv=' + str(Fdv * math.cos(alfa)) + '\n'
    telemetry.write(s1)
    telemetry.close()
    alfa = alfa + angle(alfa, R, Vv, Vh, T, Fdv, Fcb, Ft)

telemetry.write(str(mRN_2)+'\n')
print(GM)
