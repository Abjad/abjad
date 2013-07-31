# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.scoremanagertools.specifiers.MusicContributionSpecifier \
    import MusicContributionSpecifier
from experimental.tools.scoremanagertools.specifiers.Specifier \
    import Specifier


class MusicSpecifier(Specifier, ObjectInventory):

    ### CLASS VARIABLES ###

    storage_module_import_statements = [
        'from abjad import *',
        'from abjad.tools import contexttools',
        'from abjad.tools import durationtools',
        'from experimental.tools.scoremanagertools import specifiers',
        ]

    ### INITIALIZER ###

    def __init__(
        self,
        contributions=None,
        description=None,
        name=None,
        source=None,
        ):
        contributions = contributions or []
        ObjectInventory.__init__(self, contributions)
        Specifier.__init__(
            self,
            description=description,
            name=name,
            source=source,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_class(self):
        return MusicContributionSpecifer

    @property
    def _keyword_argument_names(self):
        r'''Is there a way to do this programmatically?
        '''
        return tuple(sorted([
            'description',
            'name',
            ]))

    ### PUBLIC PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
