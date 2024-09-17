#!/usr/bin/python3

# DESIGN PIZZA & GO To PIZZERIA
# a fnaf fangame by
# (c) lasermtv07, 2024
# this software is FOSS, released under the MIT license

import pygame as pg
from pygame import mixer
import sys
import random as r
import math as m
#write/read file functions
def parseData():
    try:
        d=[None,None,None]
        f=open('data.txt','r')
        fd=f.read()
        fd=fd.split("\n")
        for i in fd:
            t=i.split(":")
            if t[0]=='pizza':
                d[0]=[True if i=='1' else False for i in t[1]]
            elif t[0]=='high':
                d[1]=int(t[1])
            elif t[0]=='scan':
                if t[1]=='1': d[2]=True
                else: d[2]=False
        f.close()
    except Exception:
        d=[[True,False,False,False,False,False],0,True]
        fn=open('data.txt','w')
        fn.write("pizza:100000\nhigh:0\nscan:1")
        fn.close()
    return d
def writePizza(d):
    f=open('data.txt','r')
    fd=f.read()
    fd=fd.split("\n")
    for i in range(len(fd)):
        j=fd[i].split(":")
        if j[0]=='pizza':
            fd[i]='pizza:'
            for k in d:
                if k: fd[i]+="1"
                else: fd[i]+="0"
    f.close()
    f=open("data.txt","w")
    f.write("\n".join(fd))
    f.close()
def writeHigh(d):
    f=open('data.txt','r')
    fd=f.read()
    n=""
    for i in fd.split("\n"):
        t=i.split(":")
        if t[0]=="high":
            n+=f'high:{d}\n'
        else:
            if i!="\n": n+=i+"\n"
    f.close()
    f=open("data.txt","w")
    f.write(n)
    f.close()
def writeScan(d):
    p=parseData()
    pt=""
    for i in p[0]:
        if i:pt+="1"
        else: pt+="0"
    o=f'pizza:{pt}\n'
    o+=f"high:{p[1]}\n"
    if d: o+="scan:1"
    else: o+="scan:0"
    f=open('data.txt','w')
    f.write(o)
    f.close()
pg.init()
screen=pg.display.set_mode((1280,720))
stage=3
pause=False
#sound
mixer.init()
scoreS=pg.mixer.Sound('sfx/score.wav')
hitS=pg.mixer.Sound('sfx/hit.wav')
collectS=pg.mixer.Sound('sfx/collect.wav')
shootS=pg.mixer.Sound('sfx/shoot.wav')
#player
player=pg.image.load('gfx/player.png')
panimc=0
panimf=False
px=50
py=450
flip=False
v=7
count=0
wave=1
score=0
genHealth=lambda w:10*60*(w+1)
health=genHealth(1)
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

saved=parseData()

#pizza designs
pepperoni=pg.image.load('gfx/pepperoni.png')
sausage=pg.image.load('gfx/sausage.png')
onion=pg.image.load('gfx/onion.png')
mushroom=pg.image.load('gfx/mushrooms.png')
olive=pg.image.load('gfx/olives.png')
pepper=pg.image.load('gfx/peppers.png')
designs=saved[0]
#kids
kid=pg.image.load('gfx/kid.png')
fullKid=pg.image.load('gfx/fullKid.png')
fullId=-1
fullIdTimer=0
kids=[]
#summons kids
def summon(c):
    global kids
    rows=[[0 for j in range(9)] for i in range(7)]
    for i in range(c):
        j=r.randint(0,6)
        l=r.randint(0,8)
        while rows[j][l]!=0:
            j=r.randint(0,6)
            l=r.randint(0,8)
        rows[j][l]=1
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j]!=0:
                kids.append([650+70*j,100*i,5])
    print(kids)
    return rows
print(summon(5))
def drawScanlines():
    global saved
    global screen
    if saved[2]:
        for i in range(m.floor(720/3)):
            pg.draw.line(screen,(0,0,0),(0,3*i),(1280,3*i))
