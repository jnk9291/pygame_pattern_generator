from math import sin, pi, cos, degrees, atan
from variables import *


class Bullet(pg.sprite.Sprite):
    """ Constructor function for the bullet class."""

    def __init__(self, image, x, y, direction, speed, acceleration, curve):
        pg.sprite.Sprite.__init__(self)
        self.direction = direction
        self.dirX = Bullet.x_direction(self.direction)
        self.dirY = Bullet.y_direction(self.direction)
        self.speed = speed
        self.x_speed = self.dirX * self.speed
        self.y_speed = self.dirY * self.speed
        self.image = pg.transform.rotozoom(image, calculate_angle(self.x_speed, self.y_speed),1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.radius = self.rect
        self.acceleration = acceleration
        self.curve = curve

    def update(self):
        """pygame.sprite.Sprite class update method."""
        self.direction += self.curve
        self.speed += self.acceleration

        self.dirX = Bullet.x_direction(self.direction)
        self.dirY = Bullet.y_direction(self.direction)

        self.x_speed = self.dirX * self.speed
        self.y_speed = self.dirY * self.speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if not screen.get_rect().contains(self):
            self.kill()

    @staticmethod
    def x_direction(angle):
        return cos(angle * pi / 180)

    @staticmethod
    def y_direction(angle):
        return -sin(angle * pi / 180)


def calculate_angle(x, y):
    if x < 0 and y < 0:
        angle = degrees(atan(x / y))
        return 180 + angle
    elif x < 0 and y > 0:
        angle = degrees(atan(x / y))
        return 270 + angle
    elif x > 0 and y < 0:
        angle = degrees(atan(x / y))
        return angle
    elif x > 0 and y > 0:
        angle = degrees(atan(x / y))
        return 180 + angle
    elif x == 0 and y > 0:
        return 180
    elif x == 0 and y < 0:
        return 0
    elif x > 0 and y == 0:
        return 90
    elif x < 0 and y == 0:
        return -90
    else:
        return 0


class BulletThread(pg.sprite.Sprite):
    def __init__(self, image, x, y, acceleration, bullet_curve, bullet_speed, bullets_per_array=10, pattern_arrays=1,
                 spread_within_array=1, spread_between_array=1, default_angle=0, spin=0, spin_increase=0,
                 invert_spin=False, max_spin=0, fire_rate=1):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('mask.png')
        self.rect = self.image.get_rect()
        self.bullet_image = image
        self.array_angle = 0
        self.bullet_angle = 0
        self.bullets_per_array = bullets_per_array
        self.spread_within_array = spread_within_array
        self.rect.center = (x, y)
        self.object_width = 1
        self.object_height = 1
        self.last_shooting = pg.time.get_ticks()
        self.default_angle = default_angle
        self.spin = spin
        self.spin_increase = spin_increase
        self.invert_spin = invert_spin
        self.max_spin = max_spin
        self.fire_rate = fire_rate
        self.spread_between_array = spread_between_array
        self.pattern_arrays = pattern_arrays
        self.bullet_speed = bullet_speed
        self.bullet_curve = bullet_curve
        self.acceleration = acceleration

    def update(self):
        center = self.rect.center
        bullet_length = self.bullets_per_array - 1
        if bullet_length == 0:
            bullet_length = 1

        array_length = self.pattern_arrays - 1 * self.pattern_arrays
        if array_length == 0:
            array_length = 1

        self.array_angle = (self.spread_within_array / bullet_length)
        self.bullet_angle = (self.spread_between_array / array_length)
        if pg.time.get_ticks() - self.last_shooting > self.fire_rate:
            self.last_shooting = pg.time.get_ticks()
            for i in range(0, self.pattern_arrays):
                for j in range(0, self.bullets_per_array):
                    self.shoot(i, j, self.array_angle, self.bullet_angle)
                    self.rect.center = center

            if self.default_angle > 360:
                self.default_angle = 0

            self.default_angle += self.spin
            self.spin += self.spin_increase

            if self.invert_spin:
                if self.spin < -self.max_spin or self.spin > self.max_spin:
                    self.spin_increase = -self.spin_increase

    @staticmethod
    def lengthdir_x(dist, angle):
        return dist * cos((angle * pi) / 180)

    @staticmethod
    def lengthdir_y(dist, angle):
        return dist * -sin((angle * pi) / 180)

    def shoot(self, i, j, array_angle, bullet_angle):
        x_value = self.rect.centerx
        # BulletThread.lengthdir_x(self.object_width,self.default_angle + (bullet_angle * i) + (array_angle * j))
        y_value = self.rect.centery
        # BulletThread.lengthdir_x(self.object_width,self.default_angle + (bullet_angle * i) + (array_angle * j))

        direction = self.default_angle + (bullet_angle * i) + (array_angle * j)

        bullet = Bullet(self.bullet_image, x_value, y_value, direction, self.bullet_speed, self.acceleration,
                        self.bullet_curve)

        all_sprites.add(bullet)
