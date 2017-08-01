# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TypedCounter import TypedCounter


class RotationCounter(TypedCounter):
    r'''Rotation counter.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmmakertools

    ..  container:: example

        ::

            >>> counter = rhythmmakertools.RotationCounter(default=3)

        ::

            >>> counter['talea__counts']
            3

        ::

            >>> counter['talea__counts'] += 1
            >>> counter['talea__counts']
            4

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_autoincrement',
        '_default',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        autoincrement=None,
        default=None,
        items=None,
        **keywords
        ):
        TypedCounter.__init__(
            self,
            items=items,
            **keywords
            )
        if autoincrement is not None:
            autoincrement = bool(autoincrement)
        self._autoincrement = autoincrement
        if default is not None:
            default = int(default or 0)
        self._default = default

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        Returns item or slice.
        '''
        argument = self._item_coercer(argument)
        if argument not in self._collection:
            self._collection[argument] = self._default or 0
        return self._collection.__getitem__(argument)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        names.extend(sorted(self._collection.keys()))
        if 'items' in names:
            names.remove('items')
        if not self.autoincrement:
            names.remove('autoincrement')
        return systemtools.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[],
            storage_format_kwargs_names=names,
            template_names=names,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def autoincrement(self):
        r'''Is true if rotation counter should be auto-incremented.
        Otherwise false.

        Returns true or false.
        '''
        return self._autoincrement

    @property
    def default(self):
        r'''Gets default count.

        Returns integer.
        '''
        return self._default
