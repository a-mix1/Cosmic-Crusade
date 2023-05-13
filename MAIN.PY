import pygame

import os

import time
import random

from pygame import mixer

pygame.init()

width=563
height=474
dis=pygame.display.set_mode((width,height))
name=pygame.display.set_caption("Cosmic Crusade")


red_space_ship=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\enemy1.png'))
green_space_ship=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\enemy2.png'))
blue_space_ship=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\enemy3.png'))

#player 
yellow_space_ship=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\white ship final (1).png'))

laser_red=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\pixel_laser_red.png'))
laser_blue=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\pixel_laser_blue.png'))
laser_green=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\pixel_laser_green.png'))
laser_yellow=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\pixel_laser_yellow.png'))

mixer.music.load('bgmusic.ogg')
mixer.music.play(-1)

back=pygame.image.load((r'C:\Users\tatan\Desktop\COSMIC NEW\space(5).png'))


class Laser:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y+=vel

    def offscreen(self,height):
        return not(self.y<=height and self.y>=0)
    
    def collision(self,obj):
        return collide(self,obj)

class Ship:
    COOLDOWN=30

    def __init__(self, x,y,hp=100):
        self.x=x
        self.y=y
        self.hp=hp
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_count=0
    
    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.hp -= 10
                self.lasers.remove(laser)
        
    def cooldown(self):
        if self.cool_down_count >= self.COOLDOWN:
            self.cool_down_count=0
        elif self.cool_down_count>0:
            self.cool_down_count+=1
            
    def shoot(self):
        if self.cool_down_count==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_count=1
        
            
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()
  
class Player(Ship):##inherting from Ship
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.ship_img=yellow_space_ship
        self.laser_img=laser_yellow
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_hp=hp

    def move_laser(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.offscreen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def shoot(self):
        if self.cool_down_count==0:
            laser=Laser(self.x+39,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_count=1
    
    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x , self.y + self.ship_img.get_height()-25, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height()-25, self.ship_img.get_width() * (self.hp/self.max_hp),5))
    
    
    

class Enemy(Ship):
    color_map={
        "red" : (red_space_ship,laser_red),
        "green" : (green_space_ship,laser_green),
        "blue" : (blue_space_ship,laser_blue)
    }
    def __init__(self, x, y,color, hp=100):
        super().__init__(x, y, hp)
        self.ship_img,self.laser_img=self.color_map[color]
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y+=vel

    def shoot(self):
        if self.cool_down_count==0:
            laser=Laser(self.x-17.5,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_count=1
    
def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None 


        
def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    lost=False
    lost_count=0
    main_font=pygame.font.SysFont("resolve-sans-w05-blk-exntended",16)
    lost_font=pygame.font.SysFont("resolve-sans-w05-blk-exntended",30)
    
    enemies=[]
    wavelength=5
    enemy_vel=0.8
    player_vel=6
    laser_vel=5
    player=Player(225,380)
    clock= pygame.time.Clock()
    def redrawindow():
        dis.blit(back,(0,0))
        lives_label=main_font.render(f"Lives: { lives}",1,(249,213,0))
        level_label=main_font.render(f"Level: { level}",1,(249,213,0))
        dis.blit(lives_label,(10,10))
        dis.blit(level_label,(width-level_label.get_width()-10,10))

        for enemy in enemies:
            enemy.draw(dis)
        player.draw(dis)

        if lost==True:
            lost_label=lost_font.render("You LOSE :( ",1,((255,0,0)))
            dis.blit(lost_label,(width/2-lost_label.get_width()/2,243))
        pygame.display.update() 

    while run :
       clock.tick(fps)

       redrawindow() 

       if lives<=0 or player.hp<=0:
           lost=True
           lost_count+=1
                     
       if lost:
           if lost_count>fps*3:
             run = False
           else:
             continue
       
       if len(enemies)==0:
           level+=1
           wavelength+=5
           for i in range(wavelength):
               enemy=Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(["red","green","blue"]))
               enemies.append(enemy)
               
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               quit()
               sys.exit()

       keys=pygame.key.get_pressed()
       if keys[pygame.K_a]and player.x-player_vel>0:
           player.x -= player_vel
       if keys[pygame.K_d]and player.x+player_vel+player.get_width()<width:
           player.x += player_vel
       if keys[pygame.K_w] and player.y-player_vel>0:
           player.y -= player_vel
       if keys[pygame.K_s] and player_vel+player.y+player.get_height()<height:
           player.y += player_vel
       if keys[pygame.K_SPACE] and player_vel+player.y<height:
           player.shoot()
       
       for enemy in enemies[:]:
           enemy.move(enemy_vel)  
           enemy.move_laser(laser_vel,player)

           if random.randrange(0,120)==1:
               enemy.shoot()  
           if collide(enemy,player):
              player.hp-=10
              enemies.remove(enemy)
                
           elif enemy.y+enemy.get_height()>height:
               lives-=1
               enemies.remove(enemy)

       player.move_laser(-laser_vel,enemies)
       
       
def menu1():
    title_font = pygame.font.SysFont("resolve-sans-w05-blk-exntended", 24)
    title_font1 = pygame.font.SysFont("resolve-sans-w05-blk-exntended", 16)
    ins_font1=    pygame.font.SysFont("resolve-sans-w05-blk-exntended", 16)
    ins_font2=    pygame.font.SysFont("resolve-sans-w05-blk-exntended", 16)


    run=True
    while run:
        dis.blit(back,(0,0))
        title_label = title_font.render("Cosmic Crusade", 1, (249,213,0))
        title_label1 = title_font1.render("Left Click to begin", 1, (249,213,0))
        ins_label1 = ins_font1.render("Controls: w-a-s-d to move", 1, (249,213,0))
        ins_label2 = ins_font2.render("Space to shoot", 1, (249,213,0))
        dis.blit(title_label, (width/2 - title_label.get_width()/2, 223))
        dis.blit(title_label1, (width/2 - title_label1.get_width()/2, 250))
        dis.blit(ins_label1, (width/2 - title_label1.get_width()/2-60, 273))
        dis.blit(ins_label2, (width/2 - title_label1.get_width()/2, 293))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()   


menu1()
