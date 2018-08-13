# Auto generated settings file
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True
}

WINDOW = {
    "class": "demosys.context.pyqt.Window",
    "size": (1280, 720),
    "fullscreen": False,
    "resizable": True,
    "title": "demosys-py",
    "vsync": True,
    "cursor": True,
}

MUSIC = os.path.join(PROJECT_DIR, 'resources/music/sim_life_128.ogg')

# TIMER = 'demosys.timers.Timer'
# TIMER = 'demosys.timers.MusicTimer'
TIMER = 'demosys.timers.rocketmusic.Timer'

PROJECT = 'simlife.project.Project'

ROCKET = {
    # 'mode': 'editor',
    'mode': 'project',
    # 'mode': 'files',
    'rps': 20,  # row_rate from the old demo
    'project': os.path.join(PROJECT_DIR, 'resources/tracks.xml'),
    'files': os.path.join(PROJECT_DIR, 'resources/tracks'),
}

PROGRAM_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/programs'),
)

TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/textures'),
)
