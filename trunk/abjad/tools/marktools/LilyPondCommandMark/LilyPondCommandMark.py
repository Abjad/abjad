from abjad.tools.marktools.Mark import Mark
import copy


# TODO: extend LilyPond command marks to attach to spanners.
class LilyPondCommandMark(Mark):
    r'''.. versionadded:: 2.0

    LilyPond command mark::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)

    ::

        >>> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(staff[0])

    ::

        >>> f(staff)
        \new Staff {
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Initialize LilyPond command marks from command name; or from command name
    with format slot; or from another LilyPond command mark; or from another LilyPond
    command mark with format slot.

    LilyPond command marks implement ``__slots__``.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_command_name', '_format_slot', )

    ### INITIALIZER ###

    def __init__(self,  *args):
        Mark.__init__(self)
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.command_name = copy.copy(args[0].command_name)
            self.format_slot = copy.copy(args[0].format_slot)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.command_name = copy.copy(args[0])
            self.format_slot = None
        elif len(args) == 2 and isinstance(args[0], type(self)):
            self.command_name = copy.copy(args[0].command_name)
            self.format_slot = args[1]
        elif len(args) == 2 and not isinstance(args[0], type(self)):
            self.command_name = args[0]
            self.format_slot = args[1]
        else:
            raise ValueError('Can not initialize LilyPond command mark.')

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        #return type(self)(self._command_name)
        new = type(self)(self._command_name)
        new.format_slot = self.format_slot
        return new

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._command_name == arg._command_name
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.command_name)

    ### PUBLIC PROPERTIES ###

    @apply
    def command_name():
        def fget(self):
            '''Get command name of LilyPond command mark::

                >>> lilypond_command = marktools.LilyPondCommandMark('slurDotted')
                >>> lilypond_command.command_name
                'slurDotted'

            Set command name of LilyPond command mark::

                >>> lilypond_command.command_name = 'slurDashed'
                >>> lilypond_command.command_name
                'slurDashed'

            Set string.
            '''
            return self._command_name
        def fset(self, command_name):
            assert isinstance(command_name, str)
            self._command_name = command_name
        return property(**locals())

    @property
    def lilypond_format(self):
        '''Read-only LilyPond input format of LilyPond command mark::

            >>> note = Note("c'4")
            >>> lilypond_command = marktools.LilyPondCommandMark('slurDotted')(note)
            >>> lilypond_command.lilypond_format
            '\\slurDotted'

        Return string.
        '''
        from abjad.tools import stringtools
        command = self._command_name
        if command.startswith('#'):
            return command
        else:
            return '\\' + stringtools.underscore_delimited_lowercase_to_lowercamelcase(command)

    @apply
    def format_slot():
        def fget(self):
            '''.. versionadded:: 2.3

            Get format slot of LilyPond command mark::
            
                >>> note = Note("c'4")
                >>> lilypond_command = marktools.LilyPondCommandMark('break', 'after')
                >>> lilypond_command.format_slot
                'after'

            Set format slot of LiyPond command mark::

                >>> note = Note("c'4")
                >>> lilypond_command = marktools.LilyPondCommandMark('break', 'after')
                >>> lilypond_command.format_slot = 'before'
                >>> lilypond_command.format_slot
                'before'

            Set to ``'before'``, ``'after'``, ``'opening'``, ``'closing'``, ``'right'`` or none.
            '''
            return self._format_slot
        def fset(self, format_slot):
            assert format_slot in ('before', 'after', 'opening', 'closing', 'right', None)
            if format_slot is None:
                self._format_slot = 'opening'
            else:
                self._format_slot = format_slot
        return property(**locals()) 
