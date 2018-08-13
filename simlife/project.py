from demosys.project.base import BaseProject


class Project(BaseProject):
    effect_packages = [
        'simlife.underwater',
    ]

    def get_default_effect(self):
        return self.get_effect('underwater')

    def create_resources(self):
        pass

    def create_effect_instances(self):
        self.create_effect('underwater', 'UnderWaterEffect')
