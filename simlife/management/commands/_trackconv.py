import os
import struct
import xml.etree.ElementTree as ET
from xml.dom import minidom

path = "/Users/einarforselv/Documents/projects/contraz/demos/SimLife/resources/tracks"

# Shorten effect names (group names in rocket)
EFFECT_NAMES = {
    'underwater_effect': 'underwater',
    'glow_effect': 'glow',
    'fluid_effect': 'fluid',
    'camera': 'camera',
    'credits_effect': 'credits',
    'particle_creatures2_effect': 'creatures2',
    'particle_creatures_effect': 'creatures',
    'postprocess_effect': 'postprocess',
    'radial_blur_effect': 'radial',
    'effect': 'effect',
}

TRACK_NAMES = {
}

# demosys to rocket interpolation types
INTERPOLATION = {
    0: 1,  # KF_IT_LINEAR = LINEAR
    1: 2,  # KF_IT_COS_UP = SMOOTH
    2: 2,  # KF_IT_COS_DOWN = SMOOTH
    3: 0,  # FK_IT_STEP = STEP
    4: 3,  # KF_IT_RAMP = RAMP
}


def process_files():
    """Look for tracks and convert them"""
    files = os.listdir(path)
    tracks = TrackDocument()
    for f in files:
        if not f.endswith(".track"):
            continue

        s = f.split(".")
        if len(s) == 2:
            print("StartStop", s[0])
            track = crate_start_stop_track(
                os.path.join(path, f),
                EFFECT_NAMES[s[0]],
            )
        elif len(s) == 3:
            print("KeyFrames", s[0], s[1])
            track = create_keyframe_track(
                os.path.join(path, f),
                EFFECT_NAMES[s[0]],
                s[1],
            )
        else:
            raise ValueError("Not a recognized track type: {}".format(s[1]))

        if track.keyframes:
            tracks.add(track)

    return tracks


def crate_start_stop_track(path, effect):
    """Convert StartStop track to rocket"""
    with open(path, 'rb') as fd:
        priority = struct.unpack('<i', fd.read(4))[0]
        # print("priority:", priority)

        count = struct.unpack('<i', fd.read(4))[0]
        # print("count:", count)

        t = Track("ctrl:{}".format(effect))
        if effect is None:
            raise ValueError

        for i in range(count):
            row = struct.unpack('i', fd.read(4))[0]
            action = struct.unpack('i', fd.read(4))[0]
            if action == 1:
                name = read_string(fd)
                # print("name", name)

            # print("row={}, action={}".format(row, action))
            # Add a step keyframe
            t.add(KeyFrame(row, action, 0))

    return t


def create_keyframe_track(path, effect, name):
    """Convert interpolation track to rocket"""
    t = Track("{}:{}".format(effect, name))
    with open(path, 'rb') as fd:
        count = struct.unpack('i', fd.read(4))[0]
        # print("count={}".format(count))
        for i in range(count):
            row = struct.unpack('i', fd.read(4))[0]
            kind = struct.unpack('i', fd.read(4))[0]
            value = struct.unpack('f', fd.read(4))[0]
            # print("row={}, kind={}, value={}".format(row, kind, value))
            t.add(KeyFrame(row, value, INTERPOLATION.get(kind)))

    return t


class TrackDocument:
    """All tracks"""
    def __init__(self):
        self.tracks = []

    def add(self, track):
        self.tracks.append(track)

    def save(self, dest):
        root = ET.Element("tracks")
        for track in self.tracks:
            t = ET.SubElement(root, "track", name=track.name)
            for kf in track.keyframes:
                ET.SubElement(t, 'key', row=str(kf.row), value=str(kf.value), interpolation=str(kf.kind))

        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        with open(dest, 'w') as fd:
            fd.write(reparsed.toprettyxml(indent="  "))


class Track:
    """A track containing keyframes"""
    def __init__(self, name):
        self.name = name
        self.keyframes = []

    def add(self, kf):
        self.keyframes.append(kf)


class KeyFrame:
    """Keyframe"""
    def __init__(self, row, value, kind):
        self.row = row
        self.value = value
        self.kind = kind


# --- Utils ---

def read_string(fd):
    """Read null-terminated string"""
    chars = []
    while True:
        c = fd.read(1)
        # print(c)
        if c == b'\x00' or c == b'':
            return "".join(chars)
        chars.append(c.decode())
