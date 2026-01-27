from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import time
import random


player_pos = (0, 0, 0, 0)
x, y, z, angle = player_pos
camera_pos = (x, y+70, z+100)
t1 = int(time.time())
t2 = int(time.time())
fovY = 125
player_life = 100
score = 0
fpp = False
game_state = False
game_start = True
enemy_spaceship = []
asteroid = []
bullet = []
enemy_bullet = []
ang = 0
map_edge = False
ship_color = (0.95, 0.95, 0.86)
ship_speed = 3
d, h = -500, 500


def create_asteroid():
    x = random.randint(-10000, 10000)
    y = random.randint(-10000, 10000)
    z = random.randint(-10000, 10000)
    
    return (x, y, z)


def create_enemy_spaceship():
    x = random.randint(-10000, 10000)
    y = random.randint(-10000, 10000)
    return (x, y)


def create_enemy_bullet():
    global enemy_bullet
    glPushMatrix()
    for b in enemy_bullet:
        x, y, z, dir = b

        glColor3f(1, 0, 0)
        glTranslate(x, y, z)
        glutSolidCube(20)
        glTranslate(-x, -y, -z)

    glPopMatrix()

def shoot():
    global t2, enemy_spaceship,enemy_bullet,player_pos
    t = int(time.time())
    if (t - t2) > 5:
        t2 = t
        for i in enemy_spaceship:
            x,y = i
            enemy_bullet.append((x,y,player_pos[2],player_pos[3]))  



for i in range(500):
    asteroid.append(create_asteroid())

for i in range(10):
    enemy_spaceship.append(create_enemy_spaceship())


def spawn_enemy_spaceship():
    global enemy_spaceship, player_pos
    x, y, z, ang = player_pos
    for i in enemy_spaceship:
        x_e, y_e = i
        draw_enemy_spaceship(x_e, y_e, z)


def draw_text(x, y, text, color, flag=False, font=GLUT_BITMAP_HELVETICA_18):
    global game_state, player_life

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    if flag:
        # health bar
        glPointSize(40)
        glLineWidth(10)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex2f(165, 775)
        glVertex2f(165 + player_life * 5, 775)
        glEnd()
        glLineWidth(1)

    r, g, b = color
    glColor3f(r, g, b)
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_bullet():
    global bullet
    glPushMatrix()

    for b in bullet:
        x, y, z, dir = b

        glColor3f(1, 0, 0)
        glTranslate(x, y, z)
        glutSolidCube(20)
        glTranslate(-x, -y, -z)

    glPopMatrix()


def keyboardListener(key, x, y):
    global player_pos, player_life, score, fpp, game_state, enemy_spaceship, asteroid, map_edge, camera_pos, bullet, ang, ship_color, ship_speed, t1, t2, d, h, enemy_bullet, game_start

    if key == b'w' and game_state:
        t = int(time.time())
        if (t - t1) > 5:
            t1 = t
            ship_speed = 10

    if key == b's' and game_state:
        pass

    if key == b'a' and game_state:
        x1, y1, z1, angle = player_pos
        angle += 2
        player_pos = x1, y1, z1, angle

    if key == b'd' and game_state:
        x1, y1, z1, angle = player_pos
        angle -= 2
        player_pos = x1, y1, z1, angle
    
    if key == b'x':
        glutLeaveMainLoop()

    if key == b'r':
        player_pos = (0, 0, 0, 0)
        x, y, z, angle = player_pos
        camera_pos = (x, y+70, z+100)
        t1 = int(time.time())
        t2 = int(time.time())
        fovY = 125
        player_life = 100
        score = 0
        fpp = False
        game_state = True
        game_start = False
        enemy_spaceship = []
        asteroid = []
        bullet = []
        enemy_bullet = []
        ang = 0
        map_edge = False
        ship_color = (0.95, 0.95, 0.86)
        ship_speed = 3
        d, h = -500, 500
        for i in range(500):
            asteroid.append(create_asteroid())

        for i in range(10):
            enemy_spaceship.append(create_enemy_spaceship())


