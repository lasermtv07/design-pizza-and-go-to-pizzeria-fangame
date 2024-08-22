#!/usr/bin/python3
import pygame as pg
import sys
pg.init()
screen=pg.display.set_mode((1280,720))
#player
player=pg.image.load('gfx/player.png')
px=50
py=50
flip=False
v=5
count=5
#pizzas
pizza=pg.image.load('gfx/pizza.png')
pizzas=[]
offset=10
mv=7
cooldown=10
while True:
    screen.fill((0,0,0))
    for e in pg.event.get():
        if e.type==pg.QUIT: exit(0)
        if e.type==pg.KEYDOWN and e.key==32 and cooldown<0 and count>0:
            if not flip: pizzas.append([px+64,py+offset,flip])
            else: pizzas.append([px-92,py+offset,flip])
            cooldown=10
            count-=1
    #draws border
    for i in range(24):
        if i%2==1: pg.draw.rect(screen,(255,255,255),pg.Rect(450+64,i*30,30,30))
        else: pg.draw.rect(screen,(255,255,255),pg.Rect(450+64+30,i*30,30,30))
    pg.draw.line(screen,(255,255,255),(450+64,0),(450+64,720))
    pg.draw.line(screen,(255,255,255),(450+64+60,0),(450+64+60,720))
    #draw pizzas
    n=[]
    for i in range(len(pizzas)):
        j=pizzas[i]
        screen.blit(pizza,(j[0],j[1]))
        if not j[2]: pizzas[i][0]+=mv
        else: pizzas[i][0]-=mv
        if j[0]>-100 and j[0]<1280: n.append(j)
    pizzas=n

    #handle player
    if not flip: screen.blit(player,(px,py))
    else: screen.blit(pg.transform.flip(player,True,False),(px,py))
    k=pg.key.get_pressed()
    if (k[pg.K_w] or k[pg.K_UP]) and py>0:
        py-=v
    if (k[pg.K_s] or k[pg.K_DOWN]) and py<720-128:
        py+=v
    if (k[pg.K_d] or k[pg.K_RIGHT]) and px<450:
        px+=v
        flip=False
    if (k[pg.K_a] or k[pg.K_LEFT]) and px>0:
        px-=v
        flip=True
    #draw pizza counter
    for i in range(count):
        pg.draw.rect(screen,(250,80,30),pg.Rect(px+50,py+offset+50-20*i,80,20))
        pg.draw.rect(screen,(150,80,30),pg.Rect(px+55,py+offset+55-20*i,70,10))
    cooldown-=1
    pg.display.update()
    pg.time.Clock().tick(60)
