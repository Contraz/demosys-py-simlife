import random
import math
import numpy
from demosys.effects import effect
from demosys.opengl import VAO
from demosys.opengl import geometry
from OpenGL import GL
from OpenGL.arrays import vbo
from pyrr import Vector3, matrix44


class UnderWaterEffect(effect.Effect):
    """Generated default efffect"""
    def init(self):
        self.mesh_size = 200
        self.scroll0 = 0.0
        self.scroll1 = 0.0
        self.scroll2 = 0.0

        self.debris = generate_debris()
        self.debris_texture = self.get_texture('underwater/debris.png')
        self.debris_shader = self.get_shader('underwater/debris.glsl')

        # self.floor = generate_ocean_floor(self.mesh_size)
        self.floor = geometry.plane_xz(size=(self.mesh_size, self.mesh_size), resolution=(128, 128))
        self.floor_shader = self.get_shader("underwater/floor.glsl")
        self.floor_map = self.get_texture("underwater/floor_map.png")
        self.floor_map.set_interpolation(GL.GL_NEAREST)

        self.ocean = geometry.plane_xz(size=(self.mesh_size, self.mesh_size), resolution=(64, 64))
        self.ocean_shader = self.get_shader('underwater/ocean.glsl')
        self.ocean_surface = self.get_texture('underwater/OceanSurface.png')
        self.ocean_normals1 = self.get_texture('underwater/Waves1Normals.png')
        self.ocean_normals2 = self.get_texture('underwater/Waves2Normals.png')
        self.ocean_normals3 = self.get_texture('underwater/Waves3Normals.png')

    @effect.bind_target
    def draw(self, time, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.draw_floor(self.sys_camera.projection, self.sys_camera.view_matrix)
        self.draw_debris(self.sys_camera.projection, self.sys_camera.view_matrix)
        self.draw_ocean(time, self.sys_camera.projection, self.sys_camera.view_matrix)

    def draw_ocean(self, time, m_proj, m_mv):

        m = self.create_transformation(translation=Vector3([0.0, 12.0, 0.0]))
        m_mv = matrix44.multiply(m, m_mv)
        m_normal = self.create_normal_matrix(m_mv)

        self.ocean.bind(self.ocean_shader)
        self.ocean_shader.uniform_mat4("m_proj", m_proj)
        self.ocean_shader.uniform_mat4("m_mv", m_mv)
        self.ocean_shader.uniform_mat3("m_normal", m_normal)
        self.ocean_shader.uniform_sampler_2d(0, "tex0", self.ocean_normals1)
        self.ocean_shader.uniform_sampler_2d(1, "tex1", self.ocean_normals2)
        self.ocean_shader.uniform_sampler_2d(2, "tex2", self.ocean_normals3)
        self.ocean_shader.uniform_sampler_2d(3, "tex3", self.ocean_surface)
        self.ocean_shader.uniform_1f("scroll0", time / 10.0)
        self.ocean_shader.uniform_1f("scroll1", time / 10.0)
        self.ocean_shader.uniform_1f("scroll2", time / 10.0)
        self.ocean.draw()

    def draw_floor(self, m_proj, m_mv):
        self.floor.bind(self.floor_shader)
        self.floor_shader.uniform_mat4("m_proj", m_proj)
        self.floor_shader.uniform_mat4("m_mv", m_mv)
        self.floor_shader.uniform_sampler_2d(0, "floor_map", self.floor_map)
        self.floor.draw()

    def draw_debris(self, m_proj, m_mv):
        GL.glEnable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)

        self.debris.bind(self.debris_shader)
        self.debris_shader.uniform_mat4("m_proj", m_proj)
        self.debris_shader.uniform_mat4("m_mv", m_mv)
        self.debris_shader.uniform_sampler_2d(0, "texture0", self.debris_texture)
        self.debris_shader.uniform_1f("size", 0.25)
        self.debris.draw(mode=GL.GL_POINTS)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)


def generate_debris():
    # FIXME: Just geometry?
    size = 1280
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


def rnd_in_float(range_start, range_end):
    rng = range_end - range_start
    rnd = 0.0001 * (random.randint(0, 4294967296) % 10000)
    return range_start + math.fmod(rnd, rng)
