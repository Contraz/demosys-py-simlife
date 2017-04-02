import random
import math
import numpy
from demosys.effects import effect
from demosys.opengl import VAO
from demosys.opengl import geometry
from OpenGL import GL
from OpenGL.arrays import vbo
from pyrr import matrix44


class UnderWaterEffect(effect.Effect):
    """Generated default efffect"""
    def init(self):
        self.mesh_size = 200
        self.scroll0 = 0.0
        self.scroll1 = 0.0
        self.scroll2 = 0.0

        self.debris = generate_debris()
        self.debris_shader = self.get_shader('underwater/debris.glsl')
        self.debris_texture = self.get_texture('underwater/debris.png')

        self.floor = generate_ocean_floor(self.mesh_size)
        self.floor_shader = self.get_shader("underwater/floor.glsl")

    @effect.bind_target
    def draw(self, time, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.draw_floor(self.sys_camera.projection, self.sys_camera.view_matrix)
        self.draw_debris(self.sys_camera.projection, self.sys_camera.view_matrix)

    def draw_floor(self, m_proj, m_mv):
        self.floor.bind(self.floor_shader)
        self.floor_shader.uniform_mat4("m_proj", m_proj)
        self.floor_shader.uniform_mat4("m_mv", m_mv)
        self.floor.draw(mode=GL.GL_TRIANGLE_STRIP)

    def draw_debris(self, m_proj, m_mv):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)

        self.debris.bind(self.debris_shader)
        self.debris_shader.uniform_mat4("m_proj", m_proj)
        self.debris_shader.uniform_mat4("m_mv", m_mv)
        self.debris_shader.uniform_sampler_2d(0, "texture0", self.debris_texture)
        self.debris_shader.uniform_1f("size", 0.25)
        self.debris.draw(mode=GL.GL_POINTS)
        GL.glDisable(GL.GL_BLEND)


def generate_debris():
    size = 128
    colors = [0] * size * 3
    positions = [0] * size * 3

    for i in range(0, size * 3, 3):
        positions[i] = rnd_in_float(-0.5, 0.5) * 200.0
        positions[i + 1] = 2.0 + rnd_in_float(0.0, 1.0) * 10.0
        positions[i + 2] = rnd_in_float(-0.5, 0.5) * 200.0
        col = rnd_in_float(0.0, 1.0)
        colors[i] = col
        colors[i + 1] = col
        colors[i + 2] = col

    position_vbo = vbo.VBO(numpy.array(positions, dtype=numpy.float32))
    color_vbo = vbo.VBO(numpy.array(colors, dtype=numpy.float32))

    vao = VAO("debris")
    vao.add_array_buffer(GL.GL_FLOAT, position_vbo)
    vao.add_array_buffer(GL.GL_FLOAT, color_vbo)
    vao.map_buffer(position_vbo, "in_position", 3)
    vao.map_buffer(color_vbo, "in_color", 3)
    vao.build()
    return vao


def generate_ocean_surface():
    pass


def generate_ocean_floor(mesh_size):
    mesh_res = 32
    # xpos = -mesh_size / 2.0
    zpos = mesh_size / 2.0
    xzstep = mesh_size / mesh_res

    positions = [0] * mesh_res * mesh_res * 3 * 4
    index = 0

    def noise(x, z):
        return math.sin(x * 1000.0) * 3.0 + math.cos(z * 1000.0) * 2.0

    for y in range(mesh_res):
        xpos = -mesh_size / 2.0
        for x in range(mesh_res):
            # r =  rnd_in_float(0, 1) * 10.0
            # Lower Left
            positions[index] = xpos
            positions[index + 1] = noise(xpos, zpos - xzstep)
            positions[index + 2] = zpos - xzstep
            index += 3

            # Upper Left
            positions[index] = xpos
            positions[index + 1] = noise(xpos, zpos)
            positions[index + 2] = zpos
            index += 3

            # Lower Left
            positions[index] = xpos + xzstep
            positions[index + 1] = noise(xpos + xzstep, zpos - xzstep)
            positions[index + 2] = zpos - xzstep
            index += 3

            # Upper Right
            positions[index] = xpos + xzstep
            positions[index + 1] = noise(xpos + xzstep, zpos)
            positions[index + 2] = zpos
            index += 3

            xpos += xzstep
        zpos -= xzstep

    # print(positions)
    position_vbo = vbo.VBO(numpy.array(positions, dtype=numpy.float32))

    vao = VAO("ocean_floor")
    vao.add_array_buffer(GL.GL_FLOAT, position_vbo)
    vao.map_buffer(position_vbo, "in_position", 3)
    vao.build()

    return vao


def rnd_in_float(range_start, range_end):
    rng = range_end - range_start
    rnd = 0.0001 * (random.randint(0, 4294967296) % 10000)
    return range_start + math.fmod(rnd, rng)
