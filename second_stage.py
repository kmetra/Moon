import sys
import math

INPUT_FILE = 'toMoon.txt'
output = open('earthtomoon.txt', 'w')
output2 = open('coordinates.txt', 'w')
output3 = open('speed.txt' , 'w')
out = open('to 3.txt', 'w')
gEarth = 0.00981  # ускорение на Земле
gMoon = 0.00162  # ускорение на Луне
rEarth = 6375  # радиус Земли
rMoon = 1738  # радиус Луны
GM = gEarth * rEarth * rEarth
Gm = gMoon * rMoon * rMoon
R = 384405  # радиус лунной орбиты
pi = math.pi
Tmoon = 2 * pi * math.sqrt(R * R * R / GM)  # период обращения луны
mass = 5500 + 22500 + 15000  # масса КО+СМ+ЛМ
fuelMass = 17700  # масса топлива коррекция СМ
dryMass = 20000  # сухая масса выход на траекторию 3 ступень
F = 1016  # тяга двигателей 3 ступень
F2 = 95.75  # тяга двигателей СМ
u = 4.130  # скорость истечения 3 ступень
u2 = 3.050  # скорость истечения СМ
q = F / u  # потребление топлива 3 ступень ускорение
q2 = F2 / u2  # потребление топлива СМ замедление


# Начало координат в центре Земли, в нулевой момент времени ось х направлена на Луну,
# ось z направлена на северный полюс.
class Vector:  # класс операций кинематических величин
    def plus(a, b):
        ans = Vector()
        ans.x = a.x + b.x
        ans.y = a.y + b.y
        ans.z = a.z + b.z
        return ans

    def minus(a, b):
        ans = Vector()
        ans.x = a.x - b.x
        ans.y = a.y - b.y
        ans.z = a.z - b.z
        return ans

    def abs(a):
        return math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z)

    def mult(k, a):
        ans = Vector()
        ans.x = k * a.x
        ans.y = k * a.y
        ans.z = k * a.z
        return ans

    def angle(v, u):
        a = Vector.abs(v)
        b = Vector.abs(u)
        c = v.x * u.x + v.y * u.y + v.z * u.z
        return math.acos(c / a / b)

    def copy(a):
        ans = Vector()
        ans.x = a.x
        ans.y = a.y
        ans.z = a.z
        return ans


class RVTME:  # содержит текущую позицию, скорость, время общее массовое и булево состояние двигателя
    # (0 - off, q - ускорение, q2 - замедление)
    def copy(rvtme):
        ans = RVTME()
        ans.r = Vector.copy(rvtme.r)
        ans.v = Vector.copy(rvtme.v)
        ans.t = rvtme.t
        ans.m = rvtme.m
        ans.engine = rvtme.engine
        return ans


def moonPosition(time):  # положение Луны в данный момент времени(т.к. она обращается)
    global R, pi, Tmoon
    ans = Vector()
    ans.x = R * math.cos(2 * pi * time / Tmoon)
    ans.y = R * math.sin(2 * pi * time / Tmoon)
    ans.z = 0
    return ans


def moonV(time):  # скорость Луны в данный момент времени
    global Tmoon, pi, R
    ans = Vector()
    ans.x = -2 * pi * R / Tmoon * math.sin(2 * pi * time / Tmoon)
    ans.y = 2 * pi * R / Tmoon * math.cos(2 * pi * time / Tmoon)
    ans.z = 0
    return ans


def timestep(a):  # возвращает непостоянную промежуток времени, чтобы сделать нашу модель более точной
    return 0.00005 / Vector.abs(a)


def acc(r, v, time, mass, engine):  # возвращает ускорение устройства в данный момент времени в
    # зависимости от происходящего процесса: q - вывод на траекторию(ускорение) // q2 - коррекция(замедление)
    global GM, Gm, q, F, q2, F2
    aEarth = Vector.mult(-GM / (Vector.abs(r) * Vector.abs(r) * Vector.abs(r)), r)
    moon = Vector.minus(r, moonPosition(time))
    aMoon = Vector.mult(-Gm / (Vector.abs(moon) * Vector.abs(moon) * Vector.abs(moon)), moon)
    aEngine = Vector()
    if engine == 0:
        aEngine.x = 0
        aEngine.y = 0
        aEngine.z = 0
    if engine == q:
        aEngine = Vector.mult(F / mass / Vector.abs(v), v)
    if engine == q2:
        aEngine = Vector.mult(-F2 / mass / Vector.abs(v), v)
    return Vector.plus(aEngine, Vector.plus(aEarth, aMoon))


