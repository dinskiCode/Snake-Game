import sys
import pygame
import random

pygame.init()
size = width, height = 750, 750
speed_up = [0, -50]     # horizontal, vertical
speed_down = [0, 50]
speed_left = [-50, 0]
speed_right = [50, 0]

screen = pygame.display.set_mode(size)


class BodyCount:
    id = 1
    bodies = []


class Body:
    def __init__(self, pos, is_head=False):
        self.is_head = is_head
        self.pos = pos
        self.id = BodyCount.id
        self.img = pygame.image.load("Body.png")
        self.body = self.img.get_rect()
        self.body.x = self.pos[0]
        self.body.y = self.pos[1]
        BodyCount.id += 1
        BodyCount.bodies.append(self)

    def apple_eaten(self, apple_obj):
        eaten = False
        if self.is_head:
            if self.body.x == apple_obj.body.x and self.body.y == apple_obj.body.y:
                eaten = True
        return eaten

    move_dir = []


class Apple:
    def __init__(self):
        self.pos = [random.randint(1, 13)*50, random.randint(1, 13)*50]
        self.img = pygame.image.load("Apple.png")
        self.body = self.img.get_rect()
        self.body.x = self.pos[0]
        self.body.y = self.pos[1]

    def random_move(self):
        curr_x = self.body.x    # equal to distance from left border
        curr_y = self.body.y    # equal to distance from top border
        x_pos = random.randint((0-curr_x)/50, (700-curr_x)/50)*50
        y_pos = random.randint((0-curr_y)/50, (700-curr_y)/50)*50
        new_pos = [x_pos, y_pos]
        self.body = self.body.move(new_pos)


# head
snake_head = Body((0, 700), True)
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if snake_head.apple_eaten(apple):
                    new_body = Body((BodyCount.bodies[0].body.x, BodyCount.bodies[0].body.y))
                    apple.random_move()
                snake_head.body = snake_head.body.move(speed_down)
            elif event.key == pygame.K_UP:
                if snake_head.apple_eaten(apple):
                    new_body = Body((BodyCount.bodies[0].body.x, BodyCount.bodies[0].body.y))
                    apple.random_move()
                snake_head.body = snake_head.body.move(speed_up)
            elif event.key == pygame.K_LEFT:
                if snake_head.apple_eaten(apple):
                    new_body = Body((BodyCount.bodies[0].body.x, BodyCount.bodies[0].body.y))
                    apple.random_move()
                snake_head.body = snake_head.body.move(speed_left)
            elif event.key == pygame.K_RIGHT:
                if snake_head.apple_eaten(apple):
                    new_body = Body((BodyCount.bodies[0].body.x, BodyCount.bodies[0].body.y))
                    apple.random_move()
                snake_head.body = snake_head.body.move(speed_right)

    screen.fill((136, 181, 78))
    screen.blit(apple.img, apple.body)
    for body_part in BodyCount.bodies:
        screen.blit(body_part.img, body_part.body)   # blit ?

    pygame.display.flip()   # updates whole screen whereas update(*args) only the args portion of the screen.

