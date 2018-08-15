from demosys.effects import Effect
from demosys import geometry


class CreditsEffect(Effect):
    runnable = True

    def __init__(self):
        # Info for rocket timeline
        self.rocket_timeline_track = self.get_track("ctrl:credits")
        self.rocket_timeline_order = 10

        # Textures
        self.binf_texture = self.get_texture('binf')
        self.dran_texture = self.get_texture('dran')
        self.enex_texture = self.get_texture('enex')
        self.phlaton_texture = self.get_texture('phlaton')
        self.contrazlogo_texture = self.get_texture('contrazlogo')
        self.simlifelogo_texture = self.get_texture('simlifelogo')

        self.binf_texture.repeat_x, self.binf_texture.repeat_y = False, False
        self.dran_texture.repeat_x, self.dran_texture.repeat_y = False, False
        self.enex_texture.repeat_x, self.enex_texture.repeat_y = False, False
        self.phlaton_texture.repeat_x, self.phlaton_texture.repeat_y = False, False
        self.contrazlogo_texture.repeat_x, self.contrazlogo_texture.repeat_y = False, False
        self.simlifelogo_texture.repeat_x, self.simlifelogo_texture.repeat_y = False, False

        self.textures = {
            0: self.binf_texture,
            1: self.dran_texture,
            2: self.enex_texture,
            3: self.phlaton_texture,
            4: self.contrazlogo_texture,
            5: self.simlifelogo_texture,
        }

        self.track_index = self.get_track("credits:index")
        self.track_xpos = self.get_track("credits:xpos")
        self.track_ypos = self.get_track("credits:ypos")
        self.track_scale = self.get_track("credits:scale")
        self.track_alpha = self.get_track("credits:alpha")

        self.screen_program = self.get_program("credits")
        self.quad_fs = geometry.quad_fs()

    def draw(self, time, frametime, target):
        index = int(self.track_index.time_value(time))
        texture = self.textures.get(index)

        if not texture:
            return

        scale = self.track_scale.time_value(time)

        # FIXME: Needs to screen blend with staging fbo
        texture.use(location=0)
        self.screen_program['source0'].value = 0
        self.screen_program['source1'].value = 0
        self.screen_program['source0_opacity'].value = self.track_alpha.time_value(time)
        self.screen_program['source1_opacity'].value = 1.0
        self.screen_program['position'].value = (self.track_xpos.time_value(time),
                                                 self.track_ypos.time_value(time))
        self.screen_program['scale'].value = (scale, scale * 5)
        self.quad_fs.render(self.screen_program)
