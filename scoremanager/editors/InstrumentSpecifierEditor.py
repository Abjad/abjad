# -*- encoding: utf-8 -*-
from scoremanager.editors.SpecifierEditor import SpecifierEditor 


class InstrumentSpecifierEditor(SpecifierEditor):

    ### CLASS VARIABLES ###

    @property
    def target_manifest(self):
        from scoremanager import getters
        from scoremanager import specifiers
        from scoremanager import wizards
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
        SpecifierEditor.__init__(
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
