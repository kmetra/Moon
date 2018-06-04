from math import sqrt

G = 6.67e-11
M = 7.36e22
Radius = 1738000
mass_space_ship = 6835
mass_engine = 8135
t_overall = 0

x = 0
y = 1788000
v_x = -1656.9
v_y = 0
int_period = 0.01

def changing_system_of_coordinates (x_moon, y_moon, x_ship, y_ship):
    cos = y / sqrt(x**2 + y**2)
    sin = x / sqrt(x**2 + y**2)
    x_move = x_ship - x_moon
    y_move = y_ship - y_moon
    x_turn = x_move * cos - y_move * sin
    y_turn = x_move * sin + y_move * cos
    return (x_turn, y_turn)


def a_x_and_a_y (x, y, grav_const = G, mass_moon = M):
    a_x = - (grav_const * mass_moon * x) / ((x**2 + y**2)**1.5)
    a_y = - (grav_const * mass_moon * y) / ((x**2 + y**2)**1.5)
    return (a_x, a_y)

def speed_after_impuls (x, y, v_x, v_y, t = int_period, r = Radius):
    height_finish = r + 10000
    min_speed = v_x + 11  #больше этой скорости брать смысла нет, так как минимальный радиус орбиты 50 км, учтено, чтобы после импульса ЛМ не врезался в поверхность луны
    x_probe = x
    y_probe = y
    v_y_probe = v_y
    while height_finish > r + 3000:
        min_speed += 0.5
        x = x_probe
        y = y_probe
        v_x = min_speed
        v_y = v_y_probe
        while x <= 0:
            a_x, a_y = a_x_and_a_y(x, y)
            x = x + v_x * t + a_x * (t ** 2) / 2
            y = y + v_y * t + a_y * (t ** 2) / 2
            v_x = v_x + a_x * t
            v_y = v_y + a_y * t
        height_finish = abs(y)
        print (min_speed, height_finish)
    return (min_speed)

print (speed_after_impuls(x, y, v_x, v_y))


print (x, y, v_x, v_y)

'''t = int_period
while x <= 0:
    a_x, a_y = a_x_and_a_y(x, y)
    x = x + v_x * t + a_x * (t ** 2) / 2
    y = y + v_y * t + a_y * (t ** 2) / 2
    v_x = v_x + a_x * t
    v_y = v_y + a_y * t
print (x, y, v_x, v_y)'''
