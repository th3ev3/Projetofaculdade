#Glossario
# Foguete = ICON SUS
# Inimigos = Virus (Covid)
#laser = vacina

import turtle 
import math
import random
import pygame
import tkinter



pygame.init()
from pygame.mixer import Sound
# criando a tela

turtle.setup(600,600)
wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Batalha contra o Covid-19')
wn.bgpic('fundo.gif')




## Start the game




#registrando as imagens (shapes)
turtle.register_shape('invader.gif')
turtle.register_shape('player.gif')
turtle.register_shape('foguete.gif')
turtle.register_shape('heart.gif')

#criando os sons
explod = pygame.mixer.Sound('explosion.wav')
laser = pygame.mixer.Sound('gota.ogg')
amb = pygame.mixer.music
amb.load('amb.wav')
amb.set_volume(0.2)
amb.play()
laser.set_volume(0.5)
explod.set_volume(0.2)

# desenhando as bordas

caneta = turtle.Turtle()
caneta.speed(0)
caneta.color('white')
caneta.penup()
caneta.setposition(-300, -300)
caneta.pendown()
caneta.pensize(3)
for side in range(4):
    caneta.fd(600)
    caneta.lt(90)
caneta.hideturtle()

#criando e desenhando o score(placar)
score = 0
    #desenhandoo score
scorepen = turtle.Turtle()
scorepen.color('white')
scorepen.speed(0)
scorepen.penup()
scorepen.setposition(-290,275)
    #texto do score + a variavel
scorestring = (f'Covid Abatido = {score}')
scorepen.write(scorestring, False, align = 'left', font = ('Arial', 14,'normal'))
scorepen.hideturtle()

#criando as vidas
n_vida = 3#variavel de controle de vidas, iniciando com 3 vidas
vidas = [] #lista que contem as vidas
for v in range (n_vida):
    vidas.append(turtle.Turtle())
#desenhando as vidas
y=250
for vida in vidas:
    #vida= turtle.Turtle()
    vida.hideturtle()
    vida.color('red')
    vida.shape('heart.gif')
    vida.speed(0)
    vida.penup()
    vida.setposition(-278,y)
    vida.showturtle()
    y-=35
#criando niveis de dificuldade
nivel =1 #variavel de controle de nivel, iniciada em 1
nivelpen = turtle.Turtle()
nivelpen.color('white')
nivelpen.speed(0)
nivelpen.penup()
nivelpen.setposition(200,275)
 #escrevendo o nivel na tela
nivelpen.clear()
nivelstring = f'Nivel: {nivel}'
nivelpen.write(nivelstring,False, align= 'left', font =('Arial',14,'normal'))
nivelpen.ht()

#Criando o player
player = turtle.Turtle()
player.color('blue')
player.shape('player.gif')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 15

#criando os inimigos
n_inimigos = 5 #variavel de controle da quantidade de inimigos em tela
inimigos = [] # lista de inimigos em tela
for i in range (n_inimigos):
    inimigos.append(turtle.Turtle()) 
#preenchendo a lista com inimigos
#dando caracteristicas a todos os inimigos da lista
for inimigo in inimigos:
    inimigo.color('red')
    inimigo.shape('invader.gif')
    inimigo.penup()
    inimigo.speed(0)
    #sorteando a próxima posição de aparição do inimigo
    x = random.randint(-200,200)
    y = random.randint(100,180)
    inimigo.setposition(x,y)

inimigospeed = 5

#criando o foguete do player:

foguete = turtle.Turtle()
foguete.color('yellow')
foguete.shape('foguete.gif')
foguete.penup()
foguete.speed(0)
foguete.setheading(90)
foguete.shapesize(0.25,0.25)
foguete.hideturtle()

foguetespeed=30

#definindo estado do foguete
#pronto = pronto para atirar
#fogo = foguete disparado

estado_foguete = 'pronto'



#funções de movimento do player

def moveesquerda():
    x = player.xcor()
    x-=playerspeed
    if x <-280:
        x=-280
    player.setx(x)
def movedireita():
    x = player.xcor()
    x+=playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def movefrente():
    y = player.ycor()
    y+=playerspeed
    if y >0:
        y=0
    player.sety(y)

def movetras():
    y = player.ycor()
    y-=playerspeed
    if y <-280:
        y=-280
    player.sety(y)    

#função de tiro
def atirar():
    #define o estado_foguete como global
    global estado_foguete
    
    #cuidando para que só atire se já estiver pronto
    if estado_foguete == 'pronto':
        #som do foguete
        laser.play()
        estado_foguete = 'atirando'
        
        #movendo o foguete a partir do player
        x = player.xcor()
        y = player.ycor()+10
        foguete.setposition(x,y)
        foguete.showturtle()

