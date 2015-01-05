# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


# TODO: extend to attach to spanners
class LilyPondCommand(AbjadValueObject):
    r'''A LilyPond command.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.Slur()
        >>> attach(slur, staff.select_leaves())

    ::

        >>> command = indicatortools.LilyPondCommand('slurDotted')
        >>> attach(command, staff[0])

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> show(staff) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot',
        '_name',
        )

    _format_leaf_children = False

    _valid_format_slots = (
        'before',
        'after',
        'opening',
        'closing',
        'right',
        )

    ### INITIALIZER ###

    def __init__(self, name=None, format_slot=None):
        name = name or 'slurDotted'
        format_slot = format_slot or 'opening'
        assert format_slot in self._valid_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats LilyPond command.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
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

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.name)

    @property
    def _lilypond_format(self):
        from abjad.tools import stringtools
        command = self._name
        if command.startswith('#'):
            return command
        elif ' ' not in command:
            return '\\' + stringtools.to_lower_camel_case(command)
        else:
            return '\\' + command

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            self.name,
            )
        keyword_argument_names = ()
        if not self.format_slot == 'opening':
            keyword_argument_names = (
                'format_slot',
                )
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self):
        r'''Gets format slot of LilyPond command.

        ::

            >>> command.format_slot
            'opening'

        Returns string.
        '''
        return self._format_slot


    @property
    def name(self):
        r'''Gets name of LilyPond command.

        ::

            >>> command.name
            'slurDotted'

        Returns string.
        '''
        return self._name