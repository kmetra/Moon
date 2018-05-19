from math import cos, sin, log, radians, sqrt
import unittest

R_Moon = 1738000  # радиус Луны
g_Moon = 1.62
# определяем точку старта для взлета и начальные скорости
M = 2355
m = 2355
fuel_exp = 5.1  # кг/с
fuel_speed = 3050  # м/с
Vx = 0
Vy = 0


def blast_off(time, angle):
    '''
    function for simple step of flight
    :param time: time of flight
    :param angle: direction of the ship
    :return: chages in coordinates, speed, fuel mass
    '''
    global x, y, Vx, Vy, m, M
    x = x + Vx * time - fuel_speed * cos(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    y = y + Vy * time - 0.5 * g_Moon * time ** 2 - fuel_speed * sin(radians(angle)) * (
            (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    Vx = Vx - fuel_speed * cos(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    Vy = Vy - g_Moon * time - fuel_speed * sin(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    m = m - fuel_exp * time
    high = sqrt(x ** 2 + y ** 2) - R_Moon


def blast(x_start, y_start):
    '''
    summarizing all the steps of flight scenery
    :param x_start: x starting coordinate
    :param y_start: y starting coordinate
    :return:  list of [New orbital speed, Orbital hight]
    '''
    global x, y
    x = x_start
    y = y_start
    for i in range(1, 62):
        blast_off(1, 90 - i)
    blast_off(135, 28)
    for i in range(1, 28):
        blast_off(8, 28 - i)
    Vres = sqrt(Vx ** 2 + Vy ** 2)
    Hres = sqrt(x ** 2 + y ** 2) - R_Moon
    return (Vres, Hres)


class TestBlastMethods(unittest.TestCase):

    def testAssertTrue(self):
            V_current, H_current = blast(0, R_Moon)
            self.assertTrue((1590 < V_current < 1650) and (49000 < H_current < 51000))


if __name__ == '__main__':
    unittest.main()

