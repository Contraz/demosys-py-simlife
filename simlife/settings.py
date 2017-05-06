# Auto generated settings file
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True
}

WINDOW = {
    # "size": (1920, 1080),
    # "size": (800, 420),
    "size": (1024, 576),
    # "size": (1280, 720),
    "fullscreen": False,
    "resizable": True,
    "title": "demosys-py",
    "vsync": True,
    "cursor": True,
}

MUSIC = os.path.join(PROJECT_DIR, 'resources/music/sim_life_128.mp3')

# TIMER = 'demosys.timers.Timer'
# TIMER = 'demosys.timers.MusicTimer'
TIMER = 'demosys.timers.RocketTimer'

ROCKET = {
    # 'mode': 'editor',
    'mode': 'project',
    # 'mode': 'files',
    'rps': 24,
    'project': os.path.join(PROJECT_DIR, 'resources/tracks.xml'),
    'files': os.path.join(PROJECT_DIR, 'resources/tracks'),
}

EFFECTS = (
    'simlife.underwater',
)

EFFECT_MANAGER = 'demosys.effects.managers.SingleEffectManager'

SHADER_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/shaders'),
)

SHADER_FINDERS = (
    "demosys.core.shaderfiles.finders.FileSystemFinder",
    "demosys.core.shaderfiles.finders.EffectDirectoriesFinder")

TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/textures'),
)

TEXTURE_FINDERS = (
    "demosys.core.texturefiles.finders.FileSystemFinder",
    "demosys.core.texturefiles.finders.EffectDirectoriesFinder")
