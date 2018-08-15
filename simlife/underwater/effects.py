import moderngl
import random
import math
import numpy

from pyrr import Vector3, matrix44

from demosys.effects import Effect
from demosys.opengl.vao import VAO
from demosys import geometry
from demosys.scene.camera import Camera


class UnderWaterEffect(Effect):
    runnable = True

    def __init__(self):
        # Read by rocket timeline externally
        self.rocket_timeline_track = self.get_track('ctrl:underwater')
        self.rocket_timeline_order = 0

        mesh_size = 400
        self.floor = geometry.plane_xz(size=(mesh_size, mesh_size), resolution=(128, 128))
        self.floor_shader = self.get_program("floor")
        self.floor_map = self.get_texture("floor")
        self.floor.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.ocean = geometry.plane_xz(size=(mesh_size, mesh_size), resolution=(64, 64))
        self.ocean_shader = self.get_program('ocean')
        self.ocean_surface = self.get_texture('OceanSurface')
        self.ocean_normals1 = self.get_texture('Waves1Normals')
        self.ocean_normals2 = self.get_texture('Waves2Normals')
        self.ocean_normals3 = self.get_texture('Waves3Normals')

        # postprocess
        self.quad_fs = geometry.quad_fs()
        self.texture_shader = self.get_program('texture_fs')
        self.laplacian_shader = self.get_program('laplacian')
        self.dilate_shader = self.get_program('dilate')

        self.cam = Camera(fov=75, near=1, far=500, aspect=self.window.aspect_ratio)

        self.init_fbos()
        self.init_tracks()

        self.debris = DebrisEffect()
        self.creatures = CreaturesEffect()

    def init_fbos(self):
        color_layer = self.ctx.texture(self.window.buffer_size, 4)
        color_layer.repeat_x = False
        color_layer.repeat_y = False
        self.offscreen0 = self.ctx.framebuffer(
            color_layer,
            depth_attachment=self.ctx.depth_texture(self.window.buffer_size),
        )

        color_layer = self.ctx.texture(self.window.buffer_size, 4)
        color_layer.repeat_x = False
        color_layer.repeat_y = False
        self.offscreen1 = self.ctx.framebuffer(
            color_layer,
            depth_attachment=self.ctx.depth_texture(self.window.buffer_size),
        )

    def init_tracks(self):
        # Tracks: Camera
        self.cam_pitch = self.get_track("camera:pitch")
        self.cam_yaw = self.get_track("camera:head")
        self.cam_x = self.get_track("camera:x")
        self.cam_y = self.get_track("camera:y")
        self.cam_z = self.get_track("camera:z")

    def draw(self, time, frametime, target):
        self.ctx.enable_only(moderngl.DEPTH_TEST)
        self.offscreen0.clear()
        self.offscreen1.clear()

        # Get camera position from tracks
        self.cam.position = Vector3([self.cam_x.time_value(time),
                                     self.cam_y.time_value(time),
                                     self.cam_z.time_value(time)])
        self.cam.pitch = -self.cam_pitch.time_value(time)
        self.cam.yaw = self.cam_yaw.time_value(time) - 90
        m_mv = self.cam.view_matrix

        # Draw the floor and ocean
        self.offscreen0.use()
        self.draw_floor(self.cam.projection.matrix, m_mv)
        self.draw_ocean(time, self.cam.projection.matrix, m_mv)
        target.use()

        self.ctx.disable(moderngl.DEPTH_TEST)

        # Postprocessing - Laplace
        self.offscreen1.use()
        self.offscreen0.color_attachments[0].use(location=0)
        self.laplacian_shader["texture0"].value = 0
        self.laplacian_shader["viewportStep"].value = 1.0 / 1024.0
        self.laplacian_shader["contrast"].value = 2.0
        self.laplacian_shader["color"].value = (1.0, 1.0, 1.0)
        self.quad_fs.render(self.laplacian_shader)
        target.use()

        # Postprocessing - Dilate
        self.offscreen1.color_attachments[0].use(location=0)
        self.dilate_shader["texture0"].value == 0
        self.dilate_shader["viewportStep"].value = 1.0 / 1024.0
        self.quad_fs.render(self.dilate_shader)

        # Draw debris and creatures
        self.debris.draw(self.cam.projection.matrix, m_mv)
        self.creatures.draw(time, self.cam.projection.matrix, m_mv)

    def draw_ocean(self, time, m_proj, m_mv):
        """Draw the ocean surface"""
        m = self.create_transformation(translation=Vector3([0.0, 12.0, 0.0]))
        m_mv = matrix44.multiply(m, m_mv)
        m_normal = self.create_normal_matrix(m_mv)

        shader = self.ocean_shader
        shader["m_proj"].write(m_proj.astype('f4').tobytes())
        shader["m_mv"].write(m_mv.astype('f4').tobytes())
        shader["m_normal"].write(m_normal.astype('f4').tobytes())

        self.ocean_normals1.use(location=0)
        shader["tex0"].value = 0
        self.ocean_normals2.use(location=1)
        shader["tex1"].value = 1
        self.ocean_normals3.use(location=2)
        shader["tex2"].value = 2
        self.ocean_surface.use(location=3)
        shader["tex3"].value = 3

        shader["scroll0"].value = 0.02 * time
        shader["scroll1"].value = 0.10 * time
        shader["scroll2"].value = 0.04 * time
        self.ocean.render(shader)

    def draw_floor(self, m_proj, m_mv):
        """Draw the ocean floor terrain"""
        self.floor_shader["m_proj"].write(m_proj.astype('f4').tobytes())
        self.floor_shader["m_mv"].write(m_mv.astype('f4').tobytes())
        self.floor_map.use(location=0)
        self.floor_shader["floor_map"].value = 0
        self.floor.render(self.floor_shader)


