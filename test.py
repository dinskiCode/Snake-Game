import sys
import pygame

pygame.init()
size = width, height = 750, 750
speed = [0, 1]  # horizontal, vertical
speed_up = [0, -50]
speed_down = [0, 50]
speed_left = [-50, 0]
speed_right = [50, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


class BodyCount:
    id = 1
    bodies = []


class Body:
    def __init__(self, pos):
        self.pos = pos
        self.id = BodyCount.id
        self.img = pygame.image.load("Body.png")
        self.body = self.img.get_rect()
        self.body.x = self.pos[0]
        self.body.y = self.pos[1]
        BodyCount.id += 1
        BodyCount.bodies.append(self)
# head
snake = Body((0, 700))

ball = pygame.image.load("Ball.gif")
ball_rect = ball.get_rect()
ball_rect.x = 250
ball_rect.y = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.body = snake.body.move(speed_down)
            elif event.key == pygame.K_UP:
                if not ball_rect.top < 0:
                    snake.body = snake.body.move(speed_up)
            elif event.key == pygame.K_LEFT:
                new_body = Body((BodyCount.bodies[0].body.x, BodyCount.bodies[0].body.y))
                snake.body = snake.body.move(speed_left)
                for body in BodyCount.bodies:
                    print(body.body.x, body.body.y, " = ", body.id)
            elif event.key == pygame.K_RIGHT:
                snake.body = snake.body.move(speed_right)

    screen.fill((136, 181, 78))
    for body_part in BodyCount.bodies:
        screen.blit(body_part.img, body_part.body)   # blit ?
    pygame.display.flip()   # updates whole screen whereas update(*args) only the args portion of the screen.

