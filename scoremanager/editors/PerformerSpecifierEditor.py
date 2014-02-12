# -*- encoding: utf-8 -*-
from scoremanager.editors.SpecifierEditor \
    import SpecifierEditor
from scoremanager.specifiers.PerformerSpecifier \
    import PerformerSpecifier
from scoremanager import iotools


class PerformerSpecifierEditor(SpecifierEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            PerformerSpecifier,
            ('performer', 'pf', iotools.Selector.make_performer_selector,)
            )

    @property
    def target_name(self):
        try:
            return self.target.performer.name
        except AttributeError:
            pass
