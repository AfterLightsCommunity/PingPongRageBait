
from pygame import *

# Window settings
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")

# Colours
BACKGROUND = (51, 0, 0)
WHITE = (192, 192, 192)
BLACK = (0, 0, 0)
GREEN = (102, 0, 102)
RED = (255, 0, 0)

# Font
font.init()
gameFont = font.SysFont("Arial", 50)

# Parent class
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect)


# Paddle class
class Paddle(GameSprite):
    def update(self, up_key, down_key):
        keys = key.get_pressed()

        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[down_key] and self.rect.bottom < win_height:
            self.rect.y += self.speed


# Create paddles
left_paddle = Paddle(30, 200, 20, 100, 6)
right_paddle = Paddle(650, 200, 20, 100, 6)

# Ball
ball = Rect(340, 240, 20, 20)
ball_speed_x = 5
ball_speed_y = 4

# Game settings
clock = time.Clock()
FPS = 60

finish = False
W = ""

game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False

    if finish == False:

        # Move paddles
        left_paddle.update(K_w, K_s)
        right_paddle.update(K_UP, K_DOWN)

        # Move ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Bounce off top and bottom
        if ball.top <= 0:
            ball.top = 0
            ball_speed_y *= -1

        if ball.bottom >= win_height:
            ball.bottom = win_height
            ball_speed_y *= -1

        # Bounce off left paddle
        if ball_speed_x < 0 and ball.colliderect(left_paddle.rect):
            ball.left = left_paddle.rect.right
            ball_speed_x *= -1

        # Bounce off right paddle
        if ball_speed_x > 0 and ball.colliderect(right_paddle.rect):
            ball.right = right_paddle.rect.left
            ball_speed_x *= -1

        # Losing condition
        if ball.right < 0:
            W = "Right player W"
            finish = True

        if ball.left > win_width:
            W = "Left player W"
            finish = True

    # Draw background
    window.fill(BACKGROUND)

    # Draw paddles
    draw.rect(window, WHITE, left_paddle.rect)
    draw.rect(window, BLACK, left_paddle.rect, 4)

    draw.rect(window, WHITE, right_paddle.rect)
    draw.rect(window, BLACK, right_paddle.rect, 4)

    # Draw ball
    draw.ellipse(window, GREEN, ball)
    draw.ellipse(window, BLACK, ball, 2)

    # Display winner
    if finish:
        result = gameFont.render(W, True, RED)
        window.blit(
            result,
            (win_width // 2 - result.get_width() // 2, 220)
        )

    display.update()
    clock.tick(FPS)

quit()
