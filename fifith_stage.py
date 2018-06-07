
import math
import sys
import matplotlib.pyplot as plt
import pylab
from numpy import *
output = open('moontoearth.txt', 'w')
INPUT_FILE = 'input.txt'
gEarth = 0.00981
gMoon = 0.00162
rEarth = 6375
rMoon = 1738
GM = gEarth * rEarth * rEarth
Gm = gMoon * rMoon * rMoon
R = 384405  # radius of the Moon's orbit
pi = math.pi
Tmoon = 2 * pi * math.sqrt(R * R * R / GM)
dryMass = 10300  # сухая масса стадии разгона
F = 95.75 # реактивная тяга
u = 3.05  # фактическая скорость выпуска ускоряющей ступени
q = F / u  # потребление топлива (в килограммах в секунду) ускоряющей стадии


class Vector:
    def plus(a, b):
        # возвращает сумму векторов
        ans = Vector()
        ans.x = a.x + b.x
        ans.y = a.y + b.y
        ans.z = a.z + b.z
        return ans

    def minus(a, b):
        # возвращает разность векторов
        ans = Vector()
        ans.x = a.x - b.x
        ans.y = a.y - b.y
        ans.z = a.z - b.z
        return ans

    def absV(a):
        # возвращает модудь вектора
        return math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z)

    def mult(k, a):
        # результат умножения вектора на скаляр
        ans = Vector()
        ans.x = k * a.x
        ans.y = k * a.y
        ans.z = k * a.z
        return ans

    def angle(v, u):
        # возвращает угол между веторами
        a = Vector.absV(v)
        b = Vector.absV(u)
        c = v.x * u.x + v.y * u.y + v.z * u.z
        return math.acos(c / a / b)

    def copy(a):
        ans = Vector()
        ans.x = a.x
        ans.y = a.y
        ans.z = a.z
        return ans


class RVTME:
    # содержит текущую позицию, скорость, время общее массовое и булево состояние двигателя
    # (0 - off, q - acceleration)
    def copy(rvtme):
        ans = RVTME()
        ans.r = Vector.copy(rvtme.r)
        ans.v = Vector.copy(rvtme.v)
        ans.t = rvtme.t
        ans.m = rvtme.m
        ans.engine = rvtme.engine
        return ans


def moonPosition(time):
    # положение Луны в данный момент времени(т.к. она обращается)
    global R, pi, Tmoon
    ans = Vector()
    ans.x = R * math.cos(2 * pi * time / Tmoon)
    ans.y = R * math.sin(2 * pi * time / Tmoon)
    ans.z = 0
    return ans


def moonV(time):
    # скорость Луны в данный момент времени
    global Tmoon, pi, R
    ans = Vector()
    ans.x = -2 * pi * R / Tmoon * math.sin(2 * pi * time / Tmoon)
    ans.y = 2 * pi * R / Tmoon * math.cos(2 * pi * time / Tmoon)
    ans.z = 0
    return ans


def timestep(a, deltaT=0.00005):
    # возвращает непостоянный промежуток времени, чтобы сделать нашу модель более точной
    return deltaT / Vector.absV(a)


def acc(r, v, time, mass, engine):
    # возвращает ускорение устройства в данный момент времени
    global GM, Gm, q, F, q2, F2
    aEarth = Vector.mult(-GM / (Vector.absV(r) * Vector.absV(r) * Vector.absV(r)), r)
    moon = Vector.minus(r, moonPosition(time))
    aMoon = Vector.mult(-Gm / (Vector.absV(moon) * Vector.absV(moon) * Vector.absV(moon)), moon)
    aEngine = Vector()
    if engine == 0:
        aEngine.x = 0
        aEngine.y = 0
        aEngine.z = 0
    if engine == q:
        aEngine = Vector.mult(F / mass / Vector.absV(v), v)
        # пусть сила и скорость будут сонаправлены
    return Vector.plus(aEngine, Vector.plus(aEarth, aMoon))


