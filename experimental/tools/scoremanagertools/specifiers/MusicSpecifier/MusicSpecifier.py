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
        'from abjad.tools import indicatortools',
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

    @property
    def _repr_specification(self):
        return self._storage_format_specification.__makenew__(
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(
                'custom_identifier',
                'description',
                ),
            positional_argument_values=(
                list(self),
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.music_specifier_name or 'music specifier'
