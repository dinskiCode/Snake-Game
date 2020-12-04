import sys
import pygame
import random

'''
TODO:
Mandatory updates:

--
Optional updates:
1. start-/pause-/end-screen
2. multiple difficulties
3. some sort of overlay that displays current score, difficulty and time 
4. ...
'''

pygame.init()
size = width, height = 750, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

bg = pygame.image.load("Background.png")
bg_rect = bg.get_rect()
controls_img = pygame.image.load("Controls.png")
controls_rect = controls_img.get_rect()
controls_rect.x = 220
controls_rect.y = 500

started = False
ms = 0
milliseconds_since_last_event = 0


# TODO: create file for all the classes
class Scoreboard:
    score = 0
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Your Score: " + str(score), 1, (10, 10, 10))
        text_pos = text.get_rect(centerx=600)


class GameOver:
    game_over = False
    final_score = 0
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Your score: " + str(Scoreboard.score), 1, (10, 10, 10))
        text_pos = text.get_rect(centerx=370, centery=300)

    game_over_box = pygame.image.load("Game_over_box.png")
    game_over_rect = game_over_box.get_rect()
    game_over_rect.x = 200
    game_over_rect.y = 250


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
        if self.is_head is False:
            self.img = pygame.image.load("Body.png")
        else:
            self.img = pygame.image.load("Snake_Head.png")
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

    def random_spawn(self): 
        curr_x = self.body.x    # equal to distance from left border
        curr_y = self.body.y    # equal to distance from top border
        x_pos = random.randint((0-curr_x)/50, (700-curr_x)/50)*50
        y_pos = random.randint((0-curr_y)/50, (700-curr_y)/50)*50
        new_pos = (x_pos, y_pos)
        if (new_pos[0] + curr_x, new_pos[1] + curr_y) not in BodyCount.head_pos:
            self.body = self.body.move(new_pos)
        else:
            self.random_spawn()


# head
snake_head = Body((random.randint(1, 13)*50, random.randint(1, 13)*50), True)
apple = Apple()


def move_forward():
    body_nr = 1
    for b in BodyCount.bodies[1::]:
        b.body = b.body.move(BodyCount.head_pos[len(BodyCount.head_pos) - 1 - body_nr][0] - BodyCount.bodies[body_nr].body.x,
                             BodyCount.head_pos[len(BodyCount.head_pos) - 1 - body_nr][1] - BodyCount.bodies[body_nr].body.y)
        body_nr += 1


def check_self_collision():
    if len(BodyCount.bodies) > 2:
        for bp in BodyCount.bodies[1::]:
            if snake_head.body.x == bp.body.x and snake_head.body.y == bp.body.y:
                GameOver.game_over = True


def check_border_collision():
    if snake_head.body.x < 0 or snake_head.body.x > 700 or snake_head.body.y < 0 or snake_head.body.y > 700:
        GameOver.game_over = True


def update_head_pos():
    if len(BodyCount.head_pos) > len(BodyCount.bodies):
        BodyCount.head_pos.pop(0)


while True:
    update_head_pos()
    check_self_collision()
    check_border_collision()
    if started:
        ms = clock.tick()
    milliseconds_since_last_event += ms

    if snake_head.apple_eaten(apple):
        new_body = Body((BodyCount.head_pos[len(BodyCount.head_pos) - len(BodyCount.bodies)][0],
                         BodyCount.head_pos[len(BodyCount.head_pos) - len(BodyCount.bodies)][1]))
        apple.random_spawn()
        Scoreboard.score += 1
        Scoreboard.text = text = Scoreboard.font.render("Your Score: " + str(Scoreboard.score), 1, (10, 10, 10))
        GameOver.text = text = GameOver.font.render("Game Over! Your score: " + str(Scoreboard.score), 1, (10, 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            started = True
            if event.key == pygame.K_DOWN:
                Body.move_dir = 'down'

            elif event.key == pygame.K_UP:
                Body.move_dir = 'up'

            elif event.key == pygame.K_LEFT:
                Body.move_dir = 'left'

            elif event.key == pygame.K_RIGHT:
                Body.move_dir = 'right'

    if GameOver.game_over:
        Body.move_dir = None

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
        elif Body.move_dir == 'down':
            snake_head.body = snake_head.body.move(Body.speed_down)
            BodyCount.head_pos.append((snake_head.body.x, snake_head.body.y))
        if len(BodyCount.bodies) > 1:
            move_forward()
        milliseconds_since_last_event = 0

    # draw screen, this might not be the best solution though
    screen.blit(bg, bg_rect)
    screen.blit(apple.img, apple.body)
    if not started:
        screen.blit(controls_img, controls_rect)
    for body_part in BodyCount.bodies:
        screen.blit(body_part.img, body_part.body)
    screen.blit(Scoreboard.text, Scoreboard.text_pos)
    if GameOver.game_over:
        screen.blit(GameOver.game_over_box, GameOver.game_over_rect)
        screen.blit(GameOver.text, GameOver.text_pos)

    # TODO: stop updating screen if game over
    pygame.display.flip()   # updates whole screen whereas update(*args) only the args portion of the screen.