def nextRVTME(previous, timestep):
    # возвращает следующее значение положения и скорости устройства (методом Рунге-Кутты)
    ans = RVTME()
    kv1 = Vector.mult(timestep, acc(previous.r, previous.v, previous.t, previous.m, previous.engine))
    kr1 = Vector.mult(timestep, previous.v)
    kv2 = Vector.mult(timestep,
                      acc(Vector.plus(previous.r, Vector.mult(0.5, kv1)),
                          Vector.plus(previous.v, Vector.mult(0.5, kv1)),
                          previous.t + timestep / 2, previous.m - 0.5 * previous.engine * timestep, previous.engine))
    kr2 = Vector.mult(timestep, Vector.plus(previous.v, Vector.mult(0.5, kv1)))
    kv3 = Vector.mult(timestep,
                      acc(Vector.plus(previous.r, Vector.mult(0.5, kv2)),
                          Vector.plus(previous.v, Vector.mult(0.5, kv2)),
                          previous.t + timestep / 2, previous.m - 0.5 * previous.engine * timestep, previous.engine))
    kr3 = Vector.mult(timestep, Vector.plus(previous.v, Vector.mult(0.5, kv2)))
    kv4 = Vector.mult(timestep, acc(Vector.plus(previous.r, kv3), Vector.plus(previous.v, kv3),
                                    previous.t + timestep, previous.m - previous.engine * timestep, previous.engine))
    kr4 = Vector.mult(timestep, Vector.plus(previous.v, kv3))
    ans.r = Vector.plus(previous.r, Vector.mult(1.0 / 6,
                                                Vector.plus(kr1, Vector.plus(kr2, Vector.plus(kr2, Vector.plus(kr3,
                                                                                                               Vector.plus(
                                                                                                                   kr3,
                                                                                                                   kr4)))))))
    ans.v = Vector.plus(previous.v, Vector.mult(1.0 / 6,
                                                Vector.plus(kv1, Vector.plus(kv2, Vector.plus(kv2, Vector.plus(kv3,
                                                                                                               Vector.plus(
                                                                                                                   kv3,
                                                                                                                   kv4)))))))
    ans.t = previous.t + timestep
    ans.m = previous.m - timestep * previous.engine
    ans.engine = previous.engine
    return ans;


def test(rvtme):  # возвращает расстояние до Луны, когда наша скорость параллельна поверхности Луны
    global pi
    angle = pi / 2 - Vector.angle(Vector.minus(rvtme.r, moonPosition(rvtme.t)),
                                  Vector.minus(rvtme.v, moonV(rvtme.t)))
    while angle < 0:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        angle = pi / 2 - Vector.angle(Vector.minus(rvtme.r, moonPosition(rvtme.t)),
                                      Vector.minus(rvtme.v, moonV(rvtme.t)))
    return Vector.abs(Vector.minus(rvtme.r, moonPosition(rvtme.t)))


def testDeceleration(rvtme, tau, tStart):  # расчитывает конечные данные
    # при различном времени торможения и начале торможения
    global q2
    currentTime = rvtme.t
    rvtme.engine = 0
    while rvtme.t - currentTime < tStart:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
    rvtme.engine = q2
    currentTime = rvtme.t
    while rvtme.t - currentTime < tau:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
    return rvtme;


def readFloat(f):
    return float(f.readline().strip())


