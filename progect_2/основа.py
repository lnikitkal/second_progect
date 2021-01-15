import os
import sys
import pygame
import sqlite3

play_start = False
language = 0


def give(n):
    con = sqlite3.connect('prog_2.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT info FROM cafe
                    WHERE id = {n}""").fetchall()[0][0]
    con.close()
    return str(result)


def iq(point):
    con = sqlite3.connect('prog_2.db')
    cur = con.cursor()
    result = str(int(cur.execute("""SELECT info FROM cafe
                WHERE id = 1""").fetchall()[0][0]) + point)
    cur.execute(f"""UPDATE cafe
    SET info = {result}
    WHERE id = 1""")
    con.commit()
    con.close()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def detect_lang(s):
    return s + '_en' if language == 0 else s + '_rus'


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(-800, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def detect(event):
    global global_pos
    global play_start
    global hp_hero
    global hp_enemy
    global queue
    global language
    if global_pos == 0:
        if 1088 <= event[0] <= 1407 and 411 <= event[1] <= 509:
            # play
            image = pygame.image.load(detect_lang('Уровни') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            font = pygame.font.Font(None, 90)
            text = font.render('IQ ' + str(give(1)), True, (0, 0, 0))
            screen.blit(text, (1250, 50))
            global_pos = 1
        elif 1088 <= event[0] <= 1407 and 527 <= event[1] <= 623:
            # магазин
            image = pygame.image.load(detect_lang('Магазин') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            font = pygame.font.Font(None, 90)
            text = font.render('IQ ' + str(give(1)), True, (0, 0, 0))
            screen.blit(text, (1250, 50))
            if give(2)[0] == '1':
                image = pygame.image.load('Маска1.png').convert_alpha()
                screen.blit(image, (0, 0))
            if give(2)[1] == '1':
                image = pygame.image.load('Маска2.png').convert_alpha()
                screen.blit(image, (0, 0))
            global_pos = 2
        elif 40 <= event[0] <= 154 and 639 <= event[1] <= 750:
            # настройки
            image = pygame.image.load(detect_lang('Настройки') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 3
    elif global_pos == 1:
        if 77 <= event[0] <= 214 and 222 <= event[1] <= 359:
            # уровень 1
            play_start = True
            global_pos = 11

            hp_hero = 150 if give(2)[1] == '2' else 100
            hp_enemy = 100
            queue = 0
        elif 37 <= event[0] <= 162 and 37 <= event[1] <= 110:
            # стрелка назад
            image = pygame.image.load(detect_lang('Меню') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 0
    elif global_pos == 2:
        if 37 <= event[0] <= 162 and 37 <= event[1] <= 110:
            # стрелка назад
            image = pygame.image.load(detect_lang('Меню') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 0
        elif 200 <= event[0] <= 400 and 160 <= event[1] <= 359 and give(2)[0] == '1' and int(
                give(1)) >= 10:
            con = sqlite3.connect('prog_2.db')
            cur = con.cursor()
            result = str(int(cur.execute("""SELECT info FROM cafe
                            WHERE id = 1""").fetchall()[0][0]) - 10)
            cur.execute(f"""UPDATE cafe
                SET info = {result}
                WHERE id = 1""")

            result = cur.execute("""SELECT info FROM cafe
                                        WHERE id = 2""").fetchall()[0][0]
            cur.execute(f"""UPDATE cafe
                            SET info = {'2' + str(result)[1:]}
                            WHERE id = 2""")
            con.commit()
            con.close()
            global_pos = 0
            detect((1088, 623))
        elif 450 <= event[0] <= 650 and 160 <= event[1] <= 359 and give(2)[1] == '1' and int(
                give(1)) >= 20:
            con = sqlite3.connect('prog_2.db')
            cur = con.cursor()
            result = str(int(cur.execute("""SELECT info FROM cafe
                            WHERE id = 1""").fetchall()[0][0]) - 20)
            cur.execute(f"""UPDATE cafe
                SET info = {result}
                WHERE id = 1""")

            result = cur.execute("""SELECT info FROM cafe
                                        WHERE id = 2""").fetchall()[0][0]
            cur.execute(f"""UPDATE cafe
                            SET info = {str(result)[0] + '2' + str(result)[2:]}
                            WHERE id = 2""")
            con.commit()
            con.close()
            global_pos = 0
            detect((1088, 623))


    elif global_pos == 3:
        if 37 <= event[0] <= 162 and 37 <= event[1] <= 110:
            # стрелка назад
            image = pygame.image.load(detect_lang('Меню') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 0
        elif 494 <= event[0] <= 527 and 202 <= event[1] <= 223:
            image = pygame.image.load(detect_lang('Настройки_выбор') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 31
            # выбор языка
    elif global_pos == 31:
        if language and 287 <= event[0] <= 535 and 243 <= event[1] <= 296:
            language = 0
            image = pygame.image.load('Настройки_en.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 3
        elif not language and 287 <= event[0] <= 535 and 298 <= event[1] <= 352:
            language = 1
            image = pygame.image.load('Настройки_rus.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 3
        else:
            image = pygame.image.load(detect_lang('Настройки') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 3

    elif global_pos == 11:
        if event == 'exit':
            image = pygame.image.load(detect_lang('Уровни') + '.jpg').convert_alpha()
            screen.blit(image, (0, 0))
            global_pos = 1
            pygame.display.flip()


def new_start():
    image = pygame.image.load(detect_lang('Уровень') + '.jpg').convert_alpha()
    screen.blit(image, (0, 0))

    image = pygame.image.load('Общий план.png').convert_alpha()
    screen.blit(image, (0, 350))

    pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20), 0)
    pygame.draw.rect(screen, (50, 150, 50),
                     (50, 60, hp_hero * int(300 / 150 if give(2)[1] == '2' else 300 / 100), 20), 0)
    pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

    pygame.draw.rect(screen, (100, 100, 100), (1150, 60, 300, 20), 0)
    pygame.draw.rect(screen, (50, 150, 50), (1150, 60, hp_enemy * int(300 / 100), 20), 0)
    pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

    font = pygame.font.Font(None, 30)
    text = font.render(str(hp_hero), True, (0, 0, 0))
    screen.blit(text, (180, 62))
    text = font.render(str(hp_enemy), True, (0, 0, 0))
    screen.blit(text, (1280, 62))


if __name__ == '__main__':
    pygame.init()
    size = w, h = 1500, 800
    screen = pygame.display.set_mode(size)
    run = True
    screen.fill((255, 255, 255))

    image = pygame.image.load(detect_lang('Меню') + '.jpg').convert_alpha()
    screen.blit(image, (0, 0))

    global_pos = 0

    hp_hero = 100
    hp_enemy = 100
    queue = 0
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                detect(ev.pos)
            if ev.type == pygame.KEYDOWN:
                if ev.key == 32:
                    pass
        if play_start:
            new_start()

            if not queue:
                all_sprites = pygame.sprite.Group()
                image = pygame.image.load(detect_lang('Ты атакуешь') + '.png').convert_alpha()
                screen.blit(image, (300, 200))
                end = False
                clock = pygame.time.Clock()
                pos_rect = 0
                polzunok = 0
                while not end:
                    pygame.draw.rect(screen, (50, 150, 50), (400, 600, 700, 50), 0)
                    pygame.draw.rect(screen, (255, 182, 36) if give(2)[0] == '1' else (255, 0, 0),
                                     (700, 600, 100, 50), 0)
                    pygame.draw.rect(screen, (255, 0, 0), (725, 600, 50, 50), 0)
                    if not pos_rect and polzunok > 488:
                        pos_rect = 1
                    if pos_rect and polzunok < 5:
                        pos_rect = 0
                    if not pos_rect:
                        polzunok += clock.tick()
                    else:
                        polzunok -= clock.tick()
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (int(400 + (polzunok / 500) * 700), 600, 10, 50), 0)
                    pygame.draw.rect(screen, (0, 0, 0), (400, 600, 700, 50), 2)
                    pygame.display.flip()
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            run = False
                            end = True
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            if 734 <= ev.pos[0] <= 765 and 20 <= ev.pos[1] <= 55:
                                image = pygame.image.load(
                                    detect_lang('игровое меня') + '.png').convert_alpha()
                                screen.blit(image, (0, 0))
                                pygame.display.flip()
                                ff = True
                                while ff:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT:
                                            run = False
                                            end = True
                                            ff = False
                                        if ev.type == pygame.MOUSEBUTTONDOWN:
                                            if 524 <= ev.pos[0] <= 956 and 259 <= ev.pos[1] <= 332:
                                                ff = False
                                                clock = pygame.time.Clock()
                                                new_start()

                                            elif 524 <= ev.pos[0] <= 956 and 379 <= ev.pos[
                                                1] <= 452:
                                                ff = False
                                                end = True
                                                detect('exit')
                                                play_start = False
                                            elif 524 <= ev.pos[0] <= 956 and 500 <= ev.pos[
                                                1] <= 573:
                                                ff = False
                                                end = True
                                                hp_hero = 100
                                                hp_enemy = 100
                                                queue = 0

                        if ev.type == pygame.KEYDOWN:
                            if ev.key == 32:
                                end = True
                                queue = 1
                                time = 0
                                clock = pygame.time.Clock()
                                while time < 3000:
                                    time += clock.tick()
                                anim = AnimatedSprite(load_image("Перс.png"), 1, 23, 800, 350)
                                clock = pygame.time.Clock()
                                time = 0
                                while time <= 1150:
                                    time += clock.tick()
                                    if time % 50 == 0:
                                        image = pygame.image.load(
                                            detect_lang('Уровень') + '.jpg').convert_alpha()
                                        screen.blit(image, (0, 0))
                                        image = pygame.image.load(
                                            detect_lang('Ты атакуешь') + '.png').convert_alpha()
                                        screen.blit(image, (300, 200))
                                        pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20),
                                                         0)
                                        pygame.draw.rect(screen, (50, 150, 50),
                                                         (50, 60, hp_hero * int(
                                                             300 / 150 if give(2)[
                                                                              1] == '2' else 300 / 100),
                                                          20), 0)
                                        pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

                                        pygame.draw.rect(screen, (100, 100, 100),
                                                         (1150, 60, 300, 20), 0)
                                        pygame.draw.rect(screen, (50, 150, 50), (
                                            1150, 60, hp_enemy * int(300 / 100), 20), 0)
                                        pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

                                        font = pygame.font.Font(None, 30)
                                        text = font.render(str(hp_hero), True, (0, 0, 0))
                                        screen.blit(text, (180, 62))
                                        text = font.render(str(hp_enemy), True, (0, 0, 0))
                                        screen.blit(text, (1280, 62))

                                        anim.update()
                                        all_sprites.draw(screen)
                                        pygame.display.flip()
                                if 725 <= 400 + (polzunok / 500) * 700 <= 775:
                                    hp_enemy -= 20
                                elif 700 <= 400 + (polzunok / 500) * 700 <= 800:
                                    hp_enemy -= 15 if give(2)[0] == '1' else 20
                                else:
                                    hp_enemy -= 10

                                if hp_enemy > 0:
                                    pygame.draw.rect(screen, (100, 100, 100), (1150, 60, 300, 20),
                                                     0)
                                    pygame.draw.rect(screen, (50, 150, 50),
                                                     (1150, 60, hp_enemy * int(300 / 100), 20),
                                                     0)
                                    pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

                                    font = pygame.font.Font(None, 30)
                                    text = font.render(str(hp_hero), True, (0, 0, 0))
                                    screen.blit(text, (180, 62))
                                    text = font.render(str(hp_enemy), True, (0, 0, 0))
                                    screen.blit(text, (1280, 62))
                                else:
                                    image = pygame.image.load(
                                        detect_lang('Уровень') + '.jpg').convert_alpha()
                                    screen.blit(image, (0, 0))
                                    image = pygame.image.load('Общий план.png').convert_alpha()
                                    screen.blit(image, (0, 350))

                                    pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20), 0)
                                    pygame.draw.rect(screen, (50, 150, 50),
                                                     (50, 60, hp_hero * int(300 / 150 if give(2)[
                                                                                             1] == '2' else 300 / 100),
                                                      20), 0)
                                    pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

                                    pygame.draw.rect(screen, (100, 100, 100),
                                                     (1150, 60, 300, 20), 0)
                                    pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

                                    font = pygame.font.Font(None, 30)
                                    text = font.render(str(hp_hero), True, (0, 0, 0))
                                    screen.blit(text, (180, 62))
                                    text = font.render(str(0), True, (0, 0, 0))
                                    screen.blit(text, (1280, 62))

                                    image = pygame.image.load(
                                        detect_lang('Ты победил') + '.png').convert_alpha()
                                    screen.blit(image, (300, 150))
                                    pygame.display.flip()
                                    play_start = False
                                    iq(15)

                                    time = 0
                                    clock = pygame.time.Clock()
                                    while time < 5000:
                                        time += clock.tick()
                                    detect('exit')

                                pygame.display.flip()
                                time = 0
                                clock = pygame.time.Clock()
                                while time < 2000:
                                    time += clock.tick()
            else:
                all_sprites = pygame.sprite.Group()
                image = pygame.image.load(detect_lang('Ты защищаешься') + '.png').convert_alpha()
                screen.blit(image, (300, 200))
                end = False
                clock = pygame.time.Clock()
                pos_rect = 0
                polzunok = 0
                while not end:
                    pygame.draw.rect(screen, (50, 150, 50), (400, 600, 700, 50), 0)
                    pygame.draw.rect(screen, (255, 182, 36) if give(2)[0] == '1' else (255, 0, 0),
                                     (700, 600, 100, 50), 0)
                    pygame.draw.rect(screen, (255, 0, 0), (725, 600, 50, 50), 0)
                    if not pos_rect and polzunok > 488:
                        pos_rect = 1
                    if pos_rect and polzunok < 5:
                        pos_rect = 0
                    if not pos_rect:
                        polzunok += clock.tick()
                    else:
                        polzunok -= clock.tick()
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (int(400 + (polzunok / 500) * 700), 600, 10, 50), 0)
                    pygame.draw.rect(screen, (0, 0, 0), (400, 600, 700, 50), 2)
                    pygame.display.flip()
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            run = False
                            end = True
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            if 734 <= ev.pos[0] <= 765 and 20 <= ev.pos[1] <= 55:
                                image = pygame.image.load(
                                    detect_lang('игровое меня') + '.png').convert_alpha()
                                screen.blit(image, (0, 0))
                                pygame.display.flip()
                                ff = True
                                while ff:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT:
                                            run = False
                                            end = True
                                            ff = False
                                        if ev.type == pygame.MOUSEBUTTONDOWN:
                                            if 524 <= ev.pos[0] <= 956 and 259 <= ev.pos[1] <= 332:
                                                ff = False
                                                clock = pygame.time.Clock()
                                                new_start()

                                            elif 524 <= ev.pos[0] <= 956 and 379 <= ev.pos[
                                                1] <= 452:
                                                ff = False
                                                end = True
                                                detect('exit')
                                                play_start = False
                                            elif 524 <= ev.pos[0] <= 956 and 500 <= ev.pos[
                                                1] <= 573:
                                                ff = False
                                                end = True
                                                hp_hero = 100
                                                hp_enemy = 100
                                                queue = 0
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == 32:
                                end = True
                                queue = 0
                                time = 0
                                clock = pygame.time.Clock()
                                while time < 3000:
                                    time += clock.tick()
                                anim = AnimatedSprite(load_image('Враг.png'), 1, 15, 800, 350)
                                clock = pygame.time.Clock()
                                time = 0
                                while time <= 1050:
                                    time += clock.tick()
                                    if time % 70 == 0:
                                        image = pygame.image.load(
                                            detect_lang('Уровень') + '.jpg').convert_alpha()
                                        screen.blit(image, (0, 0))
                                        image = pygame.image.load(
                                            detect_lang('Ты защищаешься') + '.png').convert_alpha()
                                        screen.blit(image, (300, 200))

                                        pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20),
                                                         0)
                                        pygame.draw.rect(screen, (50, 150, 50),
                                                         (50, 60, hp_hero * int(
                                                             300 / 150 if give(2)[
                                                                              1] == '2' else 300 / 100),
                                                          20), 0)
                                        pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

                                        pygame.draw.rect(screen, (100, 100, 100),
                                                         (1150, 60, 300, 20), 0)
                                        pygame.draw.rect(screen, (50, 150, 50), (
                                            1150, 60, hp_enemy * int(300 / 100), 20), 0)
                                        pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

                                        font = pygame.font.Font(None, 30)
                                        text = font.render(str(hp_hero), True, (0, 0, 0))
                                        screen.blit(text, (180, 62))
                                        text = font.render(str(hp_enemy), True, (0, 0, 0))
                                        screen.blit(text, (1280, 62))

                                        anim.update()
                                        all_sprites.draw(screen)
                                        pygame.display.flip()
                                if 725 <= 400 + (polzunok / 500) * 700 <= 775:
                                    hp_hero -= 10
                                elif 700 <= 400 + (polzunok / 500) * 700 <= 800:
                                    hp_hero -= 15 if give(2)[0] == '1' else 10
                                else:
                                    hp_hero -= 20

                                if hp_hero > 0:
                                    pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20), 0)
                                    pygame.draw.rect(screen, (50, 150, 50),
                                                     (50, 60, hp_hero * int(300 / 150 if give(2)[
                                                                                             1] == '2' else 300 / 100),
                                                      20), 0)
                                    pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

                                    font = pygame.font.Font(None, 30)
                                    text = font.render(str(hp_hero), True, (0, 0, 0))
                                    screen.blit(text, (180, 62))
                                else:
                                    image = pygame.image.load(
                                        detect_lang('Уровень') + '.jpg').convert_alpha()
                                    screen.blit(image, (0, 0))
                                    image = pygame.image.load('Общий план.png').convert_alpha()
                                    screen.blit(image, (0, 350))

                                    pygame.draw.rect(screen, (100, 100, 100), (50, 60, 300, 20),
                                                     0)
                                    pygame.draw.rect(screen, (0, 0, 0), (50, 60, 300, 20), 2)

                                    pygame.draw.rect(screen, (100, 100, 100), (1150, 60, 300, 20),
                                                     0)
                                    pygame.draw.rect(screen, (50, 150, 50),
                                                     (1150, 60, hp_enemy * int(300 / 100), 20),
                                                     0)
                                    pygame.draw.rect(screen, (0, 0, 0), (1150, 60, 300, 20), 2)

                                    font = pygame.font.Font(None, 30)
                                    text = font.render(str(0), True, (0, 0, 0))
                                    screen.blit(text, (180, 62))
                                    text = font.render(str(hp_enemy), True, (0, 0, 0))
                                    screen.blit(text, (1280, 62))

                                    image = pygame.image.load(
                                        detect_lang('Ты проиграл') + '.png').convert_alpha()
                                    screen.blit(image, (300, 150))
                                    pygame.display.flip()
                                    play_start = False
                                    time = 0
                                    clock = pygame.time.Clock()
                                    while time < 5000:
                                        time += clock.tick()
                                    detect('exit')
                                pygame.display.flip()
                                time = 0
                                clock = pygame.time.Clock()
                                while time < 2000:
                                    time += clock.tick()

        pygame.display.flip()