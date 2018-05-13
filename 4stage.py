from math import cos,sin,log,radians,sqrt
# взлет с Луны
R_Moon = 1738000 # радиус Луны
g_Moon = 1.62
# определяем точку старта для взлета и начальные скорости
M = 4670
m = 2355
fuel_exp = 1.1  #кг/с
fuel_speed = 3050 #м/с
def blast_off(x_start, y_start, time, angle):
    global Vx, Vy, x, y, m, M
    x = x_start
    y = y_start
    Vx = 0
    Vy = 0
    x = x + Vx * time - fuel_speed * cos(radians(angle)) * (
                (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    y = y + Vy * time - 0.5 * g_Moon * time ** 2 - fuel_speed * sin(radians(angle)) * (
                (-(M + m) / fuel_exp + time) * log((m + M - fuel_exp * time) / (m + M)) - time)
    Vx = Vx - fuel_speed * cos(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    Vy = Vy - g_Moon * time - fuel_speed * sin(radians(angle)) * log((m + M - fuel_exp * time) / (m + M))
    m = m - fuel_exp * time
    high = sqrt(x ** 2 + y ** 2) - R_Moon
    print(x, y, Vx, Vy, m, high )

blast_off(0, R_Moon, 2000, 90)