#font
font = pg.font.Font(pg.font.get_default_font(), 24)
text=font.render('Score: 0',True,(255,255,255),(0,0,0))
textRect=text.get_rect()
textRect.top=0
textRect.right=1280
#shadow freddy
shadow=pg.image.load('gfx/shadow.png')
sy=250
delay=1
delC=60
delDel=True
vel=7
#floating text
floaty=font.render('100',True,(255,255,255),(0,0,0))
floatyTodraw=[]
#other inicialization vars
buttons=saved[0]
overRest=False
overMenu=False
overPlay=False
overDes=False
overBack=False
overSwitch=False
#draws pizzeria wall
def drawWall():
    global screen
    pg.draw.rect(screen,(100,100,100),pg.Rect(0,0,1280,200))
    pg.draw.rect(screen,(50,50,50),pg.Rect(0,150,1280,50))
    for i in range(52):
        if i%2==0:
            pg.draw.rect(screen,(255,255,255),pg.Rect(25*i-10,110,25,25))
            pg.draw.rect(screen,(0,0,0),pg.Rect(25*i-10,135,25,25))
        else:
            pg.draw.rect(screen,(0,0,0),pg.Rect(25*i-10,110,25,25))
            pg.draw.rect(screen,(255,255,255),pg.Rect(25*i-10,135,25,25))
    pg.draw.line(screen,(255,0,0),(0,110),(1280,110),width=5)
    pg.draw.line(screen,(255,0,0),(0,160),(1280,160),width=5)
