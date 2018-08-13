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
TIMER = 'demosys.timers.rocket.Timer'

PROJECT = 'simlife.project.Project'

ROCKET = {
    # 'mode': 'editor',
    'mode': 'project',
    # 'mode': 'files',
    'rps': 24,
    'project': os.path.join(PROJECT_DIR, 'resources/tracks.xml'),
    'files': os.path.join(PROJECT_DIR, 'resources/tracks'),
}

PROGRAM_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/programs'),
)

TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/textures'),
)
