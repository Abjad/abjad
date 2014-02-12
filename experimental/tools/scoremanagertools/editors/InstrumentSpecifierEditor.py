# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor 


class InstrumentSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    @property
    def target_manifest(self):
        from scoremanagertools import specifiers
        return self.TargetManifest(
            specifiers.InstrumentSpecifier,
            ('custom_identifier', 'id', getters.get_string),
            ('instrument', 'st', wizards.InstrumentSelectionWizard),
            target_attribute_name='name',
            )

    ### INITIALIZER ###

    def __init__(
        self,
        instruments=None,
        session=None,
        target=None,
        ):
        ParameterSpecifierEditor.__init__(
            self, 
            session=session,
            target=target,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        try:
            return self.target.instrument.name
        except AttributeError:
            pass