while True:
    if stage==3:
        screen.fill((0,0,0))
        drawWall()
        #ignore the name i uhh. borrowed this code from other part of the program
        gameOv=pg.font.Font(pg.font.get_default_font(),48)
        tl1=gameOv.render('Design Pizza',True,(255,255,255),(0,0,0,0))
        screen.blit(tl1,(400,250))
        tl2=gameOv.render('& Go To Pizzeria',True,(255,255,255),(0,0,0,0))
        screen.blit(tl2,(450,300))   
        fonts = pg.font.Font(pg.font.get_default_font(), 32)
        if overPlay: pl=fonts.render('play',True,(0,0,255),(0,0,0))
        else: pl=fonts.render('play',True,(255,255,255),(0,0,0))
        if overDes: dp=fonts.render('design pizza',True,(0,0,255),(0,0,0))
        else: dp=fonts.render('design pizza',True,(255,255,255),(0,0,0))
        screen.blit(pl,(550,400))
        screen.blit(dp,(550,450))
        
        if saved[2]: stx="scanlines: yes"
        else: stx="scanlines: no"
        if overSwitch: screen.blit(fonts.render(stx,True,(0,0,255),(0,0,0)),(10,670))
        else: screen.blit(fonts.render(stx,True,(255,255,255),(0,0,0)),(10,670))
        #disc=fangame of FNAF by Scott Cawthon"
        screen.blit(font.render("(c) lasermtv07, under MIT license",True,(255,255,255),(0,0,0)),(830,650))
        screen.blit(font.render("fangame of a game by Scott Cawthon",True,(255,255,255),(0,0,0)),(830,680))
        if pg.mouse.get_pos()[0]<235 and pg.mouse.get_pos()[1]>665 and pg.mouse.get_pos()[1]<710:
            overSwitch=True
        else:
            overSwitch=False
        if pg.mouse.get_pos()[0]>540 and pg.mouse.get_pos()[0]<760:
            if pg.mouse.get_pos()[1]>395 and pg.mouse.get_pos()[1]<440:
                overPlay=True
            else: overPlay=False
            if pg.mouse.get_pos()[1]>450 and pg.mouse.get_pos()[1]<490:
                overDes=True
            else: overDes=False
        else:
            overPlay=False
            overDes=False
        
        drawScanlines()
        pg.display.update()
        for e in pg.event.get():
            if e.type==pg.QUIT: exit()
            if e.type==pg.MOUSEBUTTONDOWN:
                if overPlay:
                    scoreS.play()
                    stage=1
                if overDes:
                    scoreS.play()
                    stage=2
                if overSwitch:
                    scoreS.play()
                    writeScan(not saved[2])
                    saved=parseData()
        continue

    if stage==0:
        screen.fill((0,0,0))
        #draw game over text
        drawWall()
        if int(saved[1])<score:
            saved[1]=score
            writeHigh(score)
        tx=gameOv.render('game over!',True,(255,255,255),(0,0,0))
        screen.blit(tx,(500,260))
        sc=font.render(f'Score: {score}',True,(255,255,255),(0,0,0))
        screen.blit(sc,(560,324))
        hs=font.render(f'Highscore: {saved[1]}',True,(255,255,255),(0,0,0))
        screen.blit(hs,(560,360))
        #draw buttons
        mopo=pg.mouse.get_pos()
        if mopo[1]>428 and mopo[1]<432+32 and mopo[0]>560 and mopo[0]<650:
            overRest=True
        else:
            overRest=False
        if mopo[1]>432+34 and mopo[1]<432+34+32 and mopo[0]>560 and mopo[0]<760:
            overMenu=True
        else:
            overMenu=False
        if not overRest: ovr=font.render('restart',True,(255,255,255),(0,0,0))
        else: ovr=font.render('restart',True,(0,0,255),(0,0,0))
        if not overMenu: ovm=font.render('return to menu',True,(255,255,255),(0,0,0))
        else: ovm=font.render('return to menu',True,(0,0,255),(0,0,0))
        screen.blit(ovr,(560,432))
        screen.blit(ovm,(560,432+36))
        drawScanlines()
        pg.display.update()
        for e in pg.event.get():
            if e.type==pg.QUIT: exit()
            if e.type==pg.MOUSEBUTTONDOWN and (overRest or overMenu):
                wave=1
                pizzaMatrix=[[True,True],[True,True],[True,True]]
                score=0
                health=genHealth(1)
                kids=[]
                summon(5)
                print(kids)
                if overRest:
                    scoreS.play()
                    stage=1
                if overMenu:
                    scoreS.play()
                    stage=3
        continue
    if stage==2:
        screen.fill((0,0,0))
        #uhh
        drawWall()
        pizzaNew=pg.transform.scale(pizza,(350,350))
        screen.blit(pizzaNew,(100,250))
        pepperoniNew=pg.transform.scale(pepperoni,(350,350))
        sausageNew=pg.transform.scale(sausage,(350,350))
        onionNew=pg.transform.scale(onion,(350,350))
        mushroomNew=pg.transform.scale(mushroom,(350,350))
        oliveNew=pg.transform.scale(olive,(350,350))
        pepperNew=pg.transform.scale(pepper,(350,350))
        if buttons[0]: screen.blit(pepperoniNew,(100,250))
        if buttons[1]: screen.blit(sausageNew,(100,250))
        if buttons[2]: screen.blit(onionNew,(100,250))
        if buttons[3]: screen.blit(mushroomNew,(100,250))
        if buttons[4]: screen.blit(oliveNew,(100,250))
        if buttons[5]: screen.blit(pepperNew,(100,250))

        labels=["Pepperoni","Sausage","Onions","Mushroom","Olives","Peppers"]
        for i in range(len(buttons)):
            j=buttons[i]
            if j: 
                color=(255,255,255)
                fColor=(0,0,255)
            else:
                color=(150,150,150)
                fColor=color
            if i in [0,1]: shift=0
            elif i in [2,3]: shift=1
            else: shift=2
            pg.draw.rect(screen,fColor,pg.Rect(700+i%2*200-10,300+shift*75-5,195,50),2)
            screen.blit(fonts.render(labels[i],False,color,(0,0,0)),(700+i%2*200,300+shift*75))
        column=None
        row=None
        if pg.mouse.get_pos()[0]>675 and pg.mouse.get_pos()[0]<880:
            column=0
        if pg.mouse.get_pos()[0]>880 and pg.mouse.get_pos()[0]<1080:
            column=1
        if pg.mouse.get_pos()[1]>295 and pg.mouse.get_pos()[1]<345:
            row=0
        if pg.mouse.get_pos()[1]>370 and pg.mouse.get_pos()[1]<420:
            row=1
        if pg.mouse.get_pos()[1]>445 and pg.mouse.get_pos()[1]<495:
            row=2
        if pg.mouse.get_pos()[0]>990 and pg.mouse.get_pos()[1]>590 and pg.mouse.get_pos()[1]<650:
            overBack=True
        else: overBack=False
        if overBack:
            screen.blit(fonts.render("< back to menu",(0,0,0),(0,0,255)),(1000,600))
        else:
            screen.blit(fonts.render("< back to menu",(0,0,0),(255,255,255)),(1000,600))

        drawScanlines()
        pg.display.update()
        for e in pg.event.get():
            if e.type==pg.QUIT: exit(0)
            if e.type==pg.MOUSEBUTTONDOWN:
                if column!=None and row!=None:
                    buttons[2*row+column]=not buttons[2*row+column]
                    hitS.play()
                if overBack:
                    scoreS.play()
                    stage=3
        continue
    screen.fill((0,0,0))
    for e in pg.event.get():
        if e.type==pg.QUIT: exit(0)
        if e.type==pg.KEYDOWN and e.key==32 and cooldown<0 and count>0:
            if not flip: pizzas.append([px+64,py+offset,flip])
            else: pizzas.append([px-92,py+offset,flip])
            shootS.play()
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
        if i[0]: 
            screen.blit(pizza,(50,50+off*112))
            if designs[0]: screen.blit(pepperoni,(50,50+off*112))
            if designs[1]: screen.blit(sausage,(50,50+off*112))
            if designs[2]: screen.blit(onion,(50,50+off*112))
            if designs[3]: screen.blit(mushroom,(50,50+off*112))
            if designs[4]: screen.blit(olive,(50,50+off*112))
            if designs[5]: screen.blit(pepper,(50,50+off*112))
        if i[1]: 
            screen.blit(pizza,(50+92+20,50+off*112))
            if designs[0]: screen.blit(pepperoni,(50+92+20,50+off*112))
            if designs[1]: screen.blit(sausage,(50+92+20,50+off*112))
            if designs[2]: screen.blit(onion,(50+92+20,50+off*112))
            if designs[3]: screen.blit(mushroom,(50+92+20,50+off*112))
            if designs[4]: screen.blit(olive,(50+92+20,50+off*112))
            if designs[5]: screen.blit(pepper,(50+92+20,50+off*112))
        if px>50-64 and px<50+92 and py>50+off*112-128 and py<50+off*112+92 and i[0]:
            if count<=6:
                pizzaMatrix[off][0]=False
                count+=1
                collectS.play()
        if px>50-64+92+20 and px<50+2*92+20 and py>50+off*112-128 and py<50+off*112+92 and i[1]:
            if count<=6:
                pizzaMatrix[off][1]=False
                count+=1
                collectS.play()
        off+=1
    #draw pizzas
    n=[]
    for i in range(len(pizzas)):
        j=pizzas[i]
        screen.blit(pizza,(j[0],j[1]))
        if designs[0]: screen.blit(pepperoni,(j[0],j[1]))
        if designs[1]: screen.blit(sausage,(j[0],j[1]))
        if designs[2]: screen.blit(onion,(j[0],j[1]))
        if designs[3]: screen.blit(mushroom,(j[0],j[1]))
        if designs[4]: screen.blit(olive,(j[0],j[1]))
        if designs[5]: screen.blit(pepper,(j[0],j[1]))
        if not j[2]: pizzas[i][0]+=mv
        else: pizzas[i][0]-=mv
        if j[0]>-100 and j[0]<1280:
            if (not (j[0]>590-92 and j[1]>sy-92 and j[1]<sy+128 and j[0]<590+92)) or wave==1:
                n.append(j)
    pizzas=n
    #handle kids
    off=0
    for i in kids:
        if i==fullId and fullIdTimer>0:
            screen.blit(fullKid,(i[0],i[1]))
        else:
            screen.blit(kid,(i[0],i[1]))
        k=len(pizzas)-1
        while k>=0:
            j=pizzas[k]
            if j[0]+92>i[0] and j[1]+92>i[1] and j[1]<i[1]+92 :
                del pizzas[k]
                kids[off][2]-=1
                if kids[off][2]<1:
                    del kids[off]
                    scoreS.play()
                    k-=1
                    score+=100
                    health+=50
                    floatyTodraw.append([j[0]+64,j[1],j[1]-100])
                else:
                    hitS.play()
                    fullId=i
                    fullIdTimer=10
            k-=1
        off+=1
    if len(kids)==0:
        print('b')
        summon(5+m.floor(6*m.log(wave,10)))
        wave+=1
        health=genHealth(wave)
        if wave!=1:
            delC=60*round(1/((wave-1)*2-1))
            vel=0.5*round(7/(1+2.718281828**(-wave+4)))
            delDel=True
            print(delC)
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

    #draw and move shadow freddy
    if wave!=1:
        screen.blit(shadow,(590,sy))
        if delDel:
            if delay>0: delay-=1
            elif delay==0:
                delDel=False
                delay=delC
        else:
            if abs(sy-py)<15: pass
            elif sy>py: sy-=vel
            elif sy<py: sy+=vel
            if sy-vel<py and sy+vel>py: delDel=True
    #draw score text
    temp=[]
    for i in floatyTodraw:
        if not (i[1]<=i[2]):
            temp.append(i)
    floatyTodraw=temp
    for i in range(len(floatyTodraw)):
        j=floatyTodraw[i]
        screen.blit(floaty,(j[0],j[1]))
        if j[1]>j[2]:
            floatyTodraw[i][1]-=3
    #scanlines

    #UI
    text=font.render(f'Score: {score}',True,(255,255,255),(0,0,0))
    screen.blit(text,textRect)
    textRect.right=1280-len(str(score))*12
    #health
    origs=50
    hProc=m.floor((health/genHealth(wave))*100)
    if health>=0:
        for i in range(hProc):
            pg.draw.rect(screen,(255,0,0),pg.Rect(origs+i*10,10,5,20))
    if health<0:
        stage=0

    cooldown-=1
    health-=1
    if panimc%10==0:
        if panimf:
            player=pg.image.load("gfx/player1.png")
            kid=pg.image.load("gfx/kid1.png")
        else:
            player=pg.image.load("gfx/player.png")
            kid=pg.image.load("gfx/kid.png")
        panimf=not panimf
        panimc=0
    panimc+=1
    if fullIdTimer>-100:
        fullIdTimer-=1
    drawScanlines()
    pg.display.update()
    pg.time.Clock().tick(60)