#função que define se existe colisão entre os objetos do jogo (inimigo com player, foguete com inimigo...)
def isCollision(t1,t2):#preferi usar o nome em ingles por convensão, usa se dois argumentos, ou seja os dois objetos que podem ou não colidir.
    #definindo a distancia entre os objetos
    distancia = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distancia <15:
        return True
    else:
        return False
def sair():
    amb.stop()
    turtle.done()
    wn.clear()
    wn.bye()
    
#criando conexões de entrada de teclado

turtle.listen()
turtle.onkey(moveesquerda,'Left')
turtle.onkey(movedireita,'Right')
turtle.onkey(movefrente,'Up')
turtle.onkey(movetras,'Down')
turtle.onkey(atirar,'space')
turtle.onkey(sair,'Escape')

# criando o loop do jogo (maingameloop)

while True: 
   
    #definindo parametros para aumento de nivel
    if score>=100 and score%(100*nivel)==0:
         nivel+=1
         n_inimigos *=nivel
         nivelpen.clear()
         nivelstring = f'Nivel: {nivel}'
         nivelpen.write(nivelstring,False, align= 'left', font =('Arial',14,'normal'))
         nivelpen.ht()
         
         #aumentando os inimigos segundo os níveis
         if len(inimigos)<=30: #limitando o máximo de inimigos em trinta
                 inimigo = turtle.Turtle()
                 inimigo.shape('invader.gif')
                 inimigo.penup()
                 inimigo.speed(0)
                 #sorteando a próxima posição de aparição do inimigo
                 x = random.randint(-200,200)
                 y = random.randint(100,180)
                 inimigo.setposition(x,y)
                 for i in range (nivel):  
                     inimigos.append(inimigo)


    for inimigo in inimigos:        
        #movendo todos os inimigos inimigo:
        x = inimigo.xcor()
        x+=inimigospeed
        inimigo.setx(x)
        if inimigo.xcor() >280:
            for e in inimigos:
                y = e.ycor()
                y-=10
                e.sety(y)
            inimigospeed*=-1

        if inimigo.xcor()<-280:
            for e in inimigos:
                y = e.ycor()
                y-=10
                e.sety(y)
            inimigospeed*=-1

            
            #verificando se há colisão entre foguete e inimigo
        if isCollision(foguete,inimigo):
            #som de explosão do inimigo
            explod.play() 
            #resetando o foguete
            foguete.hideturtle()#tornando o foguete invisivel("destruindo")
            estado_foguete = 'pronto'# mudando estado do foguete pra que possa ser disparado denovo
            foguete.setposition(0,-400)#escondendo para novo tiro
            #resetando o inimigo
            #sorteando a próxima posição de aparição do inimigo
            x = random.randint(-200,200)
            y = random.randint(100,180)
            inimigo.setposition(x,y)
            #atualizando score a cada inimigo abatido:
            score+=10
            scorestring = (f'Covid Abatido= {score}')
            scorepen.clear()
            scorepen.write(scorestring, False, align = 'left', font = ('Arial', 14,'normal'))
            

    
        
        #verificando se o inimigo atingiu o player
        if isCollision(player,inimigo):
               
                if n_vida >0:# tirando a vida até zerar
                    explod.play()
                    #resetando o inimigo
                    #sorteando a próxima posição de aparição do inimigo
                    x = random.randint(-200,200)
                    y = random.randint(100,180)
                    inimigo.setposition(x,y)  
                    n_vida-=1#zerando as vidas
                    vidas[n_vida].ht()
                    
                    
                    continue
                
                else:
                    explod.play()
                    player.hideturtle()
                    inimigo.hideturtle()
                    #criando o texto game over
                    gopen = turtle.Turtle()
                    #criando a caneta que escreverá o texto
                    gopen.speed(0)
                    gopen.color('white')
                    gotext = ('COVID VENCEU!')#texto 
                    gopen.write(gotext, False, align = 'center', font = ('Arial', 38,'bold'))
                    gopen.hideturtle()
                    
                    amb.stop()

               
                    break    

    #movendo o foguete quando atirado
    y = foguete.ycor()
    y+=foguetespeed
    foguete.sety(y)
    
    #verificando se o foguete chegou no extremo da tela,
    #destruindo o e mudando estado do foguete para novo tiro
    if foguete.ycor()>275:
        foguete.hideturtle()
        estado_foguete = 'pronto'
amb.stop()