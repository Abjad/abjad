# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from experimental.tools.scoremanagertools.specifiers.Specifier import Specifier
from experimental.tools.scoremanagertools.specifiers.ArticulationSpecifier \
    import ArticulationSpecifier


class MusicContributionSpecifier(Specifier, TypedList):

    def __init__(
        self,
        parameter_specifiers,
        description=None,
        custom_identifier=None,
        source=None,
        ):
        TypedList.__init__(self, parameter_specifiers)
        Specifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self._articulations = ArticulationSpecifier

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or 'unknown contribution'

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
    def articulations(self):
        return self._articulations

    @property
    def directives(self):
        return self._directives
