from demosys.resources.meta import TextureDescription, ProgramDescription

effect_packages = []

resources = [
    TextureDescription(label="binf", path='credits/Binf.png'),
    TextureDescription(label="dran", path='credits/Dran.png'),
    TextureDescription(label="contrazlogo", path='credits/ContrazLogo.png'),
    TextureDescription(label="enex", path='credits/Enex.png'),
    TextureDescription(label="phlaton", path='credits/Phlaton.png'),
    TextureDescription(label="simlifelogo", path='credits/SimLifeLogo.png'),

    ProgramDescription(label="credits", path="credits/credits.glsl"),
]
