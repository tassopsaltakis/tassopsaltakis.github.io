import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame and controller
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
if joystick:
    joystick.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Floor properties
FLOOR_SIZE = 10  # Number of cubes along one edge
CUBE_SIZE = 1.0  # Size of each cube

# Player properties
player_position = np.array([0.0, CUBE_SIZE / 2, 0.0])  # Start at the center
player_velocity = np.array([0.0, 0.0, 0.0])
PLAYER_SPEED = 5.0  # Units per second

# Time step
dt = 0.01  # Simulation time step

# Camera properties
camera_angle = [0.0, 0.0]  # [rotation around x-axis, rotation around y-axis]
camera_distance = 20.0

# Light properties for neon effect
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Ambient light
    ambient_color = [0.1, 0.1, 0.1, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)

    # Diffuse light
    diffuse_color = [0.5, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_color)

    # Specular light
    specular_color = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_color)

    # Position the light
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 0, 1])

def draw_cube(position):
    glPushMatrix()
    glTranslatef(*position)
    glScalef(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
    cube_vertices = [
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [-0.5,  0.5, -0.5],
        [-0.5,  0.5,  0.5],
        [0.5, -0.5, -0.5],
        [0.5, -0.5,  0.5],
        [0.5,  0.5, -0.5],
        [0.5,  0.5,  0.5],
    ]
    cube_faces = [
        [0,1,3,2],
        [4,6,7,5],
        [0,2,6,4],
        [1,5,7,3],
        [0,4,5,1],
        [2,3,7,6],
    ]
    glBegin(GL_QUADS)
    for face in cube_faces:
        for vertex in face:
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glPopMatrix()

def draw_sphere(radius=0.5, slices=16, stacks=16):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, slices, stacks)

def draw_floor():
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.5, 1.0, 1.0])  # Neon blue emission
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])   # Black diffuse
    for x in range(-FLOOR_SIZE // 2, FLOOR_SIZE // 2):
        for z in range(-FLOOR_SIZE // 2, FLOOR_SIZE // 2):
            position = [x * CUBE_SIZE, -CUBE_SIZE / 2, z * CUBE_SIZE]
            draw_cube(position)
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # Reset emission

def draw_player():
    glPushMatrix()
    glTranslatef(*player_position)
    glColor3f(1.0, 0.0, 0.0)  # Red color
    draw_sphere(radius=0.5, slices=16, stacks=16)
    glPopMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def handle_input():
    global player_velocity

    keys = pygame.key.get_pressed()

    move_forward = move_backward = move_left = move_right = False

    # Keyboard input
    if keys[K_w] or keys[K_UP]:
        move_forward = True
    if keys[K_s] or keys[K_DOWN]:
        move_backward = True
    if keys[K_a] or keys[K_LEFT]:
        move_left = True
    if keys[K_d] or keys[K_RIGHT]:
        move_right = True

    # Joystick input
    if joystick:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        if axis_y < -0.1:
            move_forward = True
        if axis_y > 0.1:
            move_backward = True
        if axis_x < -0.1:
            move_left = True
        if axis_x > 0.1:
            move_right = True

    # Compute movement direction
    direction = np.array([0.0, 0.0, 0.0])
    if move_forward:
        direction[2] -= 1.0
    if move_backward:
        direction[2] += 1.0
    if move_left:
        direction[0] -= 1.0
    if move_right:
        direction[0] += 1.0

    # Normalize direction
    if np.linalg.norm(direction) != 0:
        direction = direction / np.linalg.norm(direction)

    # Update player velocity
    player_velocity = direction * PLAYER_SPEED

def update_player():
    global player_position

    player_position += player_velocity * dt

    # Collision detection with floor boundaries
    half_floor = (FLOOR_SIZE // 2) * CUBE_SIZE
    for i in [0, 2]:  # x and z axes
        if player_position[i] < -half_floor + CUBE_SIZE / 2:
            player_position[i] = -half_floor + CUBE_SIZE / 2
        elif player_position[i] > half_floor - CUBE_SIZE / 2:
            player_position[i] = half_floor - CUBE_SIZE / 2

def main():
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    init_opengl()
    setup_lighting()

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            elif event.type == MOUSEMOTION:
                x, y = event.rel
                camera_angle[0] += y * 0.1
                camera_angle[1] += x * 0.1

        handle_input()
        update_player()

        # Rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera transformation
        glTranslatef(0.0, -2.0, -camera_distance)
        glRotatef(camera_angle[0], 1, 0, 0)
        glRotatef(camera_angle[1], 0, 1, 0)

        draw_floor()
        draw_player()

        pygame.display.flip()

if __name__ == "__main__":
    main()
