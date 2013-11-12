# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from experimental.tools.scoremanagertools.specifiers.MusicContributionSpecifier \
    import MusicContributionSpecifier
from experimental.tools.scoremanagertools.specifiers.Specifier \
    import Specifier


class MusicSpecifier(Specifier, TypedList):

    ### CLASS VARIABLES ###

    storage_module_import_statements = [
        'from abjad import *',
        'from abjad.tools import marktools',
        'from abjad.tools import durationtools',
        'from experimental.tools.scoremanagertools import specifiers',
        ]

    ### INITIALIZER ###

    def __init__(
        self,
        contributions=None,
        description=None,
        custom_identifier=None,
        source=None,
        ):
        contributions = contributions or []
        TypedList.__init__(self,
            tokens=contributions,
            item_class=MusicContributionSpecifier,
            )
        Specifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )

    ### PRIVATE PROPERTIES ###

#    @property
#    def _item_class(self):
#        return MusicContributionSpecifer

    @property
    def _keyword_argument_names(self):
        r'''Is there a way to do this programmatically?
        '''
        return tuple(sorted([
            'custom_identifier',
            'description',
            ]))

    ### PUBLIC PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
