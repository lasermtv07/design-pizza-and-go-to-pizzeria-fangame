#!/usr/bin/python3
import pygame as pg
import sys
import random as r
pg.init()
screen=pg.display.set_mode((1280,720))
#player
player=pg.image.load('gfx/player.png')
px=50
py=450
flip=False
v=7
count=0
#pizzas
pizza=pg.image.load('gfx/pizza.png')
pizzas=[]
offset=10
mv=12
cooldown=10
pizzaMatrix=[
    [True,True],
    [True,True],
    [True,True]
]
#kids
kid=pg.image.load('gfx/kid.png')
kids=[]
#summons kids
def summon(c):
    rows=[]
    global kids
    if c<=24:
        rows.append(c-r.randint(0,c))
        c-=rows[0]
        rows.append(c-r.randint(0,c))
        c-=rows[1]
        rows.append(c-r.randint(0,c))
        c-=rows[2]
        rows.append(c-r.randint(0,c))
        c-=rows[3]
    for i in range(len(rows)):
        d=[]
        for j in range(10):
            if rows[i]>0:
                d.append(1)
                rows[i]-=1
            else: d.append(0)
        r.shuffle(d)
        print(d)
        for j in range(len(d)):
            if d[j]==1: kids.append([600+100*i,70*j,5])
    return rows
print(summon(3))

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
    #pizza pickup
    pg.draw.rect(screen,(30,30,30),pg.Rect(30,30,244,356))
    off=0
    for i in pizzaMatrix:

        if i[0]: screen.blit(pizza,(50,50+off*112))
        if i[1]: screen.blit(pizza,(50+92+20,50+off*112))
        if px>50-64 and px<50+92 and py>50+off*112-128 and py<50+off*112+92 and i[0]:
            if count<=6:
                pizzaMatrix[off][0]=False
                count+=1
        if px>50-64+92+20 and px<50+2*92+20 and py>50+off*112-128 and py<50+off*112+92 and i[1]:
            if count<=6:
                pizzaMatrix[off][1]=False
                count+=1
        off+=1
    #draw pizzas
    n=[]
    for i in range(len(pizzas)):
        j=pizzas[i]
        screen.blit(pizza,(j[0],j[1]))
        if not j[2]: pizzas[i][0]+=mv
        else: pizzas[i][0]-=mv
        if j[0]>-100 and j[0]<1280: n.append(j)
    pizzas=n
    #handle kids
    off=0
    for i in kids:
        screen.blit(kid,(i[0],i[1]))
        k=len(pizzas)-1
        while k>=0:
            j=pizzas[k]
            if j[0]+92>i[0] and j[1]+92>i[1] and j[1]<i[1]+92 :
                del pizzas[k]
                kids[off][2]-=1
                if kids[off][2]<1:
                    del kids[off]
                    k-=1
            k-=1
        off+=1
    if len(kids)==0:
        summon(r.randint(1,24))
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
        if not flip:
            pg.draw.rect(screen,(250,80,30),pg.Rect(px+50,py+offset+50-20*i,80,20))
            pg.draw.rect(screen,(150,80,30),pg.Rect(px+55,py+offset+55-20*i,70,10))
        else:
            pg.draw.rect(screen,(250,80,30),pg.Rect(px-70,py+offset+50-20*i,80,20))
            pg.draw.rect(screen,(150,80,30),pg.Rect(px-65,py+offset+55-20*i,70,10))
    #replenish pizzas
    empty=True
    for i in pizzaMatrix:
        if i[0] or i[1]: empty=False
    if empty:
        pick=[r.randint(0,2),r.randint(0,1)]
        pick2=[r.randint(0,2),r.randint(0,1)]
        while pick2==pick:
            pick2=[r.randint(0,2),r.randint(0,1)]
        pizzaMatrix[pick[0]][pick[1]]=True
        pizzaMatrix[pick2[0]][pick2[1]]=True
    for i in range(len(pizzaMatrix)):
        if r.random()<0.01 and not ((px>30 and px<30+244) and (py>30 and py<30+356)):
            pizzaMatrix[i][r.randint(0,1)]=True
    cooldown-=1
    pg.display.update()
    pg.time.Clock().tick(60)
