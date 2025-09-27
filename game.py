# game data
 
from pgzero.actor import Actor
from random import randint, choice
from pgzero.clock import clock
import pgzrun
 
WIDTH = 800
HEIGHT = 600
 
GROUND = 380
GRAVITY = 900
 
NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 200
JUMP_SPEED = 600
 
game_state = 'start'
 
# hero initialisation
hero = Actor("hero0", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND)
hero_speed = 2
on_ground = True
 
# état de transparence du héro
invincible = False
invincible_timer = 0.0
 
#Hero lifes
hero_lifes = 3
life = Actor("heart2")
lifes = []

for i in range(hero_lifes):
    life = Actor("heart2")
    life.x =  25 + i * (life.width + 8)
    life.y = 25
    lifes.append(life)
 
# compte de saut pour augmenter la vistesse
jump_count = 0
 
#collision héros/box
collision_cooldown = 1.0  # 1 seconde de délai entre deux collisions
collision_timer = 0.0
collision_active = False
 
# enemies initialisations
BOX_APPARTION = (2, 5)
FLYING_APPARITION = (2, 5)
 
next_enemy_time = randint(min(BOX_APPARTION[0], FLYING_APPARITION[0]), max(BOX_APPARTION[1], FLYING_APPARITION[1]))
 
boxes = []
flying_enemies = []
 
# background inititalisation
bg_start = Actor('bg_start')
bg_break = Actor('bg_break')
bg_over = Actor('bg_over')
backgrounds_bottom = []
backgrounds_top = []
 
for n in range(NUMBER_OF_BACKGROUND):
    bg_t = Actor("bg_1", anchor=('left', 'top'))
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)
 
    bg_b = Actor("bg_2", anchor=('left', 'bottom'))
    bg_b.pos = n * WIDTH, HEIGHT
    backgrounds_bottom.append(bg_b)
 
# element décor
element = []
nbrElm = 2
 
for n in range(nbrElm):
    elem = Actor("elem0")
    elem.pos = (n * WIDTH, 80)
    element.append(elem)
 
