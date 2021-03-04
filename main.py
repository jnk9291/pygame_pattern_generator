from bullet import *

pg.init()
clock = pg.time.Clock()

crashed = False

bullet = BulletThread(pg.image.load('talb1.png'), width / 2, height / 2, 0, 0, 3,fire_rate=5, spin=1)
all_sprites.add(bullet)
while not crashed:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pg.display.flip()
    pg.display.update()
    clock.tick(60)
pg.quit()
