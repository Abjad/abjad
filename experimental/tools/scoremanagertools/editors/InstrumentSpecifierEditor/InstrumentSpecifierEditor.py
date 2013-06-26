from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest


class InstrumentSpecifierEditor(ParameterSpecifierEditor):

    def __init__(self, instruments=None, session=None, target=None):
        ParameterSpecifierEditor.__init__(
            self, session=session, target=target)

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        specifiers.InstrumentSpecifier,
        ('name', 'nm', getters.get_string),
        ('instrument', 'st', wizards.InstrumentSelectionWizard),
        target_attribute_name='name',
        )

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        try:
            return self.target.instrument.name
        except AttributeError:
            pass
