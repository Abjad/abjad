# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondLiteral(AbjadValueObject):
    r'''LilyPond literal.

    ::

        >>> import abjad

    ..  container:: example

        Dotted slur:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> slur = abjad.Slur()
            >>> abjad.attach(slur, staff[:])
            >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
            >>> abjad.attach(literal, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \slurDotted
                c'8 (
                d'8
                e'8
                f'8 )
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot',
        '_name',
        )

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(self, name=None, format_slot=None):
        name = name or 'foo'
        format_slot = format_slot or 'opening'
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond literal.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._get_lilypond_format()
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.name)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        names = []
        if not self.format_slot == 'opening':
            names.append('format_slot')
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=[self.name],
            storage_format_kwargs_names=names,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return self.name

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        format_slot.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

                >>> for slot in abjad.LilyPondLiteral.list_allowable_format_slots():
                ...     slot
                ...
                'after'
                'before'
                'closing'
                'opening'
                'right'

        Returns tuple.
        '''
        return LilyPondLiteral._allowable_format_slots

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self):
        r'''Gets format slot of LilyPond literal.

        ..  container:: example

            ::

                >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
                >>> literal.format_slot
                'opening'

        Defaults to `'opening'`.

        Returns string.
        '''
        return self._format_slot

    @property
    def name(self):
        r'''Gets name of LilyPond literal.

        ..  container:: example

            ::

                >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
                >>> literal.name
                '\\slurDotted'

        Returns string.
        '''
        return self._name
