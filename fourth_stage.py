from math import cos, sin, log, radians, sqrt
import unittest
import matplotlib.pyplot as plt
import pylab

R_Moon = 1738000  # радиус Луны
g_Moon = 1.62
# определяем точку старта для взлета и начальные скорости
M = 2355 #масса корабля и пилота
m = 2355 #масса топлива на взлет
fuel_exp = 5.1  # кг/с скорость корабля
fuel_speed = 3050  # м/с скорость (относительная) испускания топлива
Vx = 0 # скорость старта
Vy = 0 # скорость посадки

points_of_speed=[] #  данные для построения скорости корабля от времени
points_of_hight=[] # данные для построения высоты орбиты корабля от времени
points_of_coordinates=[] # данные для построения координат корабля
timeall = 0
def blast_off(time, angle):
    '''
    function for simple step of flight,
    using angle and time of flight
    :param time: time of flight
    :param angle: direction of the ship
    :return: chages in coordinates, speed, fuel mass
    '''
    global x, y, Vx, Vy, m, M, points_of_speed, points_of_hight, timeall, points_of_coordinates
    #  рассчет координат, скорости и массы оставшегося после маневра топлива
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
    points_of_coordinates.append([x,y-R_Moon])
def blast(x_start, y_start):
    '''
    summarizing all the steps of flight scenery
    :param x_start: x starting coordinate
    :param y_start: y starting coordinate
    :return:  list of [New orbital speed, Orbital hight]
    '''
    global x, y, points_of_speed, points_of_hight, points_of_coordinates, timeall
    timeall = 0
    x = x_start
    y = y_start
    for i in range(1, 62): # подготовительный вертикальный взлет
        blast_off(1, 90 - i)
    for i in range(1,28): # основной этап взлета
        blast_off(5,28)
    for i in range(1, 28): # выход на необходимую Лунную орбиту
        blast_off(8, 28 - i)
    Vres = sqrt(Vx ** 2 + Vy ** 2)
    Hres = sqrt(x ** 2 + y ** 2) - R_Moon
    visualisation(points_of_coordinates,points_of_hight,points_of_speed)
    return (Vres, Hres, m) #  функция выдает необходимые для дальнейших тестов параметры

def visualisation(pointsdots,pointshight,pointsspeed):
    plt.ion()  # начало построения визуализации
    fig = plt.figure(figsize=(10, 8))
    pylab.subplot(131)
    plt.title(' Орбитальная скорость 1598 м/с', size=8)
    plt.axis([0, 500, 0, 2500])
    plt.ylabel(u'Скорость Лунного модуля, м/с ')
    plt.xlabel(u'Время взлета, с')

    pylab.subplot(132)
    plt.title(' Высота орбиты 50.3 км', size=8)
    plt.axis([0, 500, 0, 60])
    plt.ylabel(u'Высота над поверхностью, км ')
    plt.xlabel(u'Время взлета, с')

    pylab.subplot(133)
    plt.title(' Координаты Лунного модуля', size=8)
    plt.axis([0, 500, 0, 60])
    plt.ylabel(u'Координата y, км ')
    plt.xlabel(u'Координата х, км')
    i = 0
    while i < 115:
        pylab.subplot(131)
        plt.scatter(pointsspeed[i][1], pointsspeed[i][0], color='r');
        pylab.subplot(132)
        plt.scatter(pointshight[i][1], pointshight[i][0] / 1000, color='green');
        pylab.subplot(133)
        plt.scatter(pointsdots[i][0] / 1000, pointsdots[i][1] / 1000, color='blue');
        i += 1;
        plt.pause(0.001)
    plt.pause(4)


# class TestBlastMethods(unittest.TestCase):
#     def testresultsTrue(self):
#         V_current, H_current, m_current=blast(0,R_Moon)
#         self.assertTrue((1590 < V_current < 1650))
#         self.assertTrue((49000 < H_current < 51000))
#         self.assertTrue(m_current>=0)


if __name__ == '__main__':
    unittest.main()