def draw():
    screen.clear()
 
    if game_state == 'start':
        bg_start.draw()
        screen.draw.text("Appuie sur ENTREE pour commencer", fontname= "pixel_font1", center=(WIDTH//2, HEIGHT//2), fontsize=40, color="white")
 
    elif game_state == 'game':
        for bg in backgrounds_bottom:
            bg.draw()
        for bg in backgrounds_top:
            bg.draw()
        for box in boxes:
            box.draw()
            if box.colliderect(hero):
                set_hero_hurt()
 
        #dessiner l'élément
        for elem in element:
            elem.draw()
        
        #dessin des vies
        for live in lifes:
            live.draw()

        hero.draw()
 
        for enemy in flying_enemies:
            enemy.draw()
            if enemy.colliderect(hero):
                set_hero_hurt()
 
    elif game_state == 'break':
        bg_break.draw()
        screen.draw.text("Pause - Appuie sur ENTREE pour reprendre", fontname = "pixel_font1", center=(WIDTH//2, HEIGHT//2), fontsize = 35, color ="white")
 
    elif game_state == 'over':
        bg_over.draw()
        screen.draw.text("Game Over - Appuie sur ENTREE pour recommencer", fontname = "pixel_font1", center=(WIDTH//2, HEIGHT//1.55), fontsize = 30, color = "#a8dbff")
 

def enemy_spawn_time():
    base_min, base_max = BOX_APPARTION[0], BOX_APPARTION[1]

    factor = min(jump_count / 10, 1)
    min_time = base_min * (1 - 0.5 * factor)
    max_time = base_max * (1 - 0.5 * factor)

    return randint(int(min_time), int(max_time))


def update(dt):
 
    if game_state == 'start':
        update_start(dt)
    elif game_state == 'game':
        update_game(dt)
    elif game_state == 'break':
        update_break(dt)
    elif game_state == 'over':
        update_over(dt)
 
 
def update_break(dt):
    pass
 
 
def update_over(dt):
    pass
 
 
def update_start(dt):
    pass
 
 
def update_game(dt):
    global next_enemy_time, hero_speed, on_ground, invincible, invincible_timer, collision_timer, game_state
 
    #Enemy Update
    next_enemy_time -= dt
    if next_enemy_time <= 0:
        enemy_type = choice(["box", "fly"])
 
        if enemy_type == "box":
            box = Actor("box", anchor=('left', 'bottom'))
            box.pos = WIDTH, GROUND
            boxes.append(box)
            next_enemy_time = enemy_spawn_time()
 
        else:
            enemy = Actor("fly", anchor=('center', 'center'))
            enemy.pos = (WIDTH, randint(220, 350))
            enemy.direction = 1
            enemy.oscillation = 0
            flying_enemies.append(enemy)
            next_enemy_time = enemy_spawn_time()
           
    # rendre le héros invincible pendant x temps
    if invincible:
        invincible_timer -= dt
        if invincible_timer <= 0:
            invincible = False
 
    # décrémenter le timer de collision
    if collision_timer > 0:
        collision_timer -= dt
 
    # boxes
    for box in boxes:
        x, y = box.pos

        if jump_count <= 6:
            x -= GAME_SPEED * dt
        elif jump_count <= 12:
            x -= GAME_SPEED * 1.5 * dt
        else:
            x -= GAME_SPEED * 2 * dt

        box.pos = x, y

 
        # collision AVEC le héros placée dans la boucle
        if box.colliderect(hero) and collision_timer <= 0 and not invincible:
            if lifes:
                lifes.pop()
            if len(lifes) == 0:
                game_state = "over"
            collision_timer = collision_cooldown
            invincible = True
            invincible_timer = 1.0
 
    if boxes and boxes[0].pos[0] <= -32:
        boxes.pop(0)
 
    # flying enemies
    for enemy in flying_enemies:
        x, y = enemy.pos
 
        # Vitesse horizontale dynamique
        if jump_count <= 6:
            x -= GAME_SPEED * dt
        elif jump_count <= 12:
            x -= GAME_SPEED * 1.5 * dt
        else:
            x -= GAME_SPEED * 2 * dt
 
        # Oscillation verticale inchangée
        oscillation_speed = 100
        movement = oscillation_speed * dt * enemy.direction
        y += movement
        enemy.oscillation += movement
 
        if abs(enemy.oscillation) >= 20:
            enemy.direction *= -1
            enemy.oscillation = max(min(enemy.oscillation, 20), -20)
 
        enemy.pos = x, y
 
        # collision avec le héros
        if enemy.colliderect(hero) and collision_timer <= 0 and not invincible:
            if lifes:
                lifes.pop()
            if len(lifes) == 0:
                game_state = "over"
            collision_timer = collision_cooldown
            invincible = True
            invincible_timer = 1.0
 
    # hero update
    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt
 
    if y >= GROUND:
        y = GROUND
        hero_speed = 0
        on_ground = True
    else:
        on_ground = False
 
    hero.pos = x, y
 
    # bg update
    speed_multiplier = min(3, 1 + jump_count * 0.1)
 
    # Mise à jour du décor du haut
    for bg in backgrounds_top:
        x, y = bg.pos
        x -= (GAME_SPEED / 3) * speed_multiplier * dt
        bg.pos = x, y
 
    if backgrounds_top[0].pos[0] <= -WIDTH:
        bg = backgrounds_top.pop(0)
        last_bg = backgrounds_top[-1]
        bg.pos = last_bg.pos[0] + WIDTH, 0
        backgrounds_top.append(bg)

    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= (GAME_SPEED / 1.5) * speed_multiplier * dt
        bg.pos = x, y
  
    if backgrounds_bottom[0].pos[0] <= -WIDTH:
        bg = backgrounds_bottom.pop(0)
        last_bg = backgrounds_bottom[-1]
        bg.pos = last_bg.pos[0] + WIDTH, HEIGHT
        backgrounds_bottom.append(bg)

        if backgrounds_bottom[0].pos[0] <= -WIDTH:
            bg = backgrounds_bottom.pop(0)
            last_bg = backgrounds_bottom[-1]
            bg.pos = last_bg.pos[0] + WIDTH, HEIGHT
            backgrounds_bottom.append(bg)
 
    # element update
    for elem in element:
        x, y = elem.pos
        x -= GAME_SPEED/0.5 * dt
        elem.pos = x, y
 
    if element[0].pos[0] <= -(WIDTH-100):
        elem = element.pop(0)
        last_x = element[-1].pos[0]  
        elem.pos = last_x + WIDTH * 2.25, 80
        element.append(elem)
 
 
def reset_game():
    global hero, boxes, hero_speed, next_enemy_time, elem, invincible,invincible_timer, collision_timer, lifes, jump_count, flying_enemies
 
    hero.pos = (64, GROUND)
    hero_speed = 0
    boxes = []
    flying_enemies = []
    next_enemy_time = randint(min(BOX_APPARTION[0], FLYING_APPARITION[0]), max(BOX_APPARTION[1], FLYING_APPARITION[1]))
    invincible = False
    invincible_timer = 0.0
    collision_timer = 0.0
    jump_count = 0
 
    # Réinitialiser les éléments de décor
    for i, elem in enumerate(element):
        elem.pos = (i * WIDTH, 80)
   
    # remettre des vies
    lifes = []
    for i in range(hero_lifes):
        life = Actor("heart2")
        life.x = 25 + i * (life.width + 8)
        lifes.append(life)


def on_key_down(key):
    global hero_speed, game_state, jump_count
 
    if key == keys.SPACE and on_ground:
        hero_speed = JUMP_SPEED
        jump_count += 1
 
    if key == keys.RETURN and game_state == 'start':
        game_state = 'game'
    elif key == keys.RETURN and game_state == 'game':
        game_state = 'break'
    elif key == keys.RETURN and game_state == 'break':
        game_state = 'game'
    elif key == keys.RETURN and game_state == 'over':
        reset_game()
        game_state = 'game'


# animation
hero_animation_index = 0
elem_animation_index = 0
 
def animation():
    global  hero_animation_index, elem_animation_index
 
    table_hero =['hero0','hero1','hero2','hero3']
    table_elem =['elem0', 'elem1', 'elem2']
 
 
    hero.image = table_hero[hero_animation_index]
    hero_animation_index += 1
    if hero_animation_index >= len(table_hero):
        hero_animation_index = 0
 
    
    for elem in element:
        elem.image = table_elem[elem_animation_index]
        elem_animation_index += 1
        if elem_animation_index >= len(table_elem):
            elem_animation_index = 0

    # image du héro qui saute
    if hero.y < GROUND:
        hero.image = 'hero_jump'
 
clock.schedule_interval(animation, 1/6)

#héro normal
def set_hero_normal():
    hero.image = 'hero0'

# changement de sprite pour héro
def set_hero_hurt():
    hero.image = 'hero_hurt'
    clock.schedule_unique(set_hero_normal, 1.0)
 
pgzrun.go()