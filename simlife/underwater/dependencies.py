from demosys.resources.meta import TextureDescription, ProgramDescription

effect_packages = []

resources = [
    TextureDescription(label="debris", path='underwater/debris.png'),
    ProgramDescription(label="debris", path='underwater/debris.glsl'),

    ProgramDescription(label="floor", path="underwater/floor.glsl"),
    TextureDescription(label="floor", path="underwater/floor_map.png"),

    ProgramDescription(label="ocean", path="underwater/ocean.glsl"),
    TextureDescription(label="OceanSurface", path="underwater/OceanSurface.png"),
    TextureDescription(label="Waves1Normals", path="underwater/Waves1Normals.png"),
    TextureDescription(label="Waves2Normals", path="underwater/Waves2Normals.png"),
    TextureDescription(label="Waves3Normals", path="underwater/Waves3Normals.png"),

    ProgramDescription(label="texture_fs", path='texture_fs.glsl'),
    ProgramDescription(label="laplacian", path='underwater/laplacian.glsl'),
    ProgramDescription(label="dilate", path='underwater/dilate.glsl'),

    ProgramDescription(label="creature", path="underwater/creature.glsl"),
]