def main():
    global dryMass, mass, GM, Gm, q, q2, R, rMoon, pi

    f = open(INPUT_FILE, 'r')
    r = readFloat(f)
    r += rEarth # считывание
    m = readFloat(f)  # масса топлива в РС
    rvtme = RVTME()  # присваиваивание считанных значений
    rvtme.r = Vector()
    rvtme.v = Vector()
    rvtme.r.x = - r * math.cos(pi / 2 / math.sqrt(2))
    rvtme.r.y = - r * math.sin(pi / 2 / math.sqrt(2))
    rvtme.r.z = 0
    rvtme.v.x = math.sqrt(GM / r) * math.sin(pi / 2 / math.sqrt(2))
    rvtme.v.y = - math.sqrt(GM / r) * math.cos(pi / 2 / math.sqrt(2))
    rvtme.v.z = 0
    rvtme.t = 0
    rvtme.m = mass + m
    print("Начинаем ускорение!")
    print(rvtme.r.x, rvtme.r.y, rvtme.r.z, rvtme.v.x, rvtme.v.y, rvtme.v.z)
    deltaV = math.sqrt(GM) * (math.sqrt(2 / Vector.abs(rvtme.r) - 2 / R) - math.sqrt(1 / Vector.abs(rvtme.r))) + \
             0.0000069 * math.sqrt(1 / Vector.abs(rvtme.r)) * rvtme.m  # дельта скорости, при переходе с околоземной орбиты
    #  на орбиту с большой полуосью R/2
    tau = rvtme.m / q * (1 - math.exp(-deltaV / u))  # время разгона по формуле Циолковского
    rvtme.engine = q
    i = 0

    # ускорение

    while rvtme.t < tau:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) +
                     '\n')
        output2.write(str(Vector.abs(rvtme.r)) + '\t' + str(rvtme.t) + '\n')
        output3.write(str(Vector.abs(rvtme.v)) + '\t' + str(rvtme.t) + '\n')
    print("m_fuel = ", rvtme.m - (dryMass + mass))

    # проверка топлива
    if (rvtme.m - (dryMass + mass)) < 0:
        print("Не хватило топлива!")
    else:
        print("Хватило топлива!")

    # отключение ускорения
    rvtme.engine = 0
    # отделение третьей разгонной ступени
    rvtme.m = mass

    print("Vx после ускорения: ", rvtme.v.x, "км/с ", "Vy после ускорения: ", rvtme.v.y, "км/с ");

    # коррекция( рассчитываем расстояние, когда скорость параллельна поверхности)
    copy = RVTME.copy(rvtme)
    testR = test(copy)
    print("Расстояние, когда скорость параллельна поверхности Луны: ", testR, "км ")
    # При торможении расстояние до поверхности возрастет из-за центробежной силы.
    #  Если мы планируем пролететь по касательной, после торможения высота орбиты будет подходящая
    while abs(testR - rMoon) > 0.00001:
        copy.v = Vector.mult(1 - 0.0000003 * (rMoon - testR) / Vector.abs(copy.v), copy.v)
        testR = test(copy)
        print(testR - rMoon)
    rvtme.v = Vector.copy(copy.v)
    angle = pi / 2 - Vector.angle(Vector.minus(copy.r, moonPosition(copy.t)),
                                  Vector.minus(copy.v, moonV(copy.t)))
    while angle < 0:
        copy = nextRVTME(copy, timestep(acc(copy.r, copy.v, copy.t, copy.m, copy.engine)))
        angle = pi / 2 - Vector.angle(Vector.minus(copy.r, moonPosition(copy.t)),
                                      Vector.minus(copy.v, moonV(copy.t)))
    timeD = copy.t  # время полета(если не тормозить)
    deltaV = Vector.abs(Vector.minus(copy.v, moonV(copy.t))) - \
             math.sqrt(Gm / Vector.abs(Vector.minus(copy.r, moonPosition(copy.t))))  # находим дельта скорости
    # на торможение( достижение первой космической)
    tau = copy.m / q2 * (1 - math.exp(-deltaV / u2))  # время торможения

    print("Полет без ускорения!")
    # полет без ускорения
    while rvtme.t < timeD - 3 * tau:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) +
                     '\n')
        output2.write(str(Vector.abs(rvtme.r)) + '\t' + str(rvtme.t) + '\n')
        output3.write(str(Vector.abs(rvtme.v)) + '\t' + str(rvtme.t) + '\n')

    # коррекция(для нахождения более точного времени торможения и начала торможения)

    # поиск tau - время торможения,
    #  tStasrt - момент начала торможения с момента timeD - 3 * tau, чтобы конечная скорость была равна
    # первой космической и параллельна поверности Луны(выход на орбиту)
    copy = RVTME.copy(rvtme)
    tStart = 2 * tau
    testRvtme = testDeceleration(copy, tau, tStart)  # tau - время торможения,
    #  tStasrt - момент начала торможения с момента timeD - 3 * tau
    testV = Vector.abs(Vector.minus(testRvtme.v, moonV(testRvtme.t))) - \
            math.sqrt(Gm / Vector.abs(Vector.minus(testRvtme.r, moonPosition(testRvtme.t))))
    testAngle = pi / 2 - Vector.angle(Vector.minus(testRvtme.r, moonPosition(testRvtme.t)),
                                      Vector.minus(testRvtme.v, moonV(testRvtme.t)))
    print(testV, " ", testAngle)
    while (abs(testV) > 0.00002) or (abs(testAngle) > 0.00002):  # скорость равна первой космической и
        # параллельна поверхности Луны(выход на орбиту)
        deltaV += testV
        tau = copy.m / q2 * (1 - math.exp(-deltaV / u2))
        tStart -= 1000 * testAngle
        testRvtme = testDeceleration(copy, tau, tStart)
        testV = Vector.abs(Vector.minus(testRvtme.v, moonV(testRvtme.t))) - \
                math.sqrt(Gm / Vector.abs(Vector.minus(testRvtme.r, moonPosition(testRvtme.t))))
        testAngle = pi / 2 - Vector.angle(Vector.minus(testRvtme.r, moonPosition(testRvtme.t)),
                                          Vector.minus(testRvtme.v, moonV(testRvtme.t)))
        print(testV, " ", testAngle, " ", tStart)
    print(" Торможение ", tau, " сек с момента ", tStart, " сек")

    # полет без ускорения (до начала торможения(зная найденное время начала торможения))
    currentTime = rvtme.t
    while rvtme.t - currentTime < tStart:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) +
                     '\n')
        output2.write(str(Vector.abs(rvtme.r)) + '\t' + str(rvtme.t) + '\n')
        output3.write(str(Vector.abs(rvtme.v)) + '\t' + str(rvtme.t) + '\n')
    rvtme.engine = q2

    # торможение
    print("Торможение!")
    currentTime = rvtme.t
    while rvtme.t - currentTime < tau:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) +
                     '\n')
        output2.write(str(Vector.abs(rvtme.r)) + '\t' + str(rvtme.t) + '\n')
        output3.write(str(Vector.abs(rvtme.v)) + '\t' + str(rvtme.t) + '\n')
    rvtme.engine = 0

    print("rx :", Vector.minus(rvtme.r, moonPosition(rvtme.t)).x, "км ", "ry :",
          Vector.minus(rvtme.r, moonPosition(rvtme.t)).y, "км ", "Vx :",
          Vector.minus(rvtme.v, moonV(rvtme.t)).x, "км/с ", "Vy :",
          Vector.minus(rvtme.v, moonV(rvtme.t)).y, "км/с ", "орбита",
          (Vector.abs(Vector.minus(rvtme.r, moonPosition(rvtme.t))) - rMoon), "км ", )

    orbital = Vector.abs(Vector.minus(rvtme.r, moonPosition(rvtme.t))) - rMoon

    print("-----------------------------------")
    print("Луна rx :", moonPosition(rvtme.t).x, "Луна ry :", moonPosition(rvtme.t).y)
    out.write(str(rvtme.r.x) + '\t' + str(rvtme.r.y) + '\t'+ str(moonPosition(rvtme.t).x) + '\t' +
              str(moonPosition(rvtme.t).y) +'\t'+ str(mass - rvtme.m) + '\n')

    # проверка круговой орбиты (тест)
    a = 0
    while rvtme.t < 500000:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        i += 1
        if i % 20000 == 0:
            print(Vector.minus(rvtme.r, moonPosition(rvtme.t)).x, " ",
                  Vector.minus(rvtme.r, moonPosition(rvtme.t)).y, " ",
                  (Vector.abs(Vector.minus(rvtme.r, moonPosition(rvtme.t))) - rMoon))
        if abs(Vector.abs(Vector.minus(rvtme.r, moonPosition(rvtme.t))) - rMoon - orbital) < 0.5:
            a = 0
        else:
            a = 1
    if a == 0:
        print('Мы на орбите!')

