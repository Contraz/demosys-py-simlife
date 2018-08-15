from demosys.project.base import BaseProject
from demosys import context
from demosys.timeline.rocket import Timeline
from demosys.resources.meta import ProgramDescription


class Project(BaseProject):
    effect_packages = [
        'simlife.underwater',
        'simlife.credits',
    ]
    resources = [
    ]

    def get_default_effect(self):
        return self.get_effect('underwater')

    def create_effect_instances(self):
        self.create_effect('underwater', 'UnderWaterEffect')
        self.create_effect('credits', 'CreditsEffect')

        context.window().timeline = Timeline(self)