class CreaturesEffect(Effect):
    runnable = False

    def __init__(self):
        self.creature = geometry.cube(2.0, 2.0, 2.0)
        self.creature_shader = self.get_program("creature")

        # Tracks: Creatures
        self.creature1_pos_x = self.get_track("creatures1:pos_x")
        self.creature1_pos_y = self.get_track("creatures1:pos_y")
        self.creature1_pos_z = self.get_track("creatures1:pos_z")

        self.creature2_pos_x = self.get_track("creatures2:pos_x2")
        self.creature2_pos_y = self.get_track("creatures2:pos_y2")
        self.creature2_pos_z = self.get_track("creatures2:pos_z2")

    def draw(self, time, m_proj, m_mv):
        trans = matrix44.create_from_translation(
            Vector3([
                self.creature1_pos_x.time_value(time),
                self.creature1_pos_y.time_value(time),
                self.creature1_pos_z.time_value(time)
            ])
        )
        m_mv = matrix44.multiply(trans, m_mv)
        m_normal = self.create_normal_matrix(m_mv)

        self.creature_shader["m_proj"].write(m_proj.astype('f4').tobytes())
        self.creature_shader["m_mv"].write(m_mv.astype('f4').tobytes())
        self.creature_shader["m_normal"].write(m_normal.astype('f4').tobytes())
        self.creature.render(self.creature_shader)

        trans = matrix44.create_from_translation(
            Vector3([
                self.creature2_pos_x.time_value(time),
                self.creature2_pos_y.time_value(time),
                self.creature2_pos_z.time_value(time)
            ])
        )
        m_mv = matrix44.multiply(trans, m_mv)
        m_normal = self.create_normal_matrix(m_mv)

        self.creature_shader["m_proj"].write(m_proj.astype('f4').tobytes())
        self.creature_shader["m_mv"].write(m_mv.astype('f4').tobytes())
        self.creature_shader["m_normal"].write(m_normal.astype('f4').tobytes())
        self.creature.render(self.creature_shader)


class DebrisEffect(Effect):
    """Draws debris particles"""
    runnable = False

    def __init__(self):
        self.debris = self.generate_debris()
        self.debris_texture = self.get_texture('debris')
        self.debris_shader = self.get_program('debris')

    def draw(self, m_proj, m_mv):
        """Draw debris particles"""
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE)

        self.debris_shader["m_proj"].write(m_proj.astype('f4').tobytes())
        self.debris_shader["m_mv"].write(m_mv.astype('f4').tobytes())
        self.debris_texture.use(location=0)
        self.debris_shader["texture0"].value = 0
        self.debris_shader["size"].value = 0.25
        self.debris.render(self.debris_shader, mode=moderngl.POINTS)

        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.disable(moderngl.BLEND)

    def generate_debris(self):
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

        position_vbo = numpy.array(positions, dtype=numpy.float32)
        color_vbo = numpy.array(colors, dtype=numpy.float32)

        vao = VAO("debris")
        vao.buffer(position_vbo, '3f', 'in_position')
        vao.buffer(color_vbo, '3f', 'in_color')

        return vao


def rnd_in_float(range_start, range_end):
    rng = range_end - range_start
    rnd = 0.0001 * (random.randint(0, 4294967296) % 10000)
    return range_start + math.fmod(rnd, rng)
