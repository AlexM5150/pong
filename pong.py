import pygame
import sys
import os
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'

black = (0, 0, 0)
white = (255, 255, 255)
green = (100, 205, 100)
win_w = 920
win_h = 570

pygame.mixer.pre_init(44100, -16, 2, 2048)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((win_w, win_h), pygame.SRCALPHA)
        self.l_up = self.l_down = self.r_up = self.r_down = False
        self.clock = pygame.time.Clock()
        self.play = self.intro = True
        self.outro1 = self.outro2 = False
        self.intro_back = pygame.Surface((win_w, win_h)).convert()
        self.intro_rect = self.intro_back.get_rect()
        self.game_back = pygame.Surface((win_w, win_h)).convert()
        self.game_rect = self.game_back.get_rect()
        self.outro_back = pygame.Surface((win_w, win_h)).convert()
        self.outro_rect = self.outro_back.get_rect()

        self.title = Text(120, 'Pong', win_w/2.75, win_h/4, white)
        self.subtitle = Text(90, '-- Click Here --', win_w / 4, win_h/1.8, white)
        self.endtitle = Text(120, 'Player 1 Wins!!!', win_w/6, win_h/4, white)
        self.endtitle2 = Text(120, 'Player 2 Wins!!!', win_w/6, win_h/4, white)
        self.left_score = Text(90, "0", win_w / 4, win_h / 10, white)
        self.right_score = Text(90, "0", win_w / 1.4, win_h / 10, white)

    def blink(self, subtitle, subtitle_rect):
        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(subtitle, subtitle_rect)

    def restart(self, ball, lp, rp):
        self.left_score.image = self.left_score.font.render(str(lp.score), 1, white)
        self.right_score.image = self.right_score.font.render(str(rp.score), 1, white)
        ball.rect.centerx = win_w / 2
        ball.rect.centery = win_h / 2
        lp.rect.centerx = 100
        lp.rect.centery = (win_h / 2)
        rp.rect.centerx = 920 - (40 * 2.5)
        rp.rect.centery = (win_h / 2)
        time.sleep(1.5)

    def update(self, ball, lp, rp):
        if ball.rect.left > win_w:
            lp.score += 1
            self.restart(ball, lp, rp)

        elif ball.rect.right < 0:
            rp.score += 1
            self.restart(ball, lp, rp)

        if lp.score == 3:
            lp.score = 0
            rp.score = 0
            self.play = False
            self.outro1 = True
            self.restart(ball, lp, rp)

        elif rp.score == 3:
            lp.score = 0
            rp.score = 0
            self.play = False
            self.outro2 = True
            self.restart(ball, lp, rp)


class Text:
    def __init__(self, size, text, xpos, ypos, color):
        self.font = pygame.font.SysFont('Britannic Bold', size)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)


class Paddle:
    def __init__(self, width, height, speed, xpos):
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.Surface((self.width, self.height)).convert()
        self.image.fill(green)
        self.rect = pygame.Rect(xpos, (win_h / 2) - (self.height / 2), self.width, self.height)
        self.score = 0

    def update(self, up, down):
        if up:
            self.rect.y -= self.speed
        if down:
            self.rect.y += self.speed

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > win_h:
            self.rect.bottom = win_h


class Ball:
    def __init__(self, dim, speed):
        self.dim = dim
        self.speed = speed
        self.image = pygame.Surface((self.dim, self.dim))
        self.image.fill(green)
        self.rect = pygame.Rect(win_w/2, win_h / 2 - (self.dim / 2), self.dim, self.dim)
        

    def update(self, lp, rp):
        if self.rect.top < 0 or self.rect.top > win_h - self.rect.height:
            self.speed[1] = -self.speed[1]

        if self.rect.left > lp.rect.right - 5 and self.rect.left < lp.rect.right + 5 and self.rect.bottom > lp.rect.top and self.rect.top < lp.rect.bottom:
            self.speed[0] = -self.speed[0]

        elif self.rect.right < rp.rect.left + 5 and self.rect.right > rp.rect.left - 5 and self.rect.bottom > rp.rect.top and self.rect.top < rp.rect.bottom:
            self.speed[0] = -self.speed[0]

        self.rect = self.rect.move(self.speed)


def main():
    global black, white, green, win_w, win_h
    pygame.init()
    pygame.display.set_caption('Pong')

    run = Game()

    left_paddle = Paddle(40, 160, 8, 40 * 2)
    right_paddle = Paddle(40, 160, 8, 920 - (40 * 3))
    ball = Ball(30, [13, 13])

    while run.intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.intro = False

        run.screen.blit(run.intro_back, run.intro_rect)
        run.screen.blit(run.title.image, run.title.rect)
        run.blink(run.subtitle.image, run.subtitle.rect)
        run.clock.tick(60)
        pygame.display.flip()

    while True:
        while run.play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        run.l_up = True
                        run.l_down = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            run.l_up = False
                            run.l_down = True

                    if event.key == pygame.K_DOWN:
                        run.r_up = False
                        run.r_down = True

                    elif event.key == pygame.K_UP:
                        run.r_up = True
                        run.r_down = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        run.l_up = False
                        run.l_down = False

                    elif event.key == pygame.K_s:
                        run.l_up = False
                        run.l_down = False

                    if event.key == pygame.K_DOWN:
                        run.r_up = False
                        run.r_down = False

                    elif event.key == pygame.K_UP:
                        run.r_up = False
                        run.r_down = False

            left_paddle.update(run.l_up, run.l_down)
            right_paddle.update(run.r_up, run.r_down)
            ball.update(left_paddle, right_paddle)
            run.update(ball, left_paddle, right_paddle)

            run.screen.blit(run.game_back, run.game_rect)
            run.screen.blit(left_paddle.image, left_paddle.rect)
            run.screen.blit(right_paddle.image, right_paddle.rect)
            run.screen.blit(ball.image, ball.rect)

            run.screen.blit(run.left_score.image, run.left_score.rect)
            run.screen.blit(run.right_score.image, run.right_score.rect)
            pygame.display.flip()
            run.clock.tick(60)

            while run.outro1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                        run.outro1 = False
                        run.play = True

                run.screen.blit(run.outro_back, run.outro_rect)
                run.screen.blit(run.endtitle.image, run.endtitle.rect)
                run.blink(run.subtitle.image, run.subtitle.rect)
                run.clock.tick(60)
                pygame.display.flip()

            while run.outro2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                        run.outro2 = False
                        run.play = True

                run.screen.blit(run.outro_back, run.outro_rect)
                run.screen.blit(run.endtitle2.image, run.endtitle2.rect)
                run.blink(run.subtitle.image, run.subtitle.rect)
                run.clock.tick(60)
                pygame.display.flip()

if __name__ == "__main__":
    main()
