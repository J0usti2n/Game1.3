#_Imports________________________________________________________________
import pygame, os, random
from pygame.constants import KEYDOWN
pygame.init()
#_Classes________________________________________________________________
#-Settings---------------------------------------------------------------
class Settings(object):
    # Window
    title                           = "Game Project"
    width, height, bordersize, fps  = 1000, 700, 5, 60
    # Filepath
    file_path   = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "Pictures")
    # Game options
    score, paused = 0, False

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)
#-Car--------------------------------------------------------------------
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # load image
        self.image          = pygame.image.load(os.path.join(Settings.images_path, "Car.png")).convert_alpha()
        self.image          = pygame.transform.scale(self.image, (130, 50))
        # hitbox & spawn
        self.rect           = self.image.get_rect()
        self.rect.left      = (Settings.width   - self.rect.width)      // 2
        self.rect.bottom    = (Settings.height  - Settings.bordersize)
        # movement
        self.direction, self.direction_y      = 0, 0
        self.speed          = 5
    #-Update-------------------------------------------------------------
    def update(self):
        self.rect.left  += (self.direction * self.speed)
        self.rect.top   += (self.direction_y * self.speed)
        # move x
        if self.rect.right >= Settings.width:
            self.direction = 0
        elif self.rect.left <= Settings.bordersize:
            self.direction = 0
        # move y
        elif self.rect.bottom >= Settings.height - Settings.bordersize:
            self.direction_y = 0
        elif self.rect.top >= Settings.height - Settings.bordersize:
            self.direction_y = 0
#-Enemy------------------------------------------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # size
        self.x = random.randint(30, 60)
        self.y = self.x
        # load image
        self.image = pygame.image.load(os.path.join(Settings.images_path, "Flux Capacitor.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.x, self.y))
        # hitbox & spawn
        self.rect       = self.image.get_rect()
        self.rect.left  = random.randint(0 + Settings.bordersize, Settings.width)
        self.rect.bottom = Settings.bordersize + 10
        # movement
        self.direction_y    = 1
        self.speed          = random.randint(3, 6)
    #-Update-------------------------------------------------------------
    def update(self):
        self.rect.top    += (self.direction_y * self.speed)
        # score
        if self.rect.top >= Settings.height:
            Settings.score += 1
            self.kill()
#-Game-------------------------------------------------------------------
class Game(object):
    def __init__(self):
        # window
        pygame.display.set_caption(Settings.title)
        self.screen             = pygame.display.set_mode(Settings.get_dim())
        # background
        self.background         = pygame.image.load(os.path.join(Settings.images_path, "background.png")).convert()
        self.background         = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect    = self.background.get_rect()
        # font
        self.font, self.color   = pygame.font.SysFont("Arial", 22, True, False), (255, 255, 255)
        # car
        self.all_cars, self.car     = pygame.sprite.Group(), Car()
        self.all_cars.add(self.car)
        # enemys
        self.all_enemys = pygame.sprite.Group()
        # Game
        self.clock       = pygame.time.Clock()
        self.done        = False
        self.speed       = 2
        self.dropcounter = 100
    #-create-enemys---------------------------------------------------
    def create(self):
        for i in range(6):
            self.enemy      = Enemy()
            self.all_enemys.add(self.enemy)
            self.dropcounter = 0
    #-show-on-display-------------------------------------------------
    def show(self):
        # fps
        self.clock.tick(Settings.fps)
        # draw objects
        self.all_cars.draw(self.screen), self.all_enemys.draw(self.screen)
        self.all_cars.update(), self.all_enemys.update()
        # render
        self.render = self.font.render(str(Settings.score), True, self.color)
        pygame.display.flip(), self.screen.blit(self.background, self.background_rect), self.screen.blit(self.render, (10, 10))
    #-Run-Game--------------------------------------------------------
    def run(self):
        while not self.done:
            self.show()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                #-Options---------------------------------------------
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        Settings.paused = True
                        print("Game paused")
                    elif event.key == pygame.K_u:
                        Settings.paused = False
                        print("Game unpaused")
                if Settings.paused == False:
                    if event.type == KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit()
                        elif event.key == pygame.K_PLUS:
                            self.speed += 0.5
                            print("Increasing speed:", self.speed) 
                            if self.speed >= 10:
                                self.speed = 10
                                print("Max speed reached")
                        elif event.key == pygame.K_MINUS:
                            self.speed -= 0.5
                            print("Decreasing speed:", self.speed)
                            if self.speed <= 0.5:
                                self.speed = 0.5
                                print("Min speed reached")
                #-Movement--------------------------------------------
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.car.direction -= self.speed
                            elif event.key == pygame.K_RIGHT:
                                self.car.direction += self.speed
                            elif event.key == pygame.K_UP:
                                self.car.direction_y -= self.speed
                            elif event.key == pygame.K_DOWN:
                                self.car.direction_y += self.speed
                            elif event.key == pygame.K_SPACE:
                                self.car.rect.left = random.randint(Settings.bordersize, 1000 - Settings.bordersize - self.car.rect.right)
                                self.car.rect.bottom = random.randint(Settings.bordersize, 700 - Settings.bordersize - self.car.rect.top)
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.car.direction = 0
                        elif event.key == pygame.K_RIGHT:
                            self.car.direction = 0
                        elif event.key == pygame.K_UP:
                            self.car.direction_y = 0
                        elif event.key == pygame.K_DOWN:
                            self.car.direction_y = 0
                        elif event.key == pygame.K_SPACE:
                            self.car.direction, self.car.direction_y  = 0, 0
            #-Count-Up------------------------------------------------
            if self.dropcounter >= 100:
                self.create()
            elif Settings.paused == True:
                # When paused, the counter is supposed to not count up
                pass
            else: 
                self.dropcounter += 1
#_Execute________________________________________________________________
if __name__ == '__main__':
    print("Game is running")
    game = Game()
    game.run(), pygame.quit()
    print("Game has stopped")