def nextRVTME(previous, timestep):
    # возвращает следующее значение положения и скорости устройства (методом Рунге-Кутты)
    ans = RVTME()
    v1 = Vector.mult(timestep, acc(previous.r, previous.v, previous.t, previous.m, previous.engine))
    r1 = Vector.mult(timestep, previous.v)
    v2 = Vector.mult(timestep,
                     acc(Vector.plus(previous.r, Vector.mult(0.5, v1)), Vector.plus(previous.v, Vector.mult(0.5, v1)),
                         previous.t + timestep / 2, previous.m - 0.5 * previous.engine * timestep, previous.engine))
    r2 = Vector.mult(timestep, Vector.plus(previous.v, Vector.mult(0.5, v2)))
    v3 = Vector.mult(timestep,
                     acc(Vector.plus(previous.r, Vector.mult(0.5, v2)), Vector.plus(previous.v, Vector.mult(0.5, v2)),
                         previous.t + timestep / 2, previous.m - 0.5 * previous.engine * timestep, previous.engine))
    r3 = Vector.mult(timestep, Vector.plus(previous.v, Vector.mult(0.5, v3)))
    v4 = Vector.mult(timestep, acc(Vector.plus(previous.r, v3), Vector.plus(previous.v, v2),
                                   previous.t + timestep, previous.m - previous.engine * timestep, previous.engine))
    r4 = Vector.mult(timestep, Vector.plus(previous.v, v4))
    ans.r = Vector.plus(previous.r, Vector.mult(1.0 / 6,
                                                Vector.plus(r1, Vector.plus(r2, Vector.plus(r2, Vector.plus(r3,
                                                                                                            Vector.plus(
                                                                                                                r3,
                                                                                                                r4)))))))
    ans.v = Vector.plus(previous.v, Vector.mult(1.0 / 6,
                                                Vector.plus(v1, Vector.plus(v2, Vector.plus(v2, Vector.plus(v3,
                                                                                                            Vector.plus(
                                                                                                                v3,
                                                                                                                v4)))))))
    ans.t = previous.t + timestep
    ans.m = previous.m - timestep * previous.engine
    ans.engine = previous.engine
    return ans;


def test(rvtme):
    # возвращает расстояние до Земли, когда наша скорость параллельна поверхности Земли
    angle = pi / 2 - Vector.angle(rvtme.r, rvtme.v)
    while (angle < 0) or (Vector.absV(rvtme.r) > 100000):
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        angle = pi / 2 - Vector.angle(rvtme.r, rvtme.v)

    return Vector.absV(rvtme.r)


def readFloat(f):
    return float(f.readline().strip())


