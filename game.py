import pygame
import math
pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PoNg")

FPS = 60

BLACK = 0, 0, 0
WHITE = 255, 255, 255
PINK = 255, 0, 191
BLUE = 5, 5, 255
RECTANGLE = pygame.Rect(WIDTH - WIDTH//5, HEIGHT - (3*HEIGHT)/4, 300, HEIGHT//2)
RECTANGLE2 = pygame.Rect(1-(WIDTH//4), HEIGHT-(3*HEIGHT)/4, 300, HEIGHT//2)


PADDLE_HEIGHT, PADDLE_WIDTH = 100, 20
BALL_RADIUS = 6

SCORE_FONT = pygame.font.SysFont('monospace', 30, pygame.font.Font.bold)
WINNING_SCORE = 10

# paddle class for paddle definitions and logic
class Paddle:
    COLOR = PINK #paddle color duh
    VEL = 8 #paddle movement velocity

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

######

class Ball:
    MAX_VEL = 8
    COLOR = BLUE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius, width=0)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1



def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK) #bg color

    pygame.draw.line(win, WHITE, (WIDTH//2-5, HEIGHT), (WIDTH//2-5,-HEIGHT)) # middle line

    pygame.draw.circle(win, WHITE, (WIDTH/2 - 5, HEIGHT/2), 50, width=1) # middle circle

    pygame.draw.arc(win, WHITE, RECTANGLE, math.pi/2, (3 * math.pi)/2)
    pygame.draw.arc(win, WHITE, RECTANGLE2, -math.pi/2, -(3 * math.pi)/2)


    left_score_text = SCORE_FONT.render(f'{left_score}', 1, PINK)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, PINK)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)

#    for i in range(10, HEIGHT, HEIGHT//30): #line in the middle
#        if i % 2 == 1:
#            continue
#        pygame.draw.circle(win, WHITE, (WIDTH//2 - 5, i), 2)
#
    ball.draw(win)
    pygame.display.update() #gotta manually update the display to draw stuff

def handle_collision(ball, left_paddle, right_paddle):
    # invert direction of ball after hitting top and bottom of screen, with slight increase of speed
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1.2
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1.2

    if ball.x_vel < 0:
        #left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        #right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_y / reduction_factor
                ball.y_vel = -1 * y_vel


#paddles movement function
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0: #paddle movement and screen limit
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def main():
    run = True
    clock = pygame.time.Clock() #clock to sync the game

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) #paddle size definition
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)#paddle size definition

    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0


# main event loop, while the game is running ('run = True'), else, ('run = False')
    while run:
        clock.tick(FPS) #time sync
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
                right_score += 1
                ball.reset()
        elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = 'Left Player WON!'
        elif right_score >= WINNING_SCORE:
            win_text = 'Right Player WON!'
            won = True

        if won:
            text = SCORE_FONT.render(win_text, 1, PINK)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)

            ball.reset()
            right_paddle.reset()
            left_paddle.reset()

            right_score, left_score = 0, 0


    pygame.quit()

if __name__ == '__main__':
        main()

