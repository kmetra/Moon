from math import cos, sin, log, radians, sqrt
import unittest
import matplotlib.pyplot as plt
import pylab

R_Moon = 1738000  # радиус Луны
g_Moon = 1.62
# определяем точку старта для взлета и начальные скорости
M = 2355
m = 2355
fuel_exp = 5.1  # кг/с
fuel_speed = 3050  # м/с
Vx = 0
Vy = 0

points_of_speed=[]
points_of_hight=[]
timeall = 0
def blast_off(time, angle):
    '''
    function for simple step of flight
    :param time: time of flight
    :param angle: direction of the ship
    :return: chages in coordinates, speed, fuel mass
    '''
    global x, y, Vx, Vy, m, M, points_of_speed, points_of_hight, timeall
    x = x + Vx * time - fuel_speed * cos(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    y = y + Vy * time - 0.5 * g_Moon * time ** 2 - fuel_speed * sin(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    Vx = Vx - fuel_speed * cos(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    Vy = Vy - g_Moon * time - fuel_speed * sin(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    m = m - fuel_exp * time
    high = sqrt(x ** 2 + y ** 2) - R_Moon
    timeall+=time
    points_of_speed.append([sqrt(Vx**2+Vy**2),timeall])
    points_of_hight.append([high, timeall])
def blast(x_start, y_start):
    '''
    summarizing all the steps of flight scenery
    :param x_start: x starting coordinate
    :param y_start: y starting coordinate
    :return:  list of [New orbital speed, Orbital hight]
    '''
    global x, y, points_of_speed, points_of_hight, timeall
    timeall = 0
    x = x_start
    y = y_start
    for i in range(1, 62):
        blast_off(1, 90 - i)
    for i in range(1,28):
        blast_off(5,28)
    for i in range(1, 28):
        blast_off(8, 28 - i)
    Vres = sqrt(Vx ** 2 + Vy ** 2)
    Hres = sqrt(x ** 2 + y ** 2) - R_Moon
    plt.ion()  ## Note this correction
    fig = plt.figure('Visualisation')
    pylab.subplot(121)
    plt.title(' Орбитальная скорость = 1598 м/с',size=10)
    plt.axis([0, 500, 0, 2500])
    plt.ylabel(u'Скорость Лунного модуля, м/с ')
    plt.xlabel(u'Время взлета, с')
    pylab.subplot(122)
    plt.title(' Высота орбиты = 50.3 км', size=10)
    plt.axis([0, 500, 0, 60])
    plt.ylabel(u'Высота над поверхностью Луны, км ')
    plt.xlabel(u'Время взлета, с')
    i = 0
    while i < 115:
        pylab.subplot(121)
        plt.scatter(points_of_speed[i][1], points_of_speed[i][0], color='red');
        pylab.subplot(122)
        plt.scatter(points_of_hight[i][1], points_of_hight[i][0] / 1000, color='green');
        i += 1;
        plt.pause(0.001)
    plt.pause(4)
    return (Vres, Hres)


class TestBlastMethods(unittest.TestCase):

    def testAssertTrue(self):
            V_current, H_current = blast(0, R_Moon)
            self.assertTrue((1590 < V_current < 1650) and (49000 < H_current < 51000))


#if __name__ == '__main__':
    #unittest.main()


