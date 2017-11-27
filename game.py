import pygame
from pygame.locals import *
import math
import random


# 1 - 게임 초기화
pygame.init()
width, height = 640, 480  # 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [200, 250]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 200
pygame.mixer.init()

# 2 - 이미지
player = pygame.image.load("resources/images/monkey.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
running = 1
exitcode = 0

# 3 - 오디오
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0)
enemy.set_volume(0)
shoot.set_volume(0.08)
pygame.mixer.music.load('resources/audio/music.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(100)

# 4 - 게임 루프
while running:
    badtimer -= 1
    screen.fill(0)

# 5 배경 그리기
    for x in range(1):
        for y in range(1):
            screen.blit(grass, (x*640, y*480))
    screen.blit(castle, (0, 80))

# 6 - 마우스로 캐릭터 방향조절
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360 - angle * 57.29)
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)

# 7 - 바나나(총알) 그리기
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 15
        vely = math.sin(bullet[0]) * 18
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

# 8 - 너구리(적) 그리기
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 80 - (badtimer1 * 2)  # 적 출현 빈도
        if badtimer1 >= 20:
            badtimer1 = 20
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        badguy[0] -= 10  # 적 속도

# 9 - 바나나 나무가 공격받았을 때
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= 10
            badguys.pop(index)
        index1 = 0

# 10 - 적이 바나나(총알)하고 충돌했을 때
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

# 11 - 시간 표시
    font = pygame.font.Font(None, 50)
    survivedtext = font.render(
        str("TIME") + " " + str(int((120000 - pygame.time.get_ticks()) / 1000 % 1200)).zfill(2), True, (255, 255, 0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survivedtext, textRect)

# 12 - HP바 표시
    screen.blit(healthbar, (8, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1 + 8, 8))
    pygame.display.flip()


# 13 - 입력 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            arrows.append([math.atan2(position[1] - (playerpos1[1] + 70), position[0] - (playerpos1[0] + 40)),
                           playerpos1[0] + 70, playerpos1[1] + 70])

# 14 - 캐릭터 움직이는 속도
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 3
    elif keys[3]:
        playerpos[0] += 3

# 15 - 승리, 패배 조건
    if pygame.time.get_ticks() >= 120000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0

# 16 - 승리, 패배 화면표시
if exitcode == 0:
    screen.blit(gameover, (-55, 0))
else:
    screen.blit(youwin, (0, 0))
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()




