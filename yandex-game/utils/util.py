

from math import atan, sin, cos, sqrt


def shoot(src_pos, tgt_pos, plasm_spd):
    """Получить вектор скорости для попадания из src_pos в tgt_pos."""
    dx = tgt_pos[0] - src_pos[0]
    dy = tgt_pos[1] - src_pos[1]
    if dx == 0:
        x_vel = 0
        y_vel = plasm_spd if dy > 0 else -plasm_spd
    else:
        angle = atan(dy / dx)
        x_vel = cos(angle) * plasm_spd
        y_vel = sin(angle) * plasm_spd
        if tgt_pos[0] < src_pos[0]:
            x_vel = -x_vel
            y_vel = -y_vel
    return x_vel, y_vel


def calc_distance_sq(rect_1, rect_2):
    """Вычислить расстояние между двумя прямоугольниками."""
    dx = rect_1.x - rect_2.x
    dy = rect_1.y - rect_2.y
    distance = dx ** 2 + dy ** 2
    return distance


def handle_collision(object_rect, obstacle_rect, x_vel, y_vel):
    """
    Обработать столкновение объекта с препятствием,
    не дать пройти насквозь.
    """
    if x_vel > 0:   object_rect.right = obstacle_rect.left
    elif x_vel < 0: object_rect.left = obstacle_rect.right
    if y_vel > 0:   object_rect.bottom = obstacle_rect.top
    elif y_vel < 0: object_rect.top = obstacle_rect.bottom
