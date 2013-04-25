from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import specifiers
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest


class InstrumentSpecifierEditor(ParameterSpecifierEditor):

    #def __init__(self, instruments=None, session=None, target=None):
    def __init__(self, instruments=None, session=None, target=None):
        ParameterSpecifierEditor.__init__(self, session=session, target=target)
        #self.instruments = instruments or []

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(specifiers.InstrumentSpecifier,
        ('name', 'nm', getters.get_string),
        ('instrument', 'st', wizards.InstrumentSelectionWizard),
        target_attribute_name='name',
        )

    ### READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        try:
            return self.target.instrument.name
        except AttributeError:
            pass

    ### PUBLIC METHODS ###

#    def menu_key_to_delegated_editor_kwargs(self, menu_key):
#        kwargs = {}
#        if menu_key == 'st':
#            kwargs['instruments'] = self.instruments
#        return kwargs