def main():
    global dryMass, GM, Gm, q, q2, R, rMoon, pi, u
    f = open(INPUT_FILE, 'r')
    x = readFloat(f)
    y = readFloat(f)
    z = readFloat(f)
    vx = readFloat(f)
    vy = readFloat(f)
    vz = readFloat(f)
    mFuel = readFloat(f)  # Масса топлива
    rvtme = RVTME()
    rvtme.r = Vector()
    rvtme.v = Vector()
    rvtme.r.x = x
    rvtme.r.y = y
    rvtme.r.z = z
    rvtme.v.x = vx
    rvtme.v.y = vy
    rvtme.v.z = vz
    rvtme.t = 0
    rvtme.m = dryMass  + mFuel

    deltaV = -Vector.absV(Vector.minus(rvtme.v, moonV(rvtme.t))) + \
             math.sqrt(2 * Gm / Vector.absV(Vector.minus(rvtme.r, moonPosition(rvtme.t)))) + \
             math.sqrt(100 / Vector.absV(Vector.minus(rvtme.r, moonPosition(rvtme.t))))

    # нам нужно увеличить нашу скорость примерно на это значение
    tau = rvtme.m / q * (1 - math.exp(-deltaV / u))
    print(deltaV, " ", tau)

    # время разгона(согласно уравнению Циолковского)
    rvtme.engine = q  # взлетаем
    i = 0
    while rvtme.t < tau:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) + '\t'+ str(Vector.absV(rvtme.r)) +
                     '\t' + str(Vector.absV(rvtme.v)) + '\t' + str(rvtme.t) + '\n')
        i += 1
        if i % 10000 == 0:
            print(rvtme.r.x, " ", rvtme.r.y)
    rvtme.engine = 0
    print(Vector.absV(Vector.minus(rvtme.v, moonV(rvtme.t))))
    print(math.sqrt(2 * Gm / Vector.absV(Vector.minus(rvtme.r, moonPosition(rvtme.t)))))
    print(Vector.absV(Vector.minus(rvtme.r, moonPosition(rvtme.t))))

    # ускорение
    # ждем 1 час
    # вначале полета есть время, когда скорость параллельна Земле. Проходим расстояние, когда скорость параллельна
    while rvtme.t < 3600:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine)))
        output.write(str(rvtme.r.x) + '\t'
                     + str(rvtme.r.y) + '\t' + str(Vector.absV(rvtme.r)) +
                     '\t' + str(Vector.absV(rvtme.v)) + '\t' + str(rvtme.t) + '\n')
        i += 1
        if i % 50000 == 0:
            print(rvtme.r.x, " ", rvtme.r.y)

    # ждем час
    # корректируем
    copy = RVTME.copy(rvtme)
    testR = test(copy)
    print(testR)
    while abs(testR - rEarth - 70) > 0.00001:
        copy.v = Vector.mult(1 - 0.0000085 * (rEarth + 70 - testR) / Vector.absV(copy.v), copy.v)
        testR = test(copy)
        print(testR - rEarth)

    print("Reached 1 cm tolerance")
    print("We must increase our velocity by ", 1000 * Vector.absV(Vector.minus(copy.v, rvtme.v)), " m/s")
    rvtme.v = Vector.copy(copy.v)
    angle = pi / 2 - Vector.angle(rvtme.r, rvtme.v)
    while angle < 0:
        rvtme = nextRVTME(rvtme, timestep(acc(rvtme.r, rvtme.v, rvtme.t, rvtme.m, rvtme.engine), 0.00001))
        angle = pi / 2 - Vector.angle(rvtme.r, rvtme.v)
        i += 1
        if i % 50000 == 0:
            print(rvtme.r.x, " ", rvtme.r.y)
        output.write(str(rvtme.r.x) + '\t' + str(rvtme.r.y) + '\t' + str(Vector.absV(rvtme.r)) +
                         '\t' + str(Vector.absV(rvtme.v)) + '\t' + str(rvtme.t) + '\n')

    print("-----------------------------------")
    print("Finish!")
    print(math.sqrt(rvtme.r.x*rvtme.r.x + rvtme.r.y*rvtme.r.y)-rEarth)
    print(rvtme.m - dryMass)
main()

string = open('moontoearth.txt').readlines()
m = array([[float(i) for i in string[k].split()] for k in range((len(string)))])
from matplotlib.pyplot import *
plt.title(' y(x) ', size=11)
plot(list(m[:, 0]), list(m[:, 1]), "blue", markersize=0.1)
plt.xlabel('Координата x, км')
plt.ylabel('Координата y, км')
plt.grid()
show()

plt.title(' r(t) ', size=11)
plot(list(m[:, 4]), list(m[:, 2]), "blue", markersize=0.1)
plt.ylabel('Расстояние, км ')
plt.xlabel('Время, c')
plt.grid()
show()

plt.title(' V(t) ', size=11)
plot(list(m[:, 4]), list(m[:, 3]), "blue", markersize=0.1)
plt.ylabel('Скорость, км/с ')
plt.xlabel('Время, с')
plt.grid()
show()