main()
output.close()
out.close

#визуализация
import matplotlib.pyplot as plt
import pylab
from numpy import *
string = open('earthtomoon.txt').readlines()
m = array([[float(i) for i in string[k].split()] for k in range((len(string)))])
string1 = open('coordinates.txt').readlines()
m1 = array([[float(j) for j in string1[l].split()] for l in range((len(string1)))])
string2 = open('speed.txt').readlines()
m2 = array([[float(r) for r in string2[s].split()] for s in range((len(string2)))])

from matplotlib.pyplot import *
plt.title('Траектория полета', size=15)
plot(list(m[:, 0]), list(m[:, 1]), "-*k", markersize=0.1)
plt.xlabel('Координата x, км')
plt.ylabel('Координата y, км')
plt.grid()
show()

plt.title(' Расстояние от центра Земли от времени', size=15)
plot(list(m1[:, 1]/1000), list(m1[:, 0]), "-*k", markersize=0.1)
plt.ylabel('Расстояние, км ')
plt.xlabel('Время, 10^3 c')
plt.grid()
show()

plt.title(' Cкорость от времени', size=15)
plot(list(m2[:, 1]/1000), list(m2[:, 0]), "-*k", markersize=0.1)
plt.ylabel('Скорость, км/с ')
plt.xlabel('Время, 10^3 с')
plt.grid()
show()

i=0
while i < 460000:
    pylab.subplot(131);
    plt.scatter(m[i][0], m[i][1], color='black');# y(x)
    pylab.subplot(132);
    plt.scatter(m2[i][1]/1000, m2[i][0], color='black'); # r(t)
    pylab.subplot(133)
    plt.scatter(m1[i][1]/1000, m1[i][0], color='black'); # v(t)
    i += 1000;
    plt.pause(0.001)
plt.pause(10)
output.close
output2.close
output3.close