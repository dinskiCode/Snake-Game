import sys
import pygame
import random


pygame.init()
size = width, height = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
bg = pygame.image.load("Background.png")    # TODO: Background
bg_rect = bg.get_rect()


class Scoreboard:
    score = 0
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Your Score: " + str(score), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=600)


class BodyCount:
    id = 1
    bodies = []
    head_pos = []


class Body:
    speed_up = [0, -50]  # horizontal, vertical
    speed_down = [0, 50]
    speed_left = [-50, 0]
    speed_right = [50, 0]

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

    move_dir = None


class Apple:
    def __init__(self):
        self.pos = [random.randint(1, 13)*50, random.randint(1, 13)*50]
        self.img = pygame.image.load("Apple.png")
        self.body = self.img.get_rect()
        self.body.x = self.pos[0]
        self.body.y = self.pos[1]

    def random_spawn(self):  # TODO: new_pos might be in a field that currently contains a part of snake body
        curr_x = self.body.x    # equal to distance from left border
        curr_y = self.body.y    # equal to distance from top border
        x_pos = random.randint((0-curr_x)/50, (700-curr_x)/50)*50
        y_pos = random.randint((0-curr_y)/50, (700-curr_y)/50)*50
        new_pos = [x_pos, y_pos]
        self.body = self.body.move(new_pos)


# head
snake_head = Body((0, 700), True)
apple = Apple()


def move_forward():
    body_nr = 1
    for b in BodyCount.bodies[1::]:
        b.body = b.body.move(BodyCount.head_pos[len(BodyCount.head_pos) - 1 - body_nr][0] - BodyCount.bodies[body_nr].body.x,
                             BodyCount.head_pos[len(BodyCount.head_pos) - 1 - body_nr][1] - BodyCount.bodies[body_nr].body.y)
        body_nr += 1


started = False
ms = 0
milliseconds_since_last_event = 0

while True:
    # print(milliseconds_since_last_event/1000)
    if started:
        ms = clock.tick()
    milliseconds_since_last_event += ms

    if snake_head.apple_eaten(apple):
        new_body = Body((BodyCount.head_pos[len(BodyCount.head_pos) - len(BodyCount.bodies)][0],
                         BodyCount.head_pos[len(BodyCount.head_pos) - len(BodyCount.bodies)][1]))
        apple.random_spawn()
        Scoreboard.score += 1
        Scoreboard.text = text = Scoreboard.font.render("Your Score: " + str(Scoreboard.score), 1, (10, 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            started = True
            if event.key == pygame.K_DOWN:
                Body.move_dir = 'down'
                if len(BodyCount.bodies) > 1:
                    move_forward()

            elif event.key == pygame.K_UP:
                Body.move_dir = 'up'
                if len(BodyCount.bodies) > 1:
                    move_forward()

            elif event.key == pygame.K_LEFT:
                Body.move_dir = 'left'
                if len(BodyCount.bodies) > 1:
                    move_forward()

            elif event.key == pygame.K_RIGHT:
                Body.move_dir = 'right'
                if len(BodyCount.bodies) > 1:
                    move_forward()

    if milliseconds_since_last_event > 200:
        if Body.move_dir == 'right':
            snake_head.body = snake_head.body.move(Body.speed_right)
            BodyCount.head_pos.append((snake_head.body.x, snake_head.body.y))
        elif Body.move_dir == 'left':
            snake_head.body = snake_head.body.move(Body.speed_left)
            BodyCount.head_pos.append((snake_head.body.x, snake_head.body.y))
        elif Body.move_dir == 'up':
            snake_head.body = snake_head.body.move(Body.speed_up)
            BodyCount.head_pos.append((snake_head.body.x, snake_head.body.y))
        else:
            snake_head.body = snake_head.body.move(Body.speed_down)
            BodyCount.head_pos.append((snake_head.body.x, snake_head.body.y))
        if len(BodyCount.bodies) > 1:
            move_forward()
        milliseconds_since_last_event = 0

    # quick and dirty solution
    screen.blit(bg, bg_rect)
    screen.blit(apple.img, apple.body)
    for body_part in BodyCount.bodies:
        screen.blit(body_part.img, body_part.body)
    screen.blit(Scoreboard.text, Scoreboard.textpos)

    pygame.display.flip()   # updates whole screen whereas update(*args) only the args portion of the screen.