def specialKeyListener(key, x, y):
    global camera_pos, fpp, game_state, player_pos
    x, y, z, angle = player_pos

    if game_state:
        if key == GLUT_KEY_UP:
            z += 50

        if key == GLUT_KEY_DOWN:
            z -= 50

        player_pos = (x, y, z, angle)
        camera_pos = x, y + 70, z + 100
        if fpp:
            camera_pos = x, y + 500, z + 530


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """

    global fpp, camera_pos, player_pos, bullet, d, h
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x1, y1, z1, angle = player_pos
        bullet.append((x1, y1, z1, angle))

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if fpp:
            d, h = -500, 500
        else:
            d, h = -100, 100
        fpp = not fpp


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    global fpp, player_pos, camera_pos, d, h

    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 20000)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x1, y1, z1, angle = player_pos

    rad = math.radians(angle)

    dx = d * math.sin(rad)
    dy = -d * math.cos(rad)

    cx = x1 + dx
    cy = y1 + dy
    cz = z1 + h

    gluLookAt(cx, cy, cz,
              x1, y1, z1,
              0, 0, 1)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global bullet, enemy_spaceship, player_pos, game_state, ship_speed, enemy_bullet

    if game_state:
        x1, y1, z1, angle = player_pos
        dx = ship_speed * math.sin(math.radians(angle))
        dy = ship_speed * math.cos(math.radians(angle))
        player_pos = x1 + dx, y1 - dy, z1, angle

        for i in range(len(bullet)):
            x, y, z, dir = bullet[i]
            y -= 15 * math.cos(math.radians(dir))
            x += 15 * math.sin(math.radians(dir))
            bullet[i] = x, y, z, dir

        x1, y1, z1, angle = player_pos

        for j in range(len(enemy_spaceship)):
            x2, y2 = enemy_spaceship[j]
            x = x1 - x2
            y = y1 - y2
            d = math.degrees(math.atan2(y, x))
            if d < 0:
                d += 360

            x2 += 2 * math.cos(math.radians(d))
            y2 += 2 * math.sin(math.radians(d))
            enemy_spaceship[j] = (x2, y2)

        for k in range(len(enemy_bullet)):
            x,y,z,d = enemy_bullet[k]
            a = x - x1
            b = y - y1
            dr = math.degrees(math.atan2(b,a))
            if dr < 0:
                dr += 360
            x -= 15 * math.cos(math.radians(dr))
            y -= 15 * math.sin(math.radians(dr))
            enemy_bullet[k] = x, y, z, d

    glutPostRedisplay()

def check_range():
    global player_pos, game_state
    x, y, z, angle = player_pos
    if (x > 10000) or (x < -10000) or (y > 10000) or (y < -10000) or (z > 10000) or (z < -10000):
        game_state = False


def check_hit():
    global enemy_spaceship, bullet, score, player_pos, player_life,asteroid,ship_color,enemy_bullet

    x3, y3, z3, angle = player_pos

    for i in range(len(bullet)):
        x1, y1, z1, dir = bullet[i]
        for j in range(len(enemy_spaceship)):
            x2, y2 = enemy_spaceship[j]
            d1 = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)
            if d1 < 50:
                score += 1
                bullet[i] = (-100000, -1000000, -100000 ,dir)
                enemy_spaceship[j] = create_enemy_spaceship()

    temp = []
    for i in range(len(bullet)):
        x, y, z, dir = bullet[i]
        if (z != -100000):
            temp.append((x, y, z, dir))
    bullet = temp

    for k in range(len(enemy_spaceship)):
        x2, y2 = enemy_spaceship[k]
        d2 = ((x2 - x3)**2 + (y2 - y3)**2)**(0.5)
        if d2 < 50:
            player_life -= 10
            r, g, b = ship_color
            r += 0.1
            g -= 0.1
            b -= 0.1
            ship_color = (r, g, b)
            enemy_spaceship[k] = create_enemy_spaceship()

    for a in range(len(asteroid)):
        x1, y1, z1 = asteroid[a]
        d_a = ((x1 - x3)**2 + (y1 - y3)**2 + (z1 - z3)**2)**0.5
        if d_a < 100:
            player_life -= 5
            r, g, b = ship_color
            r += 0.1
            g -= 0.1
            b -= 0.1
            ship_color = (r, g, b)
            asteroid[a] = create_asteroid()

    for i in range(len(enemy_bullet)):
        x,y,z,d = enemy_bullet[i]
        dr = ((x - x3) ** 2 +(y - y3)**2 + (z - z3) * 2) **(0.5)
        if dr < 50:
            enemy_bullet[i] = (-1000000, -1000000, -100000, d)
            player_life -= 1
            r, g, b = ship_color
            r += 0.01
            g -= 0.01
            b -= 0.01
            ship_color = (r, g, b)
    t = []
    for i in range(len(enemy_bullet)):
        x, y, z, dir = enemy_bullet[i]
        if (z != -100000):
            t.append((x, y, z, dir))
    enemy_bullet = t


def game_info():
    global game_state, player_life, score, map_edge, t1, game_start

    if game_start:
        draw_text(380, 500, f"Welcome to Star Wars 3D", (1, 1, 1))
        draw_text(360, 460, f'Please Press R to start the game', (1, 1, 1))
        draw_text(380, 420, f'Press X to close the game', (1, 1, 1))
    
    else:
        if game_state:
            draw_text(10, 770, f"Spaceship Health: ", (1, 1, 1), True)
            draw_text(10, 740, f"Game Score: {score}", (1, 1, 1))
            t = int(time.time())
            if ((t - t1) > 5 and t % 2 == 0):
                draw_text(
                    300, 680, "Speed Boost is available now! Press W to activate", (1, 1, 0.3))

            if map_edge:
                if (t % 2 == 0):
                    draw_text(
                        10, 710, "Approaching the firewall !!\nTurn back immediately!!", (1, 0.3, 0))
        else:
            draw_text(360, 500, f"Game is over. Your Score is {score}", (1, 1, 1))
            draw_text(360, 460, f'Press "R" to RESTART the Game.', (1, 1, 1))
            draw_text(380, 420, f'Press X to close the game', (1, 1, 1))


def draw_game_space():
    global player_pos, map_edge
    x, y, z, angle = player_pos
    t = int(time.time())

    glBegin(GL_QUADS)

    if x < -8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(-10000, -10000, -10000)
        glVertex3f(-10000, -10000, 10000)
        glVertex3f(-10000, 10000, 10000)
        glVertex3f(-10000, 10000, -10000)

    if x > 8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(10000, -10000, -10000)
        glVertex3f(10000, -10000, 10000)
        glVertex3f(10000, 10000, 10000)
        glVertex3f(10000, 10000, -10000)

    if y < -8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(10000, -10000, -10000)
        glVertex3f(10000, -10000, 10000)
        glVertex3f(-10000, -10000, 10000)
        glVertex3f(-10000, -10000, -10000)

    if y > 8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(10000, 10000, -10000)
        glVertex3f(10000, 10000, 10000)
        glVertex3f(-10000, 10000, 10000)
        glVertex3f(-10000, 10000, -10000)

    if z < -8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(10000, 10000, -10000)
        glVertex3f(10000, -10000, -10000)
        glVertex3f(-10000, -10000, -10000)
        glVertex3f(-10000, 10000, -10000)

    if z > 8000:
        glColor3d(1, 0.92, 0)
        glVertex3f(10000, 10000, 10000)
        glVertex3f(10000, -10000, 10000)
        glVertex3f(-10000, -10000, 10000)
        glVertex3f(-10000, 10000, 10000)

    glEnd()


def draw_spaceship():
    global player_pos, ship_color
    x, y, z, ang = player_pos
    r, g, b = ship_color

    glPushMatrix()
    glColor3f(r, g, b)
    glTranslatef(x, y, z)
    glRotate(ang, 0, 0, 1)
    glutSolidCube(90)
    glColor3f(1, 0.647, 0)
    glTranslatef(30, 30, 0)
    glRotate(90, 0, 0, 1)
    glRotate(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20, 2, 50, 10, 10)
    glTranslatef(0, 60, 0)
    gluCylinder(gluNewQuadric(), 20, 2, 50, 10, 10)
    glColor3f(0.55, 0.57, 0.55)
    glRotate(90, 0, 1, 0)
    glRotate(90, 0, 1, 0)
    glTranslatef(0, -30, 100)
    gluCylinder(gluNewQuadric(), 20, 2, 180, 10, 10)
    glPopMatrix()


def draw_asteroid():
    global asteroid
    glPushMatrix()
    for i in asteroid:
        x, y, z = i
        glColor3f(0.75, 0.75, 0.75)
        glTranslatef(x, y, z)
        gluSphere(gluNewQuadric(), 150, 10, 10)
        glTranslatef(-x, -y, -100)
    glPopMatrix()


def draw_enemy_spaceship(x, y, z):
    global player_pos
    x1, y1, z1, ang = player_pos
    glPushMatrix()
    # glColor3f(0.529, 0.81, 0.921)
    glColor3f(0.5, 0., 0.5)
    glTranslatef(x, y, z)
    glRotate(ang, 0, 0, 1)
    glutSolidCube(90)
    glColor3f(1, 0.647, 0)
    glTranslatef(30, 30, 0)
    glRotate(90, 0, 0, 1)
    glRotate(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 20, 2, 50, 10, 10)
    glTranslatef(0, 60, 0)
    gluCylinder(gluNewQuadric(), 20, 2, 50, 10, 10)
    glColor3f(0.55, 0.57, 0.55)
    glRotate(90, 0, 1, 0)
    glRotate(90, 0, 1, 0)
    glTranslatef(0, -30, 100)
    gluCylinder(gluNewQuadric(), 20, 2, 180, 10, 10)
    glPopMatrix()


def run_game():
    global game_over, game_state, player_pos, map_edge, ship_speed, player_life, t1
    x, y, z, angle = player_pos
    
    if player_life <= 0:
        game_state = False

    if game_state:
        draw_game_space()
        check_hit()
        draw_asteroid()
        spawn_enemy_spaceship()
        draw_spaceship()
        draw_bullet()
        check_range()
        create_enemy_bullet()
        shoot()

        if (x > 8000) or (x < -8000) or (y > 8000) or (y < -8000) or (z > 8000) or (z < -8000):
            map_edge = True
        else:
            map_edge = False

        t = int(time.time())
        if (t - t1) > 3:
            ship_speed = 3
    game_info()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    run_game()

    # draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    # Double buffering, RGB color, depth test
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    # Register the idle function to move the bullet automatically
    glutIdleFunc(idle)

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
