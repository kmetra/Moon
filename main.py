import fourth_stage as four

#necessary constants
R_Moon = 1738000


x_start = 0
y_start = R_Moon


V_aft_bl , H_aft_bl = four.blast(x_start, y_start)
print(V_aft_bl, H_aft_bl)
