# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: extend LilyPond command marks to attach to spanners.
class LilyPondCommand(AbjadObject):
    r'''A LilyPond command.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.Slur()
        >>> attach(slur, staff.select_leaves())

    ::

        >>> command = indicatortools.LilyPondCommand('slurDotted')
        >>> attach(command, staff[0])

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Initialize LilyPond commands from name; or from name
    with format slot; or from another LilyPond command mark;
    or from another LilyPond command with format slot.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_format_slot',
        )

    _valid_format_slots = (
        'before', 
        'after', 
        'opening', 
        'closing', 
        'right',
        )

    ### INITIALIZER ###

    def __init__(self,  *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            name = copy.copy(args[0].name)
            format_slot = copy.copy(args[0].format_slot)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            name = copy.copy(args[0])
            format_slot = None
        elif len(args) == 2 and isinstance(args[0], type(self)):
            name = copy.copy(args[0].name)
            format_slot = args[1]
        elif len(args) == 2 and not isinstance(args[0], type(self)):
            name = args[0]
            format_slot = args[1]
        else:
            message = 'can not initialize LilyPond command from {!r}.'
            message = message.format(args)
            raise ValueError(message)
        format_slot = format_slot or 'opening'
        assert format_slot in self._valid_format_slots, repr(format_slot)
        assert isinstance(name, str), repr(name)
        self._name = name
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies LilyPond command.

        Returns new LilyPond command.
        '''
        new = type(self)(self._name)
        new.format_slot = self.format_slot
        return new

    def __eq__(self, arg):
        r'''True when `arg` is a LilyPond command with a name equal to
        that of this LilyPond command. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._name == arg._name
        return False

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
        else:
            return '\\' + stringtools.snake_case_to_lower_camel_case(command)

    ### PUBLIC PROPERTIES ###

    @property
    def format_slot(self):
        r'''Format slot of LilyPond command.

        ::

            >>> command.format_slot
            'opening'

        Returns string.
        '''
        return self._format_slot


    @property
    def name(self):
        r'''Name of LilyPond command.

        ::

            >>> command.name
            'slurDotted'

        Returns string.
        '''
        return self._name
