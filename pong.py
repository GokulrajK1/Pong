import pygame 
import random

pygame.init()

# Constants 
WIDTH, HEIGHT = 1000, 800
BLACK = (0, 0, 0)
FPS = 60
SPT_XPOS = WIDTH / 8
MPT_XPOS = (7*(WIDTH) / 8) - 225
OG_SPT_XPOS = SPT_XPOS
OG_MPT_XPOS = MPT_XPOS
SCORE_TO_WIN = 5
PADDLE_Y = (HEIGHT - 100) / 2

# Creating window 
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Corbel", 50)
pygame.display.set_caption("PONG")


# Class for a paddle object 
class Paddle:
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y 
        self.ogX = x
        self.ogY = y
        self.width = width 
        self.height = height 
        self.vel = 5
        self.color = (255,255,255)
        self.score = 0

    def drawPaddle(self, win):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, rect)

    def movePaddle(self, singlePlayerMode=True, paddleID=1, ball=None):
        keys_pressed = pygame.key.get_pressed()
        if paddleID == 1:
            if keys_pressed[pygame.K_w] and self.y > 0:
                self.y -= self.vel
            if keys_pressed[pygame.K_s] and self.y + self.height < HEIGHT:
                self.y += self.vel
        elif paddleID == 2 and singlePlayerMode == False:
            if keys_pressed[pygame.K_UP] and self.y > 0:
                self.y -= self.vel
            if keys_pressed[pygame.K_DOWN] and self.y + self.height < HEIGHT:
                self.y += self.vel
        else:
            if ball.x > (WIDTH / 4) and ball.velX > 0:
                if ball.y < self.y and self.y > 0:
                    self.y -= self.vel
                elif ball.y + ball.width > self.y + self.height and (self.y + self.height) < HEIGHT:
                    self.y += self.vel

# Class for a ball object                 
class Ball:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.ogX = x
        self.ogY = y
        self.width = width 
        self.velX = -6
        self.velY = 0
        self.color = (255,0,0)

    def drawBall(self, win):
        rect = pygame.Rect(self.x, self.y, self.width, self.width)
        pygame.draw.rect(win, self.color, rect)

    def moveBall(self, gameStart, paddle1, paddle2, singlePlayerText, multiPlayerText):
        if self.y <= 0 or self.y >= HEIGHT:
            self.velY *= -1
        if self.x < 0 or self.x > WIDTH:
            if self.velX > 0:
                paddle1.score += 1
            else:
                paddle2.score += 1
            self.x = (WIDTH / 2) - (self.width / 2)
            self.y = HEIGHT / 2
            paddle1.y = PADDLE_Y
            paddle2.y = PADDLE_Y
            self.velX = -6
            self.velY = 0

            updateDisplay(paddle1, paddle2, self, singlePlayerText, multiPlayerText)
            pygame.time.wait(1000)

        self.x += self.velX
        self.y += self.velY

# Main game loop 
def main (): 
    run = True 
    clock = pygame.time.Clock()
    global gameStarted
    gameStarted = False
    singlePlayerMode = False

    global SPT_XPOS
    global MPT_XPOS

    paddle1 = Paddle(50, PADDLE_Y, 25, 100)
    paddle2 = Paddle(WIDTH - 50 - 25, PADDLE_Y, 25, 100)
    ball = Ball((WIDTH / 2) - (15/2), (HEIGHT / 2) - 15, 15)
   
    singlePlayerText = font.render("Singleplayer", True, (255,255,255))
    multiPlayerText = font.render("Multiplayer", True, (255, 255, 255))
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseHover(singlePlayerText, SPT_XPOS):
                    gameStarted = True
                    singlePlayerMode = True
                elif mouseHover(multiPlayerText, MPT_XPOS):
                    gameStarted = True
                    singlePlayerMode = False

        if gameStarted == True:
            singlePlayerText = font.render(str(paddle1.score), True, (255, 255, 255))
            multiPlayerText = font.render(str(paddle2.score), True, (255, 255, 255))
            SPT_XPOS = (WIDTH / 4) - 20
            MPT_XPOS = (3*(WIDTH / 4)) 

            paddle1.movePaddle()
            paddle2.movePaddle(singlePlayerMode, 2, ball)
            ball.moveBall(True, paddle1, paddle2, singlePlayerText, multiPlayerText)
            collisions(paddle1, ball)
            collisions(paddle2, ball)

            if paddle1.score == SCORE_TO_WIN or paddle2.score == SCORE_TO_WIN:
                singlePlayerText = font.render(str(paddle1.score), True, (255, 255, 255))
                multiPlayerText = font.render(str(paddle2.score), True, (255, 255, 255))
                updateDisplay(paddle1, paddle2, ball, singlePlayerText, multiPlayerText)
                pygame.time.wait(2000)
                paddle1.x = paddle1.ogX
                paddle1.y = paddle1.ogY
                paddle2.x = paddle2.ogX
                paddle2.y = paddle2.ogY
                ball.x = ball.ogX
                ball.y = ball.ogY
                gameStarted = False
                singlePlayerText = font.render("Singleplayer", True, (255, 255, 255))
                multiPlayerText = font.render("Multiplayer", True, (255, 255, 255))
                SPT_XPOS = OG_SPT_XPOS
                MPT_XPOS = OG_MPT_XPOS
                paddle1.score, paddle2.score = 0, 0
                updateDisplay(paddle1, paddle2, ball, singlePlayerText, multiPlayerText)

        else:
            if mouseHover(singlePlayerText, SPT_XPOS):
                singlePlayerText = font.render("Singleplayer", True, (255, 0, 0))
            else:
                singlePlayerText = font.render("Singleplayer", True, (255, 255, 255))

            if mouseHover(multiPlayerText, MPT_XPOS):
                multiPlayerText = font.render("Multiplayer", True, (255, 0, 0))
            else:
                multiPlayerText = font.render("Multiplayer", True, (255, 255, 255))

        updateDisplay(paddle1, paddle2, ball, singlePlayerText, multiPlayerText)

    pygame.quit()

# Checks to see if mouse is hovering over a text box 
def mouseHover(text, xPos):
    width = text.get_width()
    mousePos = pygame.mouse.get_pos()
    if xPos <= mousePos[0] <= xPos + width:
        if 30 <= mousePos[1] <= 65:
            return True

# Checks for ocllisions 
def collisions (paddle, ball):
    ballX = ball.x if ball.velX < 0 else ball.x + ball.width 
    if paddle.x <= ballX <= paddle.x + paddle.width:
        if paddle.y <= ball.y <= paddle.y + paddle.height:
            ball.velX *= -1
            paddleCenter = paddle.y + (paddle.height / 2)
            zone = abs(ball.y - paddleCenter)
            if zone < paddle.height / 4:
                ball.velY = random.randrange(-4, 4) 
            else:
                ball.velY = random.randrange(-8, 8)   

# Updates display with new graphics 
def updateDisplay(paddle1, paddle2, ball, singlePlayerText, multiPlayerText):
    win.fill(BLACK)
    pygame.draw.rect(win, (255, 255, 255), ((WIDTH / 2) - 7.5, 0, 15, HEIGHT))
    paddle1.drawPaddle(win)
    paddle2.drawPaddle(win)
    ball.drawBall(win)
    win.blit(singlePlayerText, (SPT_XPOS, 30))
    win.blit(multiPlayerText, (MPT_XPOS, 30))
    pygame.display.update()

main()
