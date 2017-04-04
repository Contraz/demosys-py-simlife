import random
import math
import numpy
from demosys.effects import effect
from demosys.opengl import VAO, FBO
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

        # postprocess
        self.quad_fs = geometry.quad_fs()
        self.texture_shader = self.get_shader('texture_fs.glsl')
        self.laplacian_shader = self.get_shader('underwater/laplacian.glsl')
        self.dilate_shader = self.get_shader('underwater/dilate.glsl')

        self.offscreen0 = FBO.create(1024, 1024, depth=True)
        self.offscreen1 = FBO.create(1024, 1024, depth=True)

    @effect.bind_target
    def draw(self, time, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        with self.offscreen0:
            self.draw_floor(self.sys_camera.projection, self.sys_camera.view_matrix)
            self.draw_ocean(time, self.sys_camera.projection, self.sys_camera.view_matrix)

        GL.glDisable(GL.GL_DEPTH_TEST)

        # Postprocessing
        # Laplace
        with self.offscreen1:
            with self.quad_fs.bind(self.laplacian_shader) as shader:
                shader.uniform_sampler_2d(0, "texture0", self.offscreen0.color_buffers[0])
                shader.uniform_1f("viewportStep", 1.0 / 1024.0)
                shader.uniform_1f("contrast", 2.0)
                shader.uniform_3f("color", 1.0, 1.0, 1.0)
            self.quad_fs.draw()

        # Dilate
        with self.quad_fs.bind(self.dilate_shader) as shader:
            shader.uniform_sampler_2d(0, "texture0", self.offscreen1.color_buffers[0])
            shader.uniform_1f("viewportStep", 1.0 / 1024.0)
        self.quad_fs.draw()

        # with self.quad_fs.bind(self.texture_shader) as shader:
        #     shader.uniform_sampler_2d(0, "texture0", self.offscreen1.color_buffers[0])
        # self.quad_fs.draw()

        self.draw_debris(self.sys_camera.projection, self.sys_camera.view_matrix)

        self.offscreen0.clear()
        self.offscreen1.clear()

    def draw_ocean(self, time, m_proj, m_mv):
        """Draw the ocean surface"""
        m = self.create_transformation(translation=Vector3([0.0, 12.0, 0.0]))
        m_mv = matrix44.multiply(m, m_mv)
        m_normal = self.create_normal_matrix(m_mv)

        with self.ocean.bind(self.ocean_shader) as shader:
            shader.uniform_mat4("m_proj", m_proj)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_mat3("m_normal", m_normal)
            shader.uniform_sampler_2d(0, "tex0", self.ocean_normals1)
            shader.uniform_sampler_2d(1, "tex1", self.ocean_normals2)
            shader.uniform_sampler_2d(2, "tex2", self.ocean_normals3)
            shader.uniform_sampler_2d(3, "tex3", self.ocean_surface)
            shader.uniform_1f("scroll0", 0.02 * time)
            shader.uniform_1f("scroll1", 0.10 * time)
            shader.uniform_1f("scroll2", 0.04 * time)
        self.ocean.draw()

    def draw_floor(self, m_proj, m_mv):
        """Draw the ocean floor terrain"""
        with self.floor.bind(self.floor_shader) as shader:
            shader.uniform_mat4("m_proj", m_proj)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_sampler_2d(0, "floor_map", self.floor_map)
        self.floor.draw()

    def draw_debris(self, m_proj, m_mv):
        """Draw debris particles"""
        GL.glEnable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)

        with self.debris.bind(self.debris_shader) as shader:
            shader.uniform_mat4("m_proj", m_proj)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_sampler_2d(0, "texture0", self.debris_texture)
            shader.uniform_1f("size", 0.25)
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
