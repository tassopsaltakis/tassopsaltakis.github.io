import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Shooter")

# Camera settings
camera_pos = np.array([0.0, 1.0, 5.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw = -90.0
pitch = 0.0
fov = 60.0

# Timing
clock = pygame.time.Clock()

# Mouse settings
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
last_mouse_x, last_mouse_y = pygame.mouse.get_pos()
first_mouse = True

# Load textures
def load_texture(surface):
    texture_data = pygame.image.tostring(surface, "RGB", True)
    width, height = surface.get_size()
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return texid

# Create simple textures for walls and floor
def create_checkerboard_texture(size=256, color1=(255, 255, 255), color2=(0, 0, 0)):
    surface = pygame.Surface((size, size))
    tile_size = size // 8
    for y in range(8):
        for x in range(8):
            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, color1, rect)
            else:
                pygame.draw.rect(surface, color2, rect)
    return load_texture(surface)

wall_texture = create_checkerboard_texture(color1=(200, 200, 200), color2=(100, 100, 100))
floor_texture = create_checkerboard_texture(color1=(50, 50, 50), color2=(150, 150, 150))

# Gun model (simple cube for now)
def draw_gun():
    glPushMatrix()
    glTranslatef(0.2, -0.2, -0.5)
    glScalef(0.2, 0.2, 0.5)
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0)
    # Front Face
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f( 1.0, -1.0, 1.0)
    glVertex3f( 1.0,  1.0, 1.0)
    glVertex3f(-1.0,  1.0, 1.0)
    # Back Face
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    # Top Face
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0,  1.0)
    glVertex3f( 1.0, 1.0,  1.0)
    glVertex3f( 1.0, 1.0, -1.0)
    # Bottom Face
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    # Right face
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0,  1.0, -1.0)
    glVertex3f(1.0,  1.0,  1.0)
    glVertex3f(1.0, -1.0,  1.0)
    # Left Face
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glEnd()
    glPopMatrix()

# Enemy model (simple cube)
def draw_enemy(position):
    glPushMatrix()
    glTranslatef(*position)
    glScalef(1.0, 2.0, 1.0)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)
    # Same cube code as draw_gun()
    # Front Face
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f( 0.5, 0.0, 0.5)
    glVertex3f( 0.5, 1.0, 0.5)
    glVertex3f(-0.5, 1.0, 0.5)
    # Back Face
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 1.0, -0.5)
    glVertex3f( 0.5, 1.0, -0.5)
    glVertex3f( 0.5, 0.0, -0.5)
    # Top Face
    glVertex3f(-0.5, 1.0, -0.5)
    glVertex3f(-0.5, 1.0,  0.5)
    glVertex3f( 0.5, 1.0,  0.5)
    glVertex3f( 0.5, 1.0, -0.5)
    # Bottom Face
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f( 0.5, 0.0, -0.5)
    glVertex3f( 0.5, 0.0,  0.5)
    glVertex3f(-0.5, 0.0,  0.5)
    # Right face
    glVertex3f(0.5, 0.0, -0.5)
    glVertex3f(0.5,  1.0, -0.5)
    glVertex3f(0.5,  1.0,  0.5)
    glVertex3f(0.5, 0.0,  0.5)
    # Left Face
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0,  0.5)
    glVertex3f(-0.5,  1.0,  0.5)
    glVertex3f(-0.5,  1.0, -0.5)
    glEnd()
    glPopMatrix()

# Level data
walls = [
    # Each wall is defined by two points (start and end)
    ((-5, 0, -5), (-5, 0, 5)),
    ((-5, 0, 5), (5, 0, 5)),
    ((5, 0, 5), (5, 0, -5)),
    ((5, 0, -5), (-5, 0, -5)),
]

# Enemies
enemies = [
    np.array([2.0, 0.0, -2.0]),
    np.array([-2.0, 0.0, -3.0]),
]

def draw_walls():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, wall_texture)
    glColor3f(1.0, 1.0, 1.0)
    for wall in walls:
        glBegin(GL_QUADS)
        p1 = wall[0]
        p2 = wall[1]
        # Left Side
        glTexCoord2f(0.0, 0.0); glVertex3f(p1[0], 0.0, p1[2])
        glTexCoord2f(1.0, 0.0); glVertex3f(p2[0], 0.0, p2[2])
        glTexCoord2f(1.0, 1.0); glVertex3f(p2[0], 2.0, p2[2])
        glTexCoord2f(0.0, 1.0); glVertex3f(p1[0], 2.0, p1[2])
        glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_floor():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-10.0, 0.0, -10.0)
    glTexCoord2f(10.0, 0.0); glVertex3f(10.0, 0.0, -10.0)
    glTexCoord2f(10.0, 10.0); glVertex3f(10.0, 0.0, 10.0)
    glTexCoord2f(0.0, 10.0); glVertex3f(-10.0, 0.0, 10.0)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def process_input():
    global camera_pos, yaw, pitch, camera_front  # Include camera_front here

    movement_speed = 0.1
    rotation_speed = 0.1

    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_w]:
        camera_pos += movement_speed * camera_front
    if keys[pygame.K_s]:
        camera_pos -= movement_speed * camera_front
    if keys[pygame.K_a]:
        camera_pos -= np.cross(camera_front, camera_up) * movement_speed
    if keys[pygame.K_d]:
        camera_pos += np.cross(camera_front, camera_up) * movement_speed

    # Controller input
    if joystick:
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        axis_rx = joystick.get_axis(3)
        axis_ry = joystick.get_axis(4)

        camera_pos += movement_speed * camera_front * -axis_y
        camera_pos += np.cross(camera_front, camera_up) * movement_speed * axis_x

        yaw += axis_rx * rotation_speed * 5
        pitch -= axis_ry * rotation_speed * 5

    # Mouse movement
    global last_mouse_x, last_mouse_y, first_mouse  # Include other globals if needed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if first_mouse:
        last_mouse_x = mouse_x
        last_mouse_y = mouse_y
        first_mouse = False

    x_offset = mouse_x - last_mouse_x
    y_offset = last_mouse_y - mouse_y
    last_mouse_x = mouse_x
    last_mouse_y = mouse_y

    sensitivity = 0.1
    x_offset *= sensitivity
    y_offset *= sensitivity

    yaw += x_offset
    pitch += y_offset

    if pitch > 89.0:
        pitch = 89.0
    if pitch < -89.0:
        pitch = -89.0

    # Update camera front vector
    front = np.array([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ])
    camera_front = front / np.linalg.norm(front)

def main():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(fov, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == JOYBUTTONDOWN:
                if joystick.get_button(0):
                    print("Shoot!")
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Shoot!")

        process_input()

        # Rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        camera_target = camera_pos + camera_front
        gluLookAt(
            camera_pos[0], camera_pos[1], camera_pos[2],
            camera_target[0], camera_target[1], camera_target[2],
            camera_up[0], camera_up[1], camera_up[2]
        )

        draw_floor()
        draw_walls()

        # Draw enemies
        for enemy_pos in enemies:
            draw_enemy(enemy_pos)

        # Draw gun
        draw_gun()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
