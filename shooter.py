import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
song_dir = path.join(path.dirname(__file__), 'song')

height=600
width=1200
fps=60 #frames per second how many time screen update
POWERUP_TIME = 5000

white=(255,255,255)
black=(0,0,0)
green=(0, 255, 0)
yellow=(255,255,0)
red=(255, 0,0)


pygame.init() # initialize pygame
pygame.mixer.init() # sound
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("shooter game") # heading
clock = pygame.time.Clock() # track time how we going fast

font_name= pygame.font.match_font('arial') # font for text

def draw_text(surf, text, size, x, y): # to draw text on screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
                               
def newenemy(): # to create new enemy
    m= Enemy()
    all_sprites.add(m)
    enemys.add(m)
    
def draw_shield_bar(surf,x,y,pct): #shield of shooter
    if pct < 0:
        pct=0
    bar_length = 100
    bar_height= 10
    fill = (pct/100)* bar_length
    outline_rect = pygame.Rect(x,y,bar_length,bar_height)
    fill_rect= pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf, green,fill_rect)
    pygame.draw.rect(surf,white,outline_rect,2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

        
class Shooter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(shooter_img,(70,50))
        self.image.set_colorkey(black)  # to remove background
        #self.image = pygame.Surface((50,50)) #shooter size
        # self.image.fill((black)) #shooter color
        
        self.rect= self.image.get_rect()
        self.radius= 20
        #self.radius= int(self.rect.width*.7 /2)
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        #center
        self.rect.centerx= width / 2
        self.rect.bottom= height - 10
        self.speedx =0 # speed to move rectangle
        self.shield = 100
        self.shoot_delay= 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
    def update(self):
         # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10
            
        self.speedx =0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]: # if press left key
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:# if press right key
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx # speed to move rectangle
        if self.rect.right > width:# touch right size
            self.rect.right = width
        if self.rect.left < 0: # touch left side
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    def shoot(self):
        now=pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot= now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top) # from where bullet fire
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori= random.choice(enemy_img)
        #self.image_ori=pygame.transform.scale(enemy_img,(40,30))
        self.image_ori.set_colorkey(black) # to remove background
        self.image= self.image_ori.copy()
        #self.image = pygame.Surface((30,40)) #enemy size
        #self.image.fill((white)) #enemy color
        self.rect= self.image.get_rect()
        
        self.radius= int(self.rect.width*.85 /2)
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        
        self.rect.x = random.randrange(width - self.rect.width) # from where enemy come
        #self.rect.y = random.randrange(-150, -100) # spreed
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(1,8) # speed of enemy some slow some fast
        self.speedx = random.randrange(-3,3) #diagonaly
        self.rot= 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

        
    def rotate(self): # rotate the enemy
        now= pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot= (self.rot + self.rot_speed)% 360
            new_image =pygame.transform.rotate(self.image_ori,self.rot)
            old_center = self.rect.center
            self.image= new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width +20:  # if enemy don't get shoot
            self.rect.x = random.randrange(width - self.rect.width) # from where enemy come
            self.rect.y = random.randrange(-100, -40) # spreed
            self.speedy = random.randrange(1,8) # speed of enemy some slow some fast

            #self.rot=0 # rotation
            #self.rot_speed = random.randrange(-8,8)
            #self.last_update= pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        #self.image=pygame.transform.scale(bullet_img,(10,20))
        self.image.set_colorkey(black)  # to remove background
      
        #self.image = pygame.Surface((10,20)) #bullet size
        #self.image.fill((yellow)) #enemy color
        self.rect= self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > height:
            self.kill()
            
class Explosion(pygame.sprite.Sprite): # explosion
    def __init__(self,center ,size):
        pygame.sprite.Sprite.__init__(self)
        self.size= size
        self.image = explosion_anim[self.size][0]
        self.rect= self.image.get_rect()
        self.rect.center= center
        self.frame= 0
        self.last_update= pygame.time.get_ticks()
        self.frame_rate= 50

    def update(self):
        now= pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update= now
            self.frame +=1
            if self.frame== len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect= self.image.get_rect()
                self.rect.center= center
    
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Shooterrrrrr!", 64, width / 2, height / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
        
background = pygame.image.load(path.join(img_dir,"space1.jpg")).convert() #background image
background_rect= background.get_rect()

shooter_img= pygame.image.load(path.join(img_dir,"player.png")).convert()
shooter_mini_img=pygame.transform.scale(shooter_img,(25,19))
shooter_mini_img.set_colorkey(black)
#enemy_img= pygame.image.load(path.join(img_dir,"meteorbig.png")).convert()
bullet_img= pygame.image.load(path.join(img_dir,"laserRed.png")).convert()
enemy_img = []
list= ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
        'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
        'meteorBrown_tiny1.png']
for img in list:
    enemy_img.append(pygame.image.load(path.join(img_dir,img)).convert())

#for explosion
explosion_anim={}
explosion_anim['lg']=[]
explosion_anim['sm']=[]
explosion_anim['shooter']=[]
for i in range(9):
    filename ='regularExplosion0{}.png'.format(i)
    img=pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_lg)
    
    filename ='sonicExplosion0{}.png'.format(i)
    img =pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)

    explosion_anim['shooter'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

    
shoot_sound = pygame.mixer.Sound(path.join(song_dir, 'Shoot.wav'))

all_sprites= pygame.sprite.Group()

enemys= pygame.sprite.Group()

bullets = pygame.sprite.Group()



# game loop
game_over = True
running =True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemys = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        shooter = Shooter()
        all_sprites.add(shooter) # add shooter to sprite
        for i in range(8):
            newenemy()

        score=0
    clock.tick(fps) # keep loop running at the right time/ speed
    #process input(events)
    for event in pygame.event.get(): # action for event happen
        if event.type == pygame.QUIT: # check for closing window
            running = False

       
    #update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemys, bullets,True, True)# bullet hits enemy
    for hit in hits:
        score += 50 - hit.radius # score
        expl= Explosion(hit.rect.center,'lg') #explosion
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newenemy()
        
    
    hits = pygame.sprite.spritecollide(shooter,enemys, True, pygame.sprite.collide_circle) # if enemy touch shooter
    for hit in hits:
        shooter.shield -= hit.radius *2
        expl= Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        newenemy()
        
        if shooter.shield <=0:
            
            death_expl= Explosion(hit.rect.center,'shooter') #explosion
            all_sprites.add(death_expl)
            shooter.hide()
            shooter.lives -= 1
            shooter.shield = 100
    hits = pygame.sprite.spritecollide(shooter, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
            
    if shooter.lives == 0 and not death_expl.alive(): #life
        game_over = True
    
    #Draw
    screen.fill(green)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score), 18, width/2, 10)

    draw_shield_bar(screen,5,5, shooter.shield)
    draw_lives(screen, width - 100, 5, shooter.lives, shooter_mini_img)
    #after drawing everything flip the display
    pygame.display.flip()
pygame.quit() # to end game to terminate window
