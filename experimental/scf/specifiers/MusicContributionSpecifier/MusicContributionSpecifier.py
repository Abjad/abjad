from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from scf.specifiers.Specifier import Specifier
from scf.specifiers.ArticulationSpecifier import ArticulationSpecifier


class MusicContributionSpecifier(Specifier, ObjectInventory):

    def __init__(self, parameter_specifiers, description=None, name=None, source=None):
        ObjectInventory.__init__(self, parameter_specifiers)
        Specifier.__init__(self, description=description, name=name, source=source)
        self._articulations = ArticulationSpecifier

    ### PIVATE READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or 'unknown contribution'

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def articulations(self):
        return self._articulations

    @property
    def directives(self):
        return self._directives
