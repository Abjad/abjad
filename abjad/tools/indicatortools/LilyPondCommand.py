# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondCommand(AbjadValueObject):
    r'''A LilyPond command.

    ..  container:: example

        **Example 1.** Dotted slur:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> slur = spannertools.Slur()
            >>> attach(slur, staff[:])
            >>> command = indicatortools.LilyPondCommand('slurDotted')
            >>> attach(command, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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
        '_default_scope',
        '_format_slot',
        '_name',
        '_prefix',
        )

    _format_leaf_children = False

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    ### INITIALIZER ###

    def __init__(self, name=None, format_slot=None, prefix='\\'):
        self._default_scope = None
        name = name or 'slurDotted'
        format_slot = format_slot or 'opening'
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot
        assert isinstance(prefix, str), repr(prefix)
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond command.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        format_slot = lilypond_format_bundle.get(self.format_slot)
        format_slot.commands.append(self._lilypond_format)
        return lilypond_format_bundle

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

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

            **Example 1.** Default:

                >>> commands = indicatortools.LilyPondCommand.list_allowable_format_slots()
                >>> for command in commands:
                ...     command
                'after'
                'before'
                'closing'
                'opening'
                'right'

        Returns tuple of strings.
        '''
        return LilyPondCommand._allowable_format_slots

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.name)

    @property
    def _lilypond_format(self):
        command = self._name
        if command.startswith('#'):
            return command
        elif ' ' not in command:
            return self.prefix + stringtools.to_lower_camel_case(command)
        else:
            return self.prefix + command

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of LilyPond command.

        ..  container:: example

            **Example 1.** Dotted slur:

            ::

                >>> command = indicatortools.LilyPondCommand('slurDotted')
                >>> command.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def format_slot(self):
        r'''Gets format slot of LilyPond command.

        ..  container:: example

            **Example 1.** Dotted slur:

            ::

                >>> command = indicatortools.LilyPondCommand('slurDotted')
                >>> command.format_slot
                'opening'

        Defaults to `'opening'`.

        Returns string.
        '''
        return self._format_slot

    @property
    def name(self):
        r'''Gets name of LilyPond command.

        ..  container:: example

            **Example 1.** Dotted slur:

            ::

                >>> command = indicatortools.LilyPondCommand('slurDotted')
                >>> command.name
                'slurDotted'

        Returns string.
        '''
        return self._name

    @property
    def prefix(self):
        r'''Gets prefix.

        Defaults to `'\\'`.

        Set to string.

        Returns string.
        '''
        return self._prefix
