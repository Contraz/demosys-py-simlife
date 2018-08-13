from demosys.project.base import BaseProject


class Project(BaseProject):
    effect_packages = [
        'simlife.underwater',
    ]

    def create_resources(self):
        pass

    def create_effect_instances(self):
        pass
