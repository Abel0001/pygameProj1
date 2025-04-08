import pygame

from enum import Enum

pygame.init()
screen = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
clock = pygame.time.Clock()
gameObjects = {}
diedGameObjects = {}
defaultRenderGroup = pygame.sprite.Group()
running = True



frame = screen.get_rect()


#Assets
ASSETS_PATH = "./assets/"
IMAGE_ASSESTS_PATH = ASSETS_PATH + "images/"

globalImageAssets = {}
currLevelImageAssets = {}
ballImg = pygame.image.load(IMAGE_ASSESTS_PATH + "level1/ball.png")
ballImg = ballImg.convert_alpha()

#Player
playerSpeed = 10

class BaseColors(Enum):
        RED = "red"
        YELLOW = "yellow"
        BLACK = "black"
        BEIGE = "beige"

class TextureType(Enum):
        COLOR, IMAGE = range(2)



def LoadImageAssets(levelName, isGlobal = False):
        pass
class GameObject(pygame.sprite.Sprite):
        def __init__(self, objectList:dict, id,texture, x = screen.get_width()/2, y = screen.get_height()/2, rectWidth = 50, rectHeight = 50,textureType = TextureType.COLOR, renderGroup = defaultRenderGroup, deathObjectList:dict = diedGameObjects):
                super().__init__()
                self.x = x
                self.y = y
                
                self.renderGroup = renderGroup
                self.rect = pygame.Rect(x,y,rectWidth,rectHeight)
                self.textureType = textureType
                self.texture = texture
                self.renderGroup.add(self)
                self.image = pygame.Surface((self.rect.width, self.rect.height))
                self.deathObjectList = deathObjectList
                if textureType == TextureType.COLOR:
                        if texture is None:
                                self.texture = "black"
                        self.image.fill(self.texture)
                elif textureType == TextureType.IMAGE:
                        if texture is None:
                                raise Exception("Missing texture")
                        if not isinstance(texture, pygame.Surface):
                                raise TypeError("Image texture is not a surface")
                        self.image = pygame.transform.scale(texture, (self.rect.width, self.rect.height))

                if(id in objectList):
                        raise Exception("Object already exists")
                else:
                        objectList[id] = self
                        self.id = id
                        self.objectList = objectList
        def render(self):
               screen.blit(self.image, self.rect)
        def Move(self, newX, newY, checkBorderCollision = True):
                if(checkBorderCollision):
                        if(newX < 0): newX = 0
                        if(newX > screen.get_width() - self.rect.width): newX = screen.get_width() - self.rect.width
                        if(newY < 0): newY = 0
                        if(newY > screen.get_height() - self.rect.height): newY = screen.get_height() - self.rect.height
                self.x = newX
                self.y = newY
        def update(self):
                self.rect.x = self.x
                self.rect.y = self.y
        def updateTexture(self, textureType, texture):
                self.texture = texture
                self.textureType = textureType
                if textureType == TextureType.COLOR:
                        
                        self.image.fill(self.texture)
                elif textureType == TextureType.IMAGE:
                        if texture is None:
                                raise Exception("Missing texture")
                        if not isinstance(texture, pygame.Surface):
                                raise TypeError("Image texture is not a surface")
                        self.image = pygame.transform.scale(texture, (self.rect.width, self.rect.height))
        def Destroy(self):
                self.objectList.pop(self.id, None)
                self.deathObjectList.pop(self.id, None)
                self.kill()
                
                


        
class Entity(GameObject):
        def __init__(self,*args,maxHealth = 100, currHealth = 100, renderHealth = True, **kwargs):
                super().__init__(*args, **kwargs)
                self.maxHealth = maxHealth
                self.currHealth = currHealth
                self.lastTime = 0
                self.isAlive = True
                self.isVisible = True
        def SetMaxHealth(self,maxHealth):
                self.maxHealth = maxHealth
                self.RenderHealthBar()
        def SetCurrHealth(self, newHealth):
                self.currHealth = newHealth
                if(self.currHealth <= 0):
                        self.OnDeath()
                        return
                if(self.currHealth > self.maxHealth): self.currHealth = self.maxHealth
                        
                self.RenderHealthBar()
        def Attack(self, target:'Entity', damage):
                target.SetCurrHealth(target.currHealth - damage)
        def RenderHealthBar(self):
                self.currHealth = self.currHealth
        def OnDeath(self):
                
                if(self.isAlive and self.isVisible):
                        self.SetMaxHealth(0)
                        self.isAlive = False
                        self.objectList.pop(self.id)
                        self.objectList = self.deathObjectList
                        self.objectList[self.id] = self
        
        def DeathAnimation(self):
                if(self.isVisible and not self.isAlive):
                        now = pygame.time.get_ticks()
                        if(self.lastTime == 0):
                                self.updateTexture(TextureType.COLOR, "red")
                                self.lastTime = now
                        if(now - self.lastTime) >= 3000:
                                self.isVisible = False
                                self.lastTime = now
                                self.Destroy()
                

                                


class Player(Entity):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        def MoveControl(self, deltaTime, keysPressed, moveSpeed):
                if(keysPressed[pygame.K_w]):
                        self.Move(self.x,self.y - moveSpeed*deltaTime*10)
                if(keysPressed[pygame.K_s]):
                        self.Move(self.x,self.y + moveSpeed*deltaTime*10)
                if(keysPressed[pygame.K_d]):
                        self.Move(self.x + moveSpeed*deltaTime*10,self.y)
                if(keysPressed[pygame.K_a]):
                        self.Move(self.x - moveSpeed*deltaTime*10,self.y)

                


player = Player(gameObjects, 0, "yellow")
object1 = Entity(gameObjects, 1, "black", 300,300)
object2 = GameObject(gameObjects, 2, "black", 30, 30)
ball = GameObject(gameObjects, 3,ballImg ,100,100, textureType= TextureType.IMAGE)



object1.SetCurrHealth(0)
print(1)



        
while running:
        dt = clock.tick() / 1000
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                if event.type == pygame.KEYDOWN:
                        pass
                        if event.key == pygame.K_ESCAPE:
                                running = False
                if event.type == pygame.VIDEORESIZE:
                        screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        keysPressed = pygame.key.get_pressed()

        
        for diedEntity in list(diedGameObjects.values()):
                diedEntity.DeathAnimation()

        player.MoveControl(dt, keysPressed, playerSpeed)
        screen.fill("beige")


        defaultRenderGroup.draw(screen)
        defaultRenderGroup.update()
        

        pygame.display.flip()

        
pygame.quit()
pygame.display.quit()