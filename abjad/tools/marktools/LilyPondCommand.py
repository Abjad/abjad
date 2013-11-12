# -*- encoding: utf-8 -*-
import copy
from abjad.tools.marktools.Mark import Mark


# TODO: extend LilyPond command marks to attach to spanners.
class LilyPondCommand(Mark):
    r'''A LilyPond command.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.Slur()
        >>> attach(slur, staff.select_leaves())

    ::

        >>> command = marktools.LilyPondCommand('slurDotted')
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
    or from another LilyPond command mark with format slot.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_format_slot',
        )

    ### INITIALIZER ###

    def __init__(self,  *args):
        Mark.__init__(self)
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.name = copy.copy(args[0].name)
            self.format_slot = copy.copy(args[0].format_slot)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.name = copy.copy(args[0])
            self.format_slot = None
        elif len(args) == 2 and isinstance(args[0], type(self)):
            self.name = copy.copy(args[0].name)
            self.format_slot = args[1]
        elif len(args) == 2 and not isinstance(args[0], type(self)):
            self.name = args[0]
            self.format_slot = args[1]
        else:
            message = 'can not initialize LilyPond command.'
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies LilyPond command.

        Returns new LilyPond command.
        '''
        new = type(self)(self._name)
        new.format_slot = self.format_slot
        return new

    def __eq__(self, arg):
        r'''True when `arg` is a LilyPond command with name equal to
        LilyPond command. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._name == arg._name
        return False

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

    @apply
    def name():
        def fget(self):
            r'''Gets and sets name of LilyPond command.

            ::

                >>> command = marktools.LilyPondCommand('slurDotted')
                >>> command.name
                'slurDotted'

            Sets name of LilyPond command:

            ::

                >>> command.name = 'slurDashed'
                >>> command.name
                'slurDashed'

            Returns string.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, str)
            self._name = name
        return property(**locals())

    @apply
    def format_slot():
        def fget(self):
            '''Gets and sets format slot of LilyPond command.

            ::

                >>> note = Note("c'4")
                >>> command = marktools.LilyPondCommand('break', 'after')
                >>> command.format_slot
                'after'

            Sets format slot of LiyPond command:

            ::

                >>> note = Note("c'4")
                >>> command = marktools.LilyPondCommand('break', 'after')
                >>> command.format_slot = 'before'
                >>> command.format_slot
                'before'

            Set to ``'before'``, ``'after'``, ``'opening'``,
            ``'closing'``, ``'right'`` or none.
            '''
            return self._format_slot
        def fset(self, format_slot):
            assert format_slot in (
                'before', 'after', 'opening', 'closing', 'right', None)
            if format_slot is None:
                self._format_slot = 'opening'
            else:
                self._format_slot = format_slot
        return property(**locals